import torch
import torch.nn as nn
from peft import (
    LoraConfig,
    PeftConfig,
    PeftModel,
    get_peft_model,
)
from transformers import AutoModelForSequenceClassification


MODEL_ID = "Qwen/Qwen3-1.7B"

class LLamaModel(nn.Module):
    def __init__(self, classes, adapter_path=None, model_id=None):
        super(LLamaModel, self).__init__()
        # Prefer an explicit model_id; otherwise read it from the adapter configuration for evaluation.
        if model_id is not None:
            self.model_id = model_id
        elif adapter_path is not None:
            peft_config = PeftConfig.from_pretrained(adapter_path)
            self.model_id = peft_config.base_model_name_or_path
        else:
            self.model_id = MODEL_ID

        self.lora_config = LoraConfig(
            r=16,
            lora_alpha=16,
            lora_dropout=0.1,
            bias="none",
            target_modules=[
                "q_proj",
                "v_proj",
            ],
            task_type="SEQ_CLS"
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            num_labels=classes
        )

        if adapter_path is None:
            # BF16 LoRA: keep the base weights in BF16 and train only adapters.
            self.model.config.use_cache = False
            self.model.gradient_checkpointing_enable()
            self.model.enable_input_require_grads()
            self.model = get_peft_model(self.model, self.lora_config)
        else:
            # Evaluation: load the trained LoRA adapter instead of initializing a new one.
            self.model = PeftModel.from_pretrained(
                self.model,
                adapter_path,
                is_trainable=False,
            )

        self.model.config.pad_token_id = self.model.config.eos_token_id
        self.loss = nn.BCEWithLogitsLoss()

    def applyNonLinear(self, question_embedding):
        x = self.fcl(question_embedding)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

    def forward(self, input_ids, attention_mask, labels):
        question_embedding = self.model(input_ids=input_ids, attention_mask=attention_mask)
        logits = question_embedding["logits"]  # [batch_size, number_label]
        actual_r = labels
        loss = self.loss(logits, actual_r)
        return logits, loss
