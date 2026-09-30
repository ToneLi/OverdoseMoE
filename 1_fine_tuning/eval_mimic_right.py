import argparse
from pathlib import Path
import hashlib

from model import LLamaModel, MODEL_ID
from transformers import BertModel, AutoModelForSequenceClassification
import torch.nn as nn
import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from peft import LoraConfig, get_peft_model, PeftModel, PeftConfig
from accelerate import PartialState
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer
from sklearn.metrics import accuracy_score, f1_score, jaccard_score, precision_recall_curve, auc, roc_auc_score, \
    cohen_kappa_score, average_precision_score,precision_score
import json
import random
import numpy as np
import math
MAX_LEN = 512


def LabeltoOneHot(label):
    label = str(label).strip()
    if label == "1":
        return [0, 1]
    if label == "0":
        return [1, 0]
    raise ValueError(f"Unsupported label {label!r}; expected 0 or 1.")


# Model configuration
model_id = MODEL_ID
DEFAULT_DATA_FILE = Path(__file__).resolve().parent / "mock_data_10.jsonl"

logits_output = (
    Path(__file__).resolve().parent / "logits_moe" / "qwwen3_1_7b_test2.pt"
)


def get_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return tokenizer


def get_input_and_mask(sentences, tokenizer):
    sentences_infor = tokenizer(
        sentences, return_tensors="pt", padding=True, truncation=True, max_length=2000
    )
    return sentences_infor["input_ids"], sentences_infor["attention_mask"]


def get_data(file):
    sentences = []
    labels = []
    fingerprint = hashlib.sha256()
    with open(file, "r", encoding="utf-8") as fr:
        for line_number, line in enumerate(fr, start=1):
            if not line.strip():
                continue
            line = json.loads(line)
            # print(line.keys())
            if "icds" in line:
                sentence_ = line["icds"]
            elif "icd" in line:
                sentence_ = line["icd"]
            else:
                raise KeyError(
                    f"{file}:{line_number} must contain 'icds' or 'icd'."
                )
            # head_ = line["head"]
            # relation = line["relation"]
            # tail = line["tail"]
            if "label" not in line:
                raise KeyError(f"{file}:{line_number} must contain 'label'.")
            label = line["label"]
            # triple = head + " " + relation + " " + tail
            sentences.append(sentence_)
            labels.append(LabeltoOneHot(label))

            fingerprint.update(
                json.dumps(
                    {"icds": sentence_, "label": label},
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            )
            fingerprint.update(b"\n")
    if not sentences:
        raise ValueError(f"No samples found in {file}.")
    return sentences, labels, fingerprint.hexdigest()


from tqdm import tqdm
import torch
import torch.nn.functional as F

def compute_ece_from_logits(logits, labels, n_bins=10):
    """
    logits: torch.Tensor, shape [N, C]
    labels: torch.Tensor, shape [N] or one-hot [N, C]
    """
    if not torch.is_tensor(logits):
        logits = torch.tensor(logits)

    if not torch.is_tensor(labels):
        labels = torch.tensor(labels)

    # one-hot label -> class id
    if labels.ndim == 2:
        labels = torch.argmax(labels, dim=1)

    probs = F.softmax(logits.float(), dim=1)
    confidences, predictions = torch.max(probs, dim=1)
    correct = predictions.eq(labels).float()

    ece = torch.tensor(0.0, device=logits.device)

    bin_boundaries = torch.linspace(0, 1, n_bins + 1, device=logits.device)

    for i in range(n_bins):
        lower = bin_boundaries[i]
        upper = bin_boundaries[i + 1]

        if i == n_bins - 1:
            in_bin = (confidences >= lower) & (confidences <= upper)
        else:
            in_bin = (confidences >= lower) & (confidences < upper)

        prop_in_bin = in_bin.float().mean()

        if prop_in_bin.item() > 0:
            acc_in_bin = correct[in_bin].mean()
            conf_in_bin = confidences[in_bin].mean()
            ece += prop_in_bin * torch.abs(acc_in_bin - conf_in_bin)

    return ece.item()

def get_input_id(data_file=DEFAULT_DATA_FILE, batch_size=1, tokenizer=None):
    if batch_size <= 0:
        raise ValueError("batch_size must be positive.")
    if tokenizer is None:
        tokenizer = get_tokenizer()

    test_sentences, test_labels, fingerprint = get_data(data_file)
    test_input_ids, test_attention_masks = get_input_and_mask(
        test_sentences, tokenizer
    )

    # train_inputs = train_input_ids
    test_inputs = test_input_ids

    # train_labels = torch.FloatTensor(train_labels)
    test_labels = torch.FloatTensor(test_labels)

    # train_masks = train_attention_masks
    test_masks = test_attention_masks

    test_data = TensorDataset(test_inputs, test_masks, test_labels)
    test_sampler = SequentialSampler(test_data)
    test_dataloader = DataLoader(
        test_data, sampler=test_sampler, batch_size=batch_size
    )

    return "test_dataloader", test_dataloader, fingerprint


from tqdm import tqdm


def TE(
    model,
    validation_dataloader,
    fingerprint,
    output_path=logits_output,
    data_file=None,
    device=None,
):
    model.eval()
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Tracking variables
    test_loss, test_accuracy, test_f1, test_recall = 0, 0, 0, 0
    nb_test_steps, nb_test_examples = 0, 0
    # Evaluate data for one epoch
    # accuracy=accuracy_score(Gold,P)
    Gold = []
    P = []
    Pro = []
    all_logits=[]
    all_labels=[]

    for batch in tqdm(validation_dataloader):
        # Add batch to GPU
        batch = tuple(t.to(device) for t in batch)

        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask, b_labels = batch

        # Speeding up validation
        with torch.no_grad():
            outputs, _ = model(input_ids=b_input_ids,
                               attention_mask=b_input_mask,
                               labels=b_labels)

        # Get the "logits" output by the model. The "logits" are the output
        # values prior to applying an activation function like the softmax.
        logits = torch.argmax(outputs, dim=1)
        b_labels = torch.argmax(b_labels, dim=1)
        positive_probs = F.softmax(outputs.float(), dim=1)[:, 1]

        Gold.extend(b_labels.detach().cpu().tolist())
        P.extend(logits.detach().cpu().tolist())
        Pro.extend(positive_probs.detach().cpu().tolist())

        raw_logits = outputs.detach().cpu()
        raw_labels = b_labels.detach().cpu()

        all_logits.append(raw_logits)
        all_labels.append(raw_labels)

    #print(Gold)
    #print(P)
    #print("---------")

    precision = precision_score(Gold, P, zero_division=0)
    F1 = f1_score(Gold, P, zero_division=0)
    jaccard = jaccard_score(Gold, P, zero_division=0)
    # precision, recall = precision_recall_curve(Gold, P)
    auprc = average_precision_score(Gold, Pro)
    auroc = roc_auc_score(Gold, Pro) if len(set(Gold)) > 1 else float("nan")
    # kappa=cohen_kappa_score(Gold,P)

    
    all_logits=torch.cat(all_logits,dim=0)
    all_labels=torch.cat(all_labels,dim=0)
    sample_indices = torch.arange(all_labels.numel(), dtype=torch.long)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "logits": all_logits.float(),
        "labels": all_labels.long(),
        "sample_indices": sample_indices,
        "data_fingerprint": fingerprint,
    }
    if data_file is not None:
        payload["data_file"] = str(Path(data_file).resolve())
    torch.save(
        payload,
        output_path,
    )
    print(f"Saved {all_labels.numel()} logits to {output_path}")

    
    print("precision", precision)
    print("F1", F1)
    print("jaccard", jaccard)
    print("auprc", auprc)
    print("auroc", auroc)
    Gold_arr=np.array(Gold)
    Pro_arr=np.array(Pro)

    order=np.argsort(-Pro_arr)
    Gold_sorted=Gold_arr[order]

    total_n=len(Gold_sorted)
    total_pos=Gold_arr.sum()
    top_percents=[0.01,0.02,0.05,0.10]
    for p in top_percents:
        k=math.ceil(total_n*p)
        top_k_labels=Gold_sorted[:k]
        tp_k=top_k_labels.sum()
        ppv=tp_k/k if k>0 else 0
        recall_k=tp_k  / total_pos  if total_pos >0 else 0
        print(p,"--the PPV is ",ppv,"the recall is",recall_k)
    # print("kappa", kappa)
    # print("precision", precision)
    # print("recall", recall)

    # return global_P, global_R, global_F1

    ece = compute_ece_from_logits(all_logits, all_labels, n_bins=10)

    print("ECE:", ece)


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate and save aligned logits.")
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help="Test JSONL file (default: mock_data_10.jsonl).",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path(__file__).resolve().parent / "checkpoints",
        help="LoRA checkpoint directory.",
    )
    parser.add_argument("--output", type=Path, default=logits_output)
    parser.add_argument("--batch-size", type=int, default=1)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    patience = 5
    classes = 2

    if not args.data_file.is_file():
        raise FileNotFoundError(f"Test data file not found: {args.data_file}")
    if not args.checkpoint.is_dir():
        raise FileNotFoundError(f"Checkpoint directory not found: {args.checkpoint}")
    if not (args.checkpoint / "adapter_config.json").is_file():
        raise FileNotFoundError(
            f"LoRA adapter_config.json not found in: {args.checkpoint}"
        )

    tokenizer = get_tokenizer()
    _, test_dataloader, fingerprint = get_input_id(
        args.data_file,
        batch_size=args.batch_size,
        tokenizer=tokenizer,
    )
    model = LLamaModel(classes, adapter_path=str(args.checkpoint))

    seed_val = 42
    random.seed(seed_val)
    np.random.seed(seed_val)
    torch.manual_seed(seed_val)
    torch.cuda.manual_seed_all(seed_val)

    TE(
        model,
        test_dataloader,
        fingerprint,
        output_path=args.output,
        data_file=args.data_file,
    )

"""
CUDA_VISIBLE_DEVICES=0 nohup  python eval.py>myout.eval_2000 2>&1 &
CUDA_VISIBLE_DEVICES=7   python  eval.py

"""
