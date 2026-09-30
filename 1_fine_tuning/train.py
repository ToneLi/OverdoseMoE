import pandas as pd
# from keras.preprocessing.sequence import pad_sequences

from sklearn.model_selection import train_test_split
import torch

from torch.utils.data import Dataset, DataLoader, SequentialSampler, WeightedRandomSampler
from torch.optim import AdamW

from transformers import BertTokenizer, AutoTokenizer

import numpy as np

from transformers import get_linear_schedule_with_warmup
from model import LLamaModel, MODEL_ID
from sklearn.metrics import accuracy_score, recall_score, f1_score


# model_id = "/data/data_user/public_models/Llama3-OpenBioLLM-8B"
#model_id="/data/data_user/public_models/Llama-3.1/Meta-Llama-3.1-8B"
# model_id= "/data_218/storage/EHR_data/Models/Llama-3-hf/Meta-Llama-3-8B"
model_id = MODEL_ID
# model_id="/data/data_user/public_models/Llama-3/Meta-Llama-3-8B"


# tokenizer = BertTokenizer.from_pretrained('/data_266/python_envs/anaconda3/envs/transformers_cache/Bio_ClinicalBERT', do_lower_case=True)

import torch.nn as nn

import time
import datetime
import random
import json
from tqdm import tqdm

MAX_LEN = 2000

def labeltoOneHot(label):
    if label == "1":
        return [0, 1]
    else:  # indices = "y"
        return [1, 0]

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

def get_data(file):
    sentences = []
    labels = []
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
            labels.append(labeltoOneHot(label))

    return sentences, labels

def get_input_and_mask(sentences):
    # Do not pad the whole dataset to its single longest example. Padding is
    # applied dynamically to the longest example in each batch by collate_batch.
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


def get_input_id():
   
    train_sentences, train_labels = get_data("mock_data_10.jsonl")  # mimic3_mortality_ICD_train

    train_encodings = get_input_and_mask(train_sentences)

    test_sentences, test_labels = get_data("mock_data_10.jsonl")  # mimic3_mortality_ICD_dev
    test_encodings = get_input_and_mask(test_sentences)

    train_labels = torch.FloatTensor(train_labels)

    test_labels = torch.FloatTensor(test_labels)

    batch_size =16

    # Create the DataLoader for our training set.
    train_data = TokenizedDataset(train_encodings, train_labels)
    class_count = np.array([np.sum(train_labels.numpy()[:, i]) for i in range(train_labels.shape[1])])
    weights = 1.0 / class_count
    sample_weights = torch.tensor([weights[torch.argmax(label).item()] for label in train_labels])
    #train_sampler = RandomSampler(train_data)
    train_sampler = WeightedRandomSampler(weights=sample_weights, num_samples=len(sample_weights), replacement=True)

    train_dataloader = DataLoader(
        train_data,
        sampler=train_sampler,
        batch_size=batch_size,
        collate_fn=collate_batch,
    )

    # Create the DataLoader for our validation set.
    test_data = TokenizedDataset(test_encodings, test_labels)
    test_sampler = SequentialSampler(test_data)
    test_dataloader = DataLoader(
        test_data,
        sampler=test_sampler,
        batch_size=batch_size,
        collate_fn=collate_batch,
    )

    return train_dataloader, test_dataloader

def flat_PRF1(preds, labels):
    pred_flat = preds
    labels_flat = labels
    R = accuracy_score(pred_flat, labels_flat)
    P = recall_score(pred_flat, labels_flat)
    F1 = f1_score(pred_flat, labels_flat)
    return R, P, F1

def format_time(elapsed):
    '''
    Takes a time in seconds and returns a string hh:mm:ss
    '''

    # Round to the nearest second.
    elapsed_rounded = int(round(elapsed))

    # Format as hh:mm:ss
    return str(datetime.timedelta(seconds=elapsed_rounded))

def TE(model, validation_dataloader):
    model.eval()
    # Tracking variables
    test_loss, test_accuracy, test_f1, test_recall = 0, 0, 0, 0
    nb_test_steps, nb_test_examples = 0, 0

    # Evaluate data for one epoch
    for batch in validation_dataloader:
        # Add batch to GPU
        batch = tuple(t.cuda() for t in batch)

        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask, b_labels = batch

        # Speeding up validation
        with torch.no_grad():
            outputs, loss = model(
                input_ids=b_input_ids,
                attention_mask=b_input_mask,
                labels=b_labels
            )

        # Get the "logits" output by the model. The "Logits" are the output
        # values prior to applying an activation function like the softmax.
        logits = outputs
        logits = torch.argmax(logits, dim=1)
        b_labels = torch.argmax(b_labels, dim=1)

        # Move logits and labels to CPU
        logits = logits.detach().cpu().numpy()
        label_ids = b_labels.to('cpu').numpy()

        # Calculate the accuracy for this batch of test sentences.
        P, R, F1 = flat_PRF1(logits, label_ids)

        # Accumulate the total accuracy.
        test_accuracy += P
        test_f1 += F1
        test_recall += R

        # Track the number of batches
        nb_test_steps += 1

    # Report the final accuracy for this validation run.
    print(" Accuracy: {:.2f}".format(test_accuracy / nb_test_steps))
    print(" Recall: {:.2f}".format(test_recall / nb_test_steps))
    print(" F1: {:.2f}".format(test_f1 / nb_test_steps))
    print(" Test took: {}".format(format_time(time.time() - t0)))

    global_P = test_accuracy / nb_test_steps
    global_R = test_recall / nb_test_steps
    global_F1 = test_f1 / nb_test_steps

    return global_P, global_R, global_F1


if __name__ == "__main__":
    patience = 7
    classes = 2
    no_update=0
    time_start = time.time()
    train_dataloader, test_dataloader = get_input_id()
    model = LLamaModel(classes)
    # The BF16 base model is already placed by device_map="auto".
    best_model = model.state_dict()
    optimizer = AdamW(model.parameters(), lr=2e-5, eps=1e-8)  # args.adam_epsilon default is 1e-8.
    # Create the learning rate scheduler
    epochs = 20
    total_steps = len(train_dataloader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=total_steps
    )
    seed_val = 42
    random.seed(seed_val)
    np.random.seed(seed_val)
    torch.manual_seed(seed_val)
    torch.cuda.manual_seed_all(seed_val)

    # Store the average loss after each epoch so we can plot them
    loss_values = []

    best_score = -float("inf")

    for epoch_i in range(0, epochs):
        # Measure how long the training epoch takes
        t0 = time.time()
        total_loss = 0
        model.train()
        # For each batch of training data
        for step, batch in enumerate(train_dataloader):
            optimizer.zero_grad()
            # Progress update every 40 batches
            if step % 40 == 0 and not step == 0:
                elapsed = format_time(time.time() - t0)
                print(f"  Batch {step} of {len(train_dataloader)}. Elapsed: {elapsed}.")

            # Prepare input data
            b_input_ids = batch[0].cuda()#.to(device)
            b_input_mask = batch[1].cuda()#to(device)
            b_labels = batch[2].cuda()#.to(device)
            # Forward pass
            score, loss = model(
                input_ids=b_input_ids,
                attention_mask=b_input_mask,
                labels=b_labels
            )
            # Accumulate the loss
            total_loss += loss.item()

            # Perform a backward pass to calculate the gradients
            loss.backward()
            # Clip the norm of the gradients to prevent "exploding gradients"
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            # Update parameters and take a step using the computed gradient
            optimizer.step()
            # Update the learning rate
            scheduler.step()
            # Calculate the average loss over the training data
        avg_train_loss = total_loss / len(train_dataloader)
        # Store the loss value for plotting the learning curve
        loss_values.append(avg_train_loss)

        print("")
        print(f" Average training loss: {avg_train_loss:.2f}")
        print(f" Training epoch took: {format_time(time.time() - t0)}")

        # Validation
        print("")
        print("Running Validation...")
        t0 = time.time()
        eps = 0.0001
        # Put the model in evaluation mode
        print("Testing...")
        global_P, global_R, global_F1 = TE(model, test_dataloader)
        test_per = f"P: {global_P} - R: {global_R} - F1: {global_F1}"

        if global_F1 > best_score+eps:
            best_score = global_F1
            no_update = 0

            if global_F1 > 0.10:
                # best_model = model.state_dict()
                print(f" F1 has increased from previous epoch: {global_F1}")
                checkpoint_path = "checkpoints/"
                model.model.save_pretrained(checkpoint_path)

        elif (global_F1 < best_score + eps) and (no_update < patience):
                no_update += 1
                print("Validation F1 decreases to %s from %s, %d more epoch to check" % (
                    global_F1, best_score, patience - no_update))
        elif no_update == patience:
                print("Model has exceed patience. Saving best model and exiting")
                # torch.save(best_model, checkpoint_path + "best_score_model.pt")
                time_end = time.time()
                # fw_results.write("time-cost:" + str((time_end - time_start) / 60) + "\n")
                exit()

        if epoch_i == epochs - 1:
                print("Final Epoch has reached. Stopping and saving model.")
                # torch.save(best_model, checkpoint_path + "best_score_model.pt")
                time_end = time.time()
                # fw_results.write("time-cost:" + str((time_end - time_start) / 60) + "\n")
                exit()


"""
CUDA_VISIBLE_DEVICES=1 nohup torchrun --nproc-per-node=1 --master-port=12347 train.py > myout.biomllmama38 2>&1 &

CUDA_VISIBLE_DEVICES=1   torchrun --nproc-per-node=1   train.py  

CUDA_VISIBLE_DEVICES=0   python   train.py  

CUDA_VISIBLE_DEVICES=5  nohup python train.py > myout.train 2>&1 &

"""
