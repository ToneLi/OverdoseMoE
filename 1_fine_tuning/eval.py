from pathlib import Path
import argparse
import hashlib

from model import LLamaModel, MODEL_ID
from transformers import BertModel, AutoModelForSequenceClassification
import torch.nn as nn
import torch
from torch.utils.data import Dataset, DataLoader, SequentialSampler
from peft import LoraConfig, get_peft_model, PeftModel, PeftConfig
from accelerate import PartialState
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer
from sklearn.metrics import accuracy_score, f1_score, jaccard_score, precision_recall_curve, auc, roc_auc_score, \
    cohen_kappa_score, average_precision_score,precision_score
import json
import random
import numpy as np
import math
MAX_LEN = 2000
DEFAULT_DATA_FILE = Path(
    "/mnt/data_218/home1/Cool_Chen/OOD_data_OUD_corhot/"
    "data_by_junhui_right/811_test_ood.jsonl"
)
DEFAULT_LOGITS_OUTPUT = (
    Path(__file__).resolve().parent / "logits_moe" / "biollama3_1_7b_test.pt"
)


def LabeltoOneHot(label):
    if label == "1":
        return [0, 1]
    else:  # label == "True"
        return [1, 0]


# Model configuration
model_id = MODEL_ID
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"


def get_input_and_mask(sentences):
    return tokenizer(sentences, padding=False, truncation=True, max_length=MAX_LEN)


class TokenizedDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        return {
            "input_ids": self.encodings["input_ids"][index],
            "attention_mask": self.encodings["attention_mask"][index],
            "labels": self.labels[index],
        }


def collate_batch(features):
    labels = torch.stack([feature["labels"] for feature in features])
    token_features = [
        {
            "input_ids": feature["input_ids"],
            "attention_mask": feature["attention_mask"],
        }
        for feature in features
    ]
    batch = tokenizer.pad(
        token_features,
        padding=True,
        pad_to_multiple_of=8,
        return_tensors="pt",
    )
    return batch["input_ids"], batch["attention_mask"], labels


def get_data(file):
    sentences = []
    labels = []
    fingerprint = hashlib.sha256()
    with open(file, "r", encoding="utf-8") as fr:
        for line in fr.readlines():
            line = json.loads(line)
            # print(line.keys())
            sentence_ = line["icd"]
            # head_ = line["head"]
            # relation = line["relation"]
            # tail = line["tail"]
            label = line["label"]
            # triple = head + " " + relation + " " + tail
            sentences.append(sentence_)
            labels.append(LabeltoOneHot(label))
            fingerprint.update(
                json.dumps(
                    {"icd": sentence_, "label": label},
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            )
            fingerprint.update(b"\n")

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

def get_input_id(data_file):
    test_sentences, test_labels, data_fingerprint = get_data(data_file)
    test_encodings = get_input_and_mask(test_sentences)

    # train_labels = torch.FloatTensor(train_labels)
    test_labels = torch.FloatTensor(test_labels)

    batch_size = 1

    test_data = TokenizedDataset(test_encodings, test_labels)
    test_sampler = SequentialSampler(test_data)
    test_dataloader = DataLoader(
        test_data,
        sampler=test_sampler,
        batch_size=batch_size,
        collate_fn=collate_batch,
    )

    return "train_dataloader", test_dataloader, data_fingerprint


from tqdm import tqdm


def TE(model, validation_dataloader, logits_output, data_fingerprint, data_file):
    model.eval()
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
        batch = tuple(t.cuda() for t in batch)

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
            # b_labels.to('cpu').numpy()
        logits = logits.detach().cpu().item()
        label_ids = b_labels.to("cpu").item()

        Gold += [label_ids]
        P +=  [logits]
        Pro.append(outputs[0][1].cpu().item())

        raw_logits = outputs.detach().cpu()
        raw_labels = b_labels.detach().cpu()

        all_logits.append(raw_logits)
        all_labels.append(raw_labels)

    #print(Gold)
    #print(P)
    #print("---------")

    precision = precision_score(Gold, P)
    F1 = f1_score(Gold, P)
    jaccard = jaccard_score(Gold, P)
    # precision, recall = precision_recall_curve(Gold, P)
    auprc = average_precision_score(Gold, Pro)
    auroc = roc_auc_score(Gold, Pro)
    # kappa=cohen_kappa_score(Gold,P)

    
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

    all_logits=torch.cat(all_logits,dim=0)
    all_labels=torch.cat(all_labels,dim=0)
    sample_indices = torch.arange(all_labels.numel(), dtype=torch.long)
    logits_output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "schema_version": 1,
            "logits": all_logits.float(),
            "labels": all_labels.long(),
            "sample_indices": sample_indices,
            "data_fingerprint": data_fingerprint,
            "data_file": str(data_file.resolve()),
        },
        logits_output,
    )
    print(f"Saved {all_labels.numel()} logits to {logits_output}")
    ece = compute_ece_from_logits(all_logits, all_labels, n_bins=10)

    print("ECE:", ece)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-file", type=Path, default=DEFAULT_DATA_FILE)
    parser.add_argument("--logits-output", type=Path, default=DEFAULT_LOGITS_OUTPUT)
    args = parser.parse_args()

    patience = 5
    classes = 2

    _, test_dataloader, data_fingerprint = get_input_id(args.data_file)

    checkpoint_path = Path(__file__).resolve().parent / "checkpoints"
    model = LLamaModel(classes, adapter_path=str(checkpoint_path))

    seed_val = 42
    random.seed(seed_val)
    np.random.seed(seed_val)
    torch.manual_seed(seed_val)
    torch.cuda.manual_seed_all(seed_val)

    out_label = TE(
        model,
        test_dataloader,
        args.logits_output,
        data_fingerprint,
        args.data_file,
    )

"""
CUDA_VISIBLE_DEVICES=0 nohup  python eval.py>myout.K_eval 2>&1 &
CUDA_VISIBLE_DEVICES=7   python  eval.py

"""
