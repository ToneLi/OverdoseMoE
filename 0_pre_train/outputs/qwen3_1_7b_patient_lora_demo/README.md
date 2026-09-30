---
library_name: peft
license: other
base_model: Qwen/Qwen3-0.6B
tags:
- llama-factory
- lora
- generated_from_trainer
model-index:
- name: qwen3_1_7b_patient_lora_demo
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# qwen3_1_7b_patient_lora_demo

This model is a fine-tuned version of [Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) on the patient_pretrain_train dataset.
It achieves the following results on the evaluation set:
- Loss: 3.6679

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 0.0001
- train_batch_size: 1
- eval_batch_size: 1
- seed: 42
- distributed_type: multi-GPU
- num_devices: 4
- total_train_batch_size: 4
- total_eval_batch_size: 4
- optimizer: Use adamw_torch with betas=(0.9,0.999) and epsilon=1e-08 and optimizer_args=No additional optimizer arguments
- lr_scheduler_type: cosine
- lr_scheduler_warmup_ratio: 0.1
- training_steps: 2

### Training results

| Training Loss | Epoch | Step | Validation Loss |
|:-------------:|:-----:|:----:|:---------------:|
| 3.3957        | 0.5   | 1    | 3.7373          |
| 3.362         | 1.0   | 2    | 3.6679          |


### Framework versions

- PEFT 0.15.2
- Transformers 4.52.4
- Pytorch 2.6.0+cu126
- Datasets 4.0.0
- Tokenizers 0.21.4