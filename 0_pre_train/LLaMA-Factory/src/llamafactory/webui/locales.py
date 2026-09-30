# Copyright 2025 the LlamaFactory team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

LOCALES = {
    "title": {
        "en": {
            "value": "<h1><center>🦙🏭LLaMA Factory: Unified Efficient Fine-Tuning of 100+ LLMs</center></h1>",
        },
        "ru": {
            "value": "<h1><center>🦙🏭LLaMA Factory: Унифицированная эффективная тонкая настройка 100+ LLMs</center></h1>",
        },
        "zh": {'value': '<h1><center>🦙🏭LLaMA Factory: Unified Efficient Fine-Tuning of 100+ LLMs</center></h1>'},
        "ko": {
            "value": "<h1><center>🦙🏭LLaMA Factory: 100+ LLMs를 위한 통합 효율적인 튜닝</center></h1>",
        },
        "ja": {'value': '<h1><center>🦙🏭LLaMA Factory: Unified Efficient Fine-Tuning of 100+ LLMs</center></h1>'},
    },
    "subtitle": {
        "en": {
            "value": (
                "<h3><center>Visit <a href='https://github.com/hiyouga/LLaMA-Factory' target='_blank'>"
                "GitHub Page</a> <a href='https://llamafactory.readthedocs.io/en/latest/' target='_blank'>"
                "Documentation</a> <a href='https://blog.llamafactory.net/en/' target='_blank'>"
                "Blog</a></center></h3>"
            ),
        },
        "ru": {
            "value": (
                "<h3><center>Посетить <a href='https://github.com/hiyouga/LLaMA-Factory' target='_blank'>"
                "страницу GitHub</a> <a href='https://llamafactory.readthedocs.io/en/latest/' target='_blank'>"
                "Документацию</a> <a href='https://blog.llamafactory.net/en/' target='_blank'>"
                "Блог</a></center></h3>"
            ),
        },
        "zh": {'value': "<h3><center>Visit <a href='https://github.com/hiyouga/LLaMA-Factory' target='_blank'>GitHub Page</a> <a href='https://llamafactory.readthedocs.io/en/latest/' target='_blank'>Documentation</a> <a href='https://blog.llamafactory.net/en/' target='_blank'>Blog</a></center></h3>"},
        "ko": {
            "value": (
                "<h3><center><a href='https://github.com/hiyouga/LLaMA-Factory' target='_blank'>"
                "GitHub 페이지</a> <a href='https://llamafactory.readthedocs.io/en/latest/' target='_blank'>"
                "공식 문서</a> <a href='https://blog.llamafactory.net/en/' target='_blank'>"
                "블로그</a>를 방문하세요.</center></h3>"
            ),
        },
        "ja": {
            "value": (
                "<h3><center><a href='https://github.com/hiyouga/LLaMA-Factory' target='_blank'>"
                "GitHub ページ</a> <a href='https://llamafactory.readthedocs.io/en/latest/' target='_blank'>"
                "ドキュメント</a> <a href='https://blog.llamafactory.net/en/' target='_blank'>"
                "ブログ</a>にアクセスする</center></h3>"
            ),
        },
    },
    "lang": {
        "en": {
            "label": "Language",
        },
        "ru": {
            "label": "Язык",
        },
        "zh": {'label': 'Language'},
        "ko": {
            "label": "언어",
        },
        "ja": {'label': 'Language'},
    },
    "model_name": {
        "en": {
            "label": "Model name",
            "info": "Input the initial name to search for the model.",
        },
        "ru": {
            "label": "Название модели",
            "info": "Введите начальное имя для поиска модели.",
        },
        "zh": {'label': 'Model name', 'info': 'Input the initial name to search for the model.'},
        "ko": {
            "label": "모델 이름",
            "info": "모델을 검색할 초기 이름을 입력하세요.",
        },
        "ja": {'label': 'Model name', 'info': 'Input the initial name to search for the model.'},
    },
    "model_path": {
        "en": {
            "label": "Model path",
            "info": "Path to pretrained model or model identifier from Hugging Face.",
        },
        "ru": {
            "label": "Путь к модели",
            "info": "Путь к предварительно обученной модели или идентификатор модели от Hugging Face.",
        },
        "zh": {'label': 'Model path', 'info': 'Path to pretrained model or model identifier from Hugging Face.'},
        "ko": {
            "label": "모델 경로",
            "info": "사전 훈련된 모델의 경로 또는 Hugging Face의 모델 식별자.",
        },
        "ja": {'label': 'Model path', 'info': 'Path to pretrained model or model identifier from Hugging Face.'},
    },
    "hub_name": {
        "en": {
            "label": "Hub name",
            "info": "Choose the model download source.",
        },
        "ru": {
            "label": "Имя хаба",
            "info": "Выберите источник загрузки модели.",
        },
        "zh": {'label': 'Hub name', 'info': 'Choose the model download source.'},
        "ko": {
            "label": "모델 다운로드 소스",
            "info": "모델 다운로드 소스를 선택하세요.",
        },
        "ja": {'label': 'Hub name', 'info': 'Choose the model download source.'},
    },
    "finetuning_type": {
        "en": {
            "label": "Finetuning method",
        },
        "ru": {
            "label": "Метод дообучения",
        },
        "zh": {'label': 'Finetuning method'},
        "ko": {
            "label": "파인튜닝 방법",
        },
        "ja": {'label': 'Finetuning method'},
    },
    "checkpoint_path": {
        "en": {
            "label": "Checkpoint path",
        },
        "ru": {
            "label": "Путь контрольной точки",
        },
        "zh": {'label': 'Checkpoint path'},
        "ko": {
            "label": "체크포인트 경로",
        },
        "ja": {
            "label": "チェックポイントパス",
        },
    },
    "quantization_bit": {
        "en": {
            "label": "Quantization bit",
            "info": "Enable quantization (QLoRA).",
        },
        "ru": {
            "label": "Уровень квантования",
            "info": "Включить квантование (QLoRA).",
        },
        "zh": {'label': 'Quantization bit', 'info': 'Enable quantization (QLoRA).'},
        "ko": {
            "label": "양자화 비트",
            "info": "양자화 활성화 (QLoRA).",
        },
        "ja": {'label': 'Quantization bit', 'info': 'Enable quantization (QLoRA).'},
    },
    "quantization_method": {
        "en": {
            "label": "Quantization method",
            "info": "Quantization algorithm to use.",
        },
        "ru": {
            "label": "Метод квантования",
            "info": "Алгоритм квантования, который следует использовать.",
        },
        "zh": {'label': 'Quantization method', 'info': 'Quantization algorithm to use.'},
        "ko": {
            "label": "양자화 방법",
            "info": "사용할 양자화 알고리즘.",
        },
        "ja": {'label': 'Quantization method', 'info': 'Quantization algorithm to use.'},
    },
    "template": {
        "en": {
            "label": "Chat template",
            "info": "The chat template used in constructing prompts.",
        },
        "ru": {
            "label": "Шаблон чата",
            "info": "Шаблон чата используемый для составления подсказок.",
        },
        "zh": {'label': 'Chat template', 'info': 'The chat template used in constructing prompts.'},
        "ko": {
            "label": "채팅 템플릿",
            "info": "프롬프트 작성에 사용되는 채팅 템플릿.",
        },
        "ja": {'label': 'Chat template', 'info': 'The chat template used in constructing prompts.'},
    },
    "rope_scaling": {
        "en": {
            "label": "RoPE scaling",
            "info": "RoPE scaling method to use.",
        },
        "ru": {
            "label": "Масштабирование RoPE",
            "info": "Метод масштабирования RoPE для использования.",
        },
        "zh": {'label': 'RoPE scaling', 'info': 'RoPE scaling method to use.'},
        "ko": {
            "label": "RoPE 스케일링",
            "info": "사용할 RoPE 스케일링 방법.",
        },
        "ja": {'label': 'RoPE scaling', 'info': 'RoPE scaling method to use.'},
    },
    "booster": {
        "en": {
            "label": "Booster",
            "info": "Approach used to boost training speed.",
        },
        "ru": {
            "label": "Ускоритель",
            "info": "Подход, используемый для ускорения обучения.",
        },
        "zh": {'label': 'Booster', 'info': 'Approach used to boost training speed.'},
        "ko": {
            "label": "부스터",
            "info": "훈련 속도를 향상시키기 위해 사용된 접근 방식.",
        },
        "ja": {'label': 'Booster', 'info': 'Approach used to boost training speed.'},
    },
    "training_stage": {
        "en": {
            "label": "Stage",
            "info": "The stage to perform in training.",
        },
        "ru": {
            "label": "Этап",
            "info": "Этап выполнения обучения.",
        },
        "zh": {'label': 'Stage', 'info': 'The stage to perform in training.'},
        "ko": {
            "label": "학습 단계",
            "info": "수행할 학습 방법.",
        },
        "ja": {'label': 'Stage', 'info': 'The stage to perform in training.'},
    },
    "dataset_dir": {
        "en": {
            "label": "Data dir",
            "info": "Path to the data directory.",
        },
        "ru": {
            "label": "Директория данных",
            "info": "Путь к директории данных.",
        },
        "zh": {'label': 'Data dir', 'info': 'Path to the data directory.'},
        "ko": {
            "label": "데이터 디렉토리",
            "info": "데이터 디렉토리의 경로.",
        },
        "ja": {
            "label": "データディレクトリ",
            "info": "データディレクトリへのパス。",
        },
    },
    "dataset": {
        "en": {
            "label": "Dataset",
        },
        "ru": {
            "label": "Набор данных",
        },
        "zh": {'label': 'Dataset'},
        "ko": {
            "label": "데이터셋",
        },
        "ja": {
            "label": "データセット",
        },
    },
    "data_preview_btn": {
        "en": {
            "value": "Preview dataset",
        },
        "ru": {
            "value": "Просмотреть набор данных",
        },
        "zh": {'value': 'Preview dataset'},
        "ko": {
            "value": "데이터셋 미리보기",
        },
        "ja": {
            "value": "データセットをプレビュー",
        },
    },
    "preview_count": {
        "en": {
            "label": "Count",
        },
        "ru": {
            "label": "Количество",
        },
        "zh": {'label': 'Count'},
        "ko": {
            "label": "개수",
        },
        "ja": {
            "label": "カウント",
        },
    },
    "page_index": {
        "en": {
            "label": "Page",
        },
        "ru": {
            "label": "Страница",
        },
        "zh": {'label': 'Page'},
        "ko": {
            "label": "페이지",
        },
        "ja": {
            "label": "ページ",
        },
    },
    "prev_btn": {
        "en": {
            "value": "Prev",
        },
        "ru": {
            "value": "Предыдущая",
        },
        "zh": {'value': 'Prev'},
        "ko": {
            "value": "이전",
        },
        "ja": {'value': 'Prev'},
    },
    "next_btn": {
        "en": {
            "value": "Next",
        },
        "ru": {
            "value": "Следующая",
        },
        "zh": {'value': 'Next'},
        "ko": {
            "value": "다음",
        },
        "ja": {'value': 'Next'},
    },
    "close_btn": {
        "en": {
            "value": "Close",
        },
        "ru": {
            "value": "Закрыть",
        },
        "zh": {'value': 'Close'},
        "ko": {
            "value": "닫기",
        },
        "ja": {'value': 'Close'},
    },
    "preview_samples": {
        "en": {
            "label": "Samples",
        },
        "ru": {
            "label": "Примеры",
        },
        "zh": {'label': 'Samples'},
        "ko": {
            "label": "샘플",
        },
        "ja": {
            "label": "サンプル",
        },
    },
    "learning_rate": {
        "en": {
            "label": "Learning rate",
            "info": "Initial learning rate for AdamW.",
        },
        "ru": {
            "label": "Скорость обучения",
            "info": "Начальная скорость обучения для AdamW.",
        },
        "zh": {'label': 'Learning rate', 'info': 'Initial learning rate for AdamW.'},
        "ko": {
            "label": "학습률",
            "info": "AdamW의 초기 학습률.",
        },
        "ja": {'label': 'Learning rate', 'info': 'Initial learning rate for AdamW.'},
    },
    "num_train_epochs": {
        "en": {
            "label": "Epochs",
            "info": "Total number of training epochs to perform.",
        },
        "ru": {
            "label": "Эпохи",
            "info": "Общее количество эпох обучения.",
        },
        "zh": {'label': 'Epochs', 'info': 'Total number of training epochs to perform.'},
        "ko": {
            "label": "에포크",
            "info": "수행할 총 학습 에포크 수.",
        },
        "ja": {'label': 'Epochs', 'info': 'Total number of training epochs to perform.'},
    },
    "max_grad_norm": {
        "en": {
            "label": "Maximum gradient norm",
            "info": "Norm for gradient clipping.",
        },
        "ru": {
            "label": "Максимальная норма градиента",
            "info": "Норма для обрезки градиента.",
        },
        "zh": {'label': 'Maximum gradient norm', 'info': 'Norm for gradient clipping.'},
        "ko": {
            "label": "최대 그레디언트 노름(norm)",
            "info": "그레디언트 클리핑을 위한 노름(norm).",
        },
        "ja": {'label': 'Maximum gradient norm', 'info': 'Norm for gradient clipping.'},
    },
    "train_seed": {
        "en": {
            "label": "Seed",
            "info": "Random seed for training.",
        },
        "ru": {
            "label": "Seed",
            "info": "Random seed for training.",
        },
        "zh": {'label': 'Seed', 'info': 'Random seed for training.'},
        "ko": {
            "label": "Seed",
            "info": "Random seed for training.",
        },
        "ja": {
            "label": "Seed",
            "info": "Random seed for training.",
        },
    },
    "max_samples": {
        "en": {
            "label": "Max samples",
            "info": "Maximum samples per dataset.",
        },
        "ru": {
            "label": "Максимальное количество образцов",
            "info": "Максимальное количество образцов на набор данных.",
        },
        "zh": {'label': 'Max samples', 'info': 'Maximum samples per dataset.'},
        "ko": {
            "label": "최대 샘플 수",
            "info": "데이터셋 당 최대 샘플 수.",
        },
        "ja": {'label': 'Max samples', 'info': 'Maximum samples per dataset.'},
    },
    "compute_type": {
        "en": {
            "label": "Compute type",
            "info": "Whether to use mixed precision training.",
        },
        "ru": {
            "label": "Тип вычислений",
            "info": "Использовать ли обучение смешанной точности.",
        },
        "zh": {'label': 'Compute type', 'info': 'Whether to use mixed precision training.'},
        "ko": {
            "label": "연산 유형",
            "info": "혼합 정밀도 훈련을 사용할지 여부.",
        },
        "ja": {'label': 'Compute type', 'info': 'Whether to use mixed precision training.'},
    },
    "cutoff_len": {
        "en": {
            "label": "Cutoff length",
            "info": "Max tokens in input sequence.",
        },
        "ru": {
            "label": "Длина обрезки",
            "info": "Максимальное количество токенов во входной последовательности.",
        },
        "zh": {'label': 'Cutoff length', 'info': 'Max tokens in input sequence.'},
        "ko": {
            "label": "컷오프 길이",
            "info": "입력 시퀀스의 최대 토큰 수.",
        },
        "ja": {'label': 'Cutoff length', 'info': 'Max tokens in input sequence.'},
    },
    "batch_size": {
        "en": {
            "label": "Batch size",
            "info": "Number of samples processed on each GPU.",
        },
        "ru": {
            "label": "Размер пакета",
            "info": "Количество образцов для обработки на каждом GPU.",
        },
        "zh": {'label': 'Batch size', 'info': 'Number of samples processed on each GPU.'},
        "ko": {
            "label": "배치 크기",
            "info": "각 GPU에서 처리되는 샘플 수.",
        },
        "ja": {'label': 'Batch size', 'info': 'Number of samples processed on each GPU.'},
    },
    "gradient_accumulation_steps": {
        "en": {
            "label": "Gradient accumulation",
            "info": "Number of steps for gradient accumulation.",
        },
        "ru": {
            "label": "Накопление градиента",
            "info": "Количество шагов накопления градиента.",
        },
        "zh": {'label': 'Gradient accumulation', 'info': 'Number of steps for gradient accumulation.'},
        "ko": {
            "label": "그레디언트 누적",
            "info": "그레디언트 누적 단계 수.",
        },
        "ja": {'label': 'Gradient accumulation', 'info': 'Number of steps for gradient accumulation.'},
    },
    "val_size": {
        "en": {
            "label": "Val size",
            "info": "Percentage of validation set from the entire dataset.",
        },
        "ru": {
            "label": "Размер валидации",
            "info": "Пропорция данных в наборе для разработки.",
        },
        "zh": {'label': 'Val size', 'info': 'Percentage of validation set from the entire dataset.'},
        "ko": {
            "label": "검증 데이터셋 크기",
            "info": "개발 데이터셋에서 검증 데이터의 비율.",
        },
        "ja": {'label': 'Val size', 'info': 'Percentage of validation set from the entire dataset.'},
    },
    "lr_scheduler_type": {
        "en": {
            "label": "LR scheduler",
            "info": "Name of the learning rate scheduler.",
        },
        "ru": {
            "label": "Планировщик скорости обучения",
            "info": "Название планировщика скорости обучения.",
        },
        "zh": {'label': 'LR scheduler', 'info': 'Name of the learning rate scheduler.'},
        "ko": {
            "label": "LR 스케줄러",
            "info": "학습률 스케줄러의 이름.",
        },
        "ja": {'label': 'LR scheduler', 'info': 'Name of the learning rate scheduler.'},
    },
    "extra_tab": {
        "en": {
            "label": "Extra configurations",
        },
        "ru": {
            "label": "Дополнительные конфигурации",
        },
        "zh": {'label': 'Extra configurations'},
        "ko": {
            "label": "추가 구성(configuration)",
        },
        "ja": {'label': 'Extra configurations'},
    },
    "logging_steps": {
        "en": {
            "label": "Logging steps",
            "info": "Number of steps between two logs.",
        },
        "ru": {
            "label": "Шаги логирования",
            "info": "Количество шагов между двумя записями в журнале.",
        },
        "zh": {'label': 'Logging steps', 'info': 'Number of steps between two logs.'},
        "ko": {
            "label": "로깅 스텝",
            "info": "이전 로깅과 다음 로깅 간 스텝 수.",
        },
        "ja": {'label': 'Logging steps', 'info': 'Number of steps between two logs.'},
    },
    "save_steps": {
        "en": {
            "label": "Save steps",
            "info": "Number of steps between two checkpoints.",
        },
        "ru": {
            "label": "Шаги сохранения",
            "info": "Количество шагов между двумя контрольными точками.",
        },
        "zh": {'label': 'Save steps', 'info': 'Number of steps between two checkpoints.'},
        "ko": {
            "label": "저장 스텝",
            "info": "이전 체크포인트와 다음 체크포인트 사이의 스텝 수.",
        },
        "ja": {'label': 'Save steps', 'info': 'Number of steps between two checkpoints.'},
    },
    "warmup_steps": {
        "en": {
            "label": "Warmup steps",
            "info": "Number of steps used for warmup.",
        },
        "ru": {
            "label": "Шаги прогрева",
            "info": "Количество шагов, используемых для прогрева.",
        },
        "zh": {'label': 'Warmup steps', 'info': 'Number of steps used for warmup.'},
        "ko": {
            "label": "Warmup 스텝",
            "info": "Warmup에 사용되는 스텝 수.",
        },
        "ja": {'label': 'Warmup steps', 'info': 'Number of steps used for warmup.'},
    },
    "neftune_alpha": {
        "en": {
            "label": "NEFTune alpha",
            "info": "Magnitude of noise adding to embedding vectors.",
        },
        "ru": {
            "label": "NEFTune alpha",
            "info": "Величина шума, добавляемого к векторам вложений.",
        },
        "zh": {'label': 'NEFTune alpha', 'info': 'Magnitude of noise adding to embedding vectors.'},
        "ko": {
            "label": "NEFTune 알파",
            "info": "임베딩 벡터에 추가되는 노이즈의 크기.",
        },
        "ja": {'label': 'NEFTune alpha', 'info': 'Magnitude of noise adding to embedding vectors.'},
    },
    "extra_args": {
        "en": {
            "label": "Extra arguments",
            "info": "Extra arguments passed to the trainer in JSON format.",
        },
        "ru": {
            "label": "Дополнительные аргументы",
            "info": "Дополнительные аргументы, которые передаются тренеру в формате JSON.",
        },
        "zh": {'label': 'Extra arguments', 'info': 'Extra arguments passed to the trainer in JSON format.'},
        "ko": {
            "label": "추가 인수",
            "info": "JSON 형식으로 트레이너에게 전달할 추가 인수입니다.",
        },
        "ja": {'label': 'Extra arguments', 'info': 'Extra arguments passed to the trainer in JSON format.'},
    },
    "packing": {
        "en": {
            "label": "Pack sequences",
            "info": "Pack sequences into samples of fixed length.",
        },
        "ru": {
            "label": "Упаковка последовательностей",
            "info": "Упаковка последовательностей в образцы фиксированной длины.",
        },
        "zh": {'label': 'Pack sequences', 'info': 'Pack sequences into samples of fixed length.'},
        "ko": {
            "label": "시퀀스 패킹",
            "info": "고정된 길이의 샘플로 시퀀스를 패킹합니다.",
        },
        "ja": {'label': 'Pack sequences', 'info': 'Pack sequences into samples of fixed length.'},
    },
    "neat_packing": {
        "en": {
            "label": "Use neat packing",
            "info": "Avoid cross-attention between packed sequences.",
        },
        "ru": {
            "label": "Используйте аккуратную упаковку",
            "info": "избегайте перекрестного внимания между упакованными последовательностями.",
        },
        "zh": {'label': 'Use neat packing', 'info': 'Avoid cross-attention between packed sequences.'},
        "ko": {
            "label": "니트 패킹 사용",
            "info": "패킹된 시퀀스 간의 크로스 어텐션을 피합니다.",
        },
        "ja": {'label': 'Use neat packing', 'info': 'Avoid cross-attention between packed sequences.'},
    },
    "train_on_prompt": {
        "en": {
            "label": "Train on prompt",
            "info": "Disable the label mask on the prompt (only for SFT).",
        },
        "ru": {
            "label": "Тренировка на подсказке",
            "info": "Отключить маску меток на подсказке (только для SFT).",
        },
        "zh": {'label': 'Train on prompt', 'info': 'Disable the label mask on the prompt (only for SFT).'},
        "ko": {
            "label": "프롬프트도 학습",
            "info": "프롬프트에서 라벨 마스킹을 비활성화합니다 (SFT에만 해당).",
        },
        "ja": {'label': 'Train on prompt', 'info': 'Disable the label mask on the prompt (only for SFT).'},
    },
    "mask_history": {
        "en": {
            "label": "Mask history",
            "info": "Train on the last turn only (only for SFT).",
        },
        "ru": {
            "label": "История масок",
            "info": "Тренироваться только на последнем шаге (только для SFT).",
        },
        "zh": {'label': 'Mask history', 'info': 'Train on the last turn only (only for SFT).'},
        "ko": {
            "label": "히스토리 마스킹",
            "info": "대화 데이터의 마지막 턴만 학습합니다 (SFT에만 해당).",
        },
        "ja": {'label': 'Mask history', 'info': 'Train on the last turn only (only for SFT).'},
    },
    "resize_vocab": {
        "en": {
            "label": "Resize token embeddings",
            "info": "Resize the tokenizer vocab and the embedding layers.",
        },
        "ru": {
            "label": "Изменение размера токенных эмбеддингов",
            "info": "Изменить размер словаря токенизатора и слоев эмбеддинга.",
        },
        "zh": {'label': 'Resize token embeddings', 'info': 'Resize the tokenizer vocab and the embedding layers.'},
        "ko": {
            "label": "토큰 임베딩의 사이즈 조정",
            "info": "토크나이저 어휘와 임베딩 레이어의 크기를 조정합니다.",
        },
        "ja": {'label': 'Resize token embeddings', 'info': 'Resize the tokenizer vocab and the embedding layers.'},
    },
    "use_llama_pro": {
        "en": {
            "label": "Enable LLaMA Pro",
            "info": "Make the parameters in the expanded blocks trainable.",
        },
        "ru": {
            "label": "Включить LLaMA Pro",
            "info": "Сделать параметры в расширенных блоках обучаемыми.",
        },
        "zh": {'label': 'Enable LLaMA Pro', 'info': 'Make the parameters in the expanded blocks trainable.'},
        "ko": {
            "label": "LLaMA Pro 사용",
            "info": "확장된 블록의 매개변수를 학습 가능하게 만듭니다.",
        },
        "ja": {'label': 'Enable LLaMA Pro', 'info': 'Make the parameters in the expanded blocks trainable.'},
    },
    "enable_thinking": {
        "en": {
            "label": "Enable thinking",
            "info": "Whether or not to enable thinking mode for reasoning models.",
        },
        "ru": {
            "label": "Включить мысли",
            "info": "Включить режим мысли для моделей решающего характера.",
        },
        "zh": {'label': 'Enable thinking', 'info': 'Whether or not to enable thinking mode for reasoning models.'},
        "ko": {
            "label": "생각 모드 활성화",
            "info": "추론 모델의 생각 모드를 활성화할지 여부.",
        },
        "ja": {'label': 'Enable thinking', 'info': 'Whether or not to enable thinking mode for reasoning models.'},
    },
    "report_to": {
        "en": {
            "label": "Enable external logger",
            "info": "Use TensorBoard or wandb to log experiment.",
        },
        "ru": {
            "label": "Включить внешний регистратор",
            "info": "Использовать TensorBoard или wandb для ведения журнала экспериментов.",
        },
        "zh": {'label': 'Enable external logger', 'info': 'Use TensorBoard or wandb to log experiment.'},
        "ko": {
            "label": "외부 logger 활성화",
            "info": "TensorBoard 또는 wandb를 사용하여 실험을 기록합니다.",
        },
        "ja": {'label': 'Enable external logger', 'info': 'Use TensorBoard or wandb to log experiment.'},
    },
    "freeze_tab": {
        "en": {
            "label": "Freeze tuning configurations",
        },
        "ru": {
            "label": "конфигурации для настройки заморозки",
        },
        "zh": {'label': 'Freeze tuning configurations'},
        "ko": {
            "label": "Freeze tuning 설정",
        },
        "ja": {'label': 'Freeze tuning configurations'},
    },
    "freeze_trainable_layers": {
        "en": {
            "label": "Trainable layers",
            "info": "Number of the last(+)/first(-) hidden layers to be set as trainable.",
        },
        "ru": {
            "label": "Обучаемые слои",
            "info": "Количество последних (+)/первых (-) скрытых слоев, которые будут установлены как обучаемые.",
        },
        "zh": {'label': 'Trainable layers', 'info': 'Number of the last(+)/first(-) hidden layers to be set as trainable.'},
        "ko": {
            "label": "학습 가능한 레이어",
            "info": "학습 가능하게 설정할 마지막(+)/처음(-) 히든 레이어의 수.",
        },
        "ja": {'label': 'Trainable layers', 'info': 'Number of the last(+)/first(-) hidden layers to be set as trainable.'},
    },
    "freeze_trainable_modules": {
        "en": {
            "label": "Trainable modules",
            "info": "Name(s) of trainable modules. Use commas to separate multiple modules.",
        },
        "ru": {
            "label": "Обучаемые модули",
            "info": "Название обучаемых модулей. Используйте запятые для разделения нескольких модулей.",
        },
        "zh": {'label': 'Trainable modules', 'info': 'Name(s) of trainable modules. Use commas to separate multiple modules.'},
        "ko": {
            "label": "학습 가능한 모듈",
            "info": "학습 가능한 모듈의 이름. 여러 모듈을 구분하려면 쉼표(,)를 사용하세요.",
        },
        "ja": {'label': 'Trainable modules', 'info': 'Name(s) of trainable modules. Use commas to separate multiple modules.'},
    },
    "freeze_extra_modules": {
        "en": {
            "label": "Extra modules (optional)",
            "info": (
                "Name(s) of modules apart from hidden layers to be set as trainable. "
                "Use commas to separate multiple modules."
            ),
        },
        "ru": {
            "label": "Дополнительные модули (опционально)",
            "info": (
                "Имена модулей, кроме скрытых слоев, которые следует установить в качестве обучаемых. "
                "Используйте запятые для разделения нескольких модулей."
            ),
        },
        "zh": {'label': 'Extra modules (optional)', 'info': 'Name(s) of modules apart from hidden layers to be set as trainable. Use commas to separate multiple modules.'},
        "ko": {
            "label": "추가 모듈 (선택 사항)",
            "info": "히든 레이어 외에 학습 가능하게 설정할 모듈의 이름. 모듈 간에는 쉼표(,)로 구분하십시오.",
        },
        "ja": {'label': 'Extra modules (optional)', 'info': 'Name(s) of modules apart from hidden layers to be set as trainable. Use commas to separate multiple modules.'},
    },
    "lora_tab": {
        "en": {
            "label": "LoRA configurations",
        },
        "ru": {
            "label": "Конфигурации LoRA",
        },
        "zh": {'label': 'LoRA configurations'},
        "ko": {
            "label": "LoRA 구성",
        },
        "ja": {'label': 'LoRA configurations'},
    },
    "lora_rank": {
        "en": {
            "label": "LoRA rank",
            "info": "The rank of LoRA matrices.",
        },
        "ru": {
            "label": "Ранг матриц LoRA",
            "info": "Ранг матриц LoRA.",
        },
        "zh": {'label': 'LoRA rank', 'info': 'The rank of LoRA matrices.'},
        "ko": {
            "label": "LoRA 랭크",
            "info": "LoRA 행렬의 랭크.",
        },
        "ja": {'label': 'LoRA rank', 'info': 'The rank of LoRA matrices.'},
    },
    "lora_alpha": {
        "en": {
            "label": "LoRA alpha",
            "info": "Lora scaling coefficient.",
        },
        "ru": {
            "label": "LoRA alpha",
            "info": "Коэффициент масштабирования LoRA.",
        },
        "zh": {'label': 'LoRA alpha', 'info': 'Lora scaling coefficient.'},
        "ko": {
            "label": "LoRA 알파",
            "info": "LoRA 스케일링 계수.",
        },
        "ja": {'label': 'LoRA alpha', 'info': 'Lora scaling coefficient.'},
    },
    "lora_dropout": {
        "en": {
            "label": "LoRA dropout",
            "info": "Dropout ratio of LoRA weights.",
        },
        "ru": {
            "label": "Вероятность отсева LoRA",
            "info": "Вероятность отсева весов LoRA.",
        },
        "zh": {'label': 'LoRA dropout', 'info': 'Dropout ratio of LoRA weights.'},
        "ko": {
            "label": "LoRA 드롭아웃",
            "info": "LoRA 가중치의 드롭아웃 비율.",
        },
        "ja": {'label': 'LoRA dropout', 'info': 'Dropout ratio of LoRA weights.'},
    },
    "loraplus_lr_ratio": {
        "en": {
            "label": "LoRA+ LR ratio",
            "info": "The LR ratio of the B matrices in LoRA.",
        },
        "ru": {
            "label": "LoRA+ LR коэффициент",
            "info": "Коэффициент LR матриц B в LoRA.",
        },
        "zh": {'label': 'LoRA+ LR ratio', 'info': 'The LR ratio of the B matrices in LoRA.'},
        "ko": {
            "label": "LoRA+ LR 비율",
            "info": "LoRA에서 B 행렬의 LR 비율.",
        },
        "ja": {'label': 'LoRA+ LR ratio', 'info': 'The LR ratio of the B matrices in LoRA.'},
    },
    "create_new_adapter": {
        "en": {
            "label": "Create new adapter",
            "info": "Create a new adapter with randomly initialized weight upon the existing one.",
        },
        "ru": {
            "label": "Создать новый адаптер",
            "info": "Создать новый адаптер с случайной инициализацией веса на основе существующего.",
        },
        "zh": {'label': 'Create new adapter', 'info': 'Create a new adapter with randomly initialized weight upon the existing one.'},
        "ko": {
            "label": "새 어댑터 생성",
            "info": "기존 어댑터 위에 무작위로 초기화된 가중치를 가진 새 어댑터를 생성합니다.",
        },
        "ja": {'label': 'Create new adapter', 'info': 'Create a new adapter with randomly initialized weight upon the existing one.'},
    },
    "use_rslora": {
        "en": {
            "label": "Use rslora",
            "info": "Use the rank stabilization scaling factor for LoRA layer.",
        },
        "ru": {
            "label": "Использовать rslora",
            "info": "Использовать коэффициент масштабирования стабилизации ранга для слоя LoRA.",
        },
        "zh": {'label': 'Use rslora', 'info': 'Use the rank stabilization scaling factor for LoRA layer.'},
        "ko": {
            "label": "rslora 사용",
            "info": "LoRA 레이어에 랭크 안정화 스케일링 계수를 사용합니다.",
        },
        "ja": {'label': 'Use rslora', 'info': 'Use the rank stabilization scaling factor for LoRA layer.'},
    },
    "use_dora": {
        "en": {
            "label": "Use DoRA",
            "info": "Use weight-decomposed LoRA.",
        },
        "ru": {
            "label": "Используйте DoRA",
            "info": "Используйте LoRA с декомпозицией весов.",
        },
        "zh": {'label': 'Use DoRA', 'info': 'Use weight-decomposed LoRA.'},
        "ko": {
            "label": "DoRA 사용",
            "info": "가중치-분해 LoRA를 사용합니다.",
        },
        "ja": {'label': 'Use DoRA', 'info': 'Use weight-decomposed LoRA.'},
    },
    "use_pissa": {
        "en": {
            "label": "Use PiSSA",
            "info": "Use PiSSA method.",
        },
        "ru": {
            "label": "используйте PiSSA",
            "info": "Используйте метод PiSSA.",
        },
        "zh": {'label': 'Use PiSSA', 'info': 'Use PiSSA method.'},
        "ko": {
            "label": "PiSSA 사용",
            "info": "PiSSA 방법을 사용합니다.",
        },
        "ja": {'label': 'Use PiSSA', 'info': 'Use PiSSA method.'},
    },
    "lora_target": {
        "en": {
            "label": "LoRA modules (optional)",
            "info": "Name(s) of modules to apply LoRA. Use commas to separate multiple modules.",
        },
        "ru": {
            "label": "Модули LoRA (опционально)",
            "info": "Имена модулей для применения LoRA. Используйте запятые для разделения нескольких модулей.",
        },
        "zh": {'label': 'LoRA modules (optional)', 'info': 'Name(s) of modules to apply LoRA. Use commas to separate multiple modules.'},
        "ko": {
            "label": "LoRA 모듈 (선택 사항)",
            "info": "LoRA를 적용할 모듈의 이름. 모듈 간에는 쉼표(,)로 구분하십시오.",
        },
        "ja": {'label': 'LoRA modules (optional)', 'info': 'Name(s) of modules to apply LoRA. Use commas to separate multiple modules.'},
    },
    "additional_target": {
        "en": {
            "label": "Additional modules (optional)",
            "info": (
                "Name(s) of modules apart from LoRA layers to be set as trainable. "
                "Use commas to separate multiple modules."
            ),
        },
        "ru": {
            "label": "Дополнительные модули (опционально)",
            "info": (
                "Имена модулей, кроме слоев LoRA, которые следует установить в качестве обучаемых. "
                "Используйте запятые для разделения нескольких модулей."
            ),
        },
        "zh": {'label': 'Additional modules (optional)', 'info': 'Name(s) of modules apart from LoRA layers to be set as trainable. Use commas to separate multiple modules.'},
        "ko": {
            "label": "추가 모듈 (선택 사항)",
            "info": "LoRA 레이어 외에 학습 가능하게 설정할 모듈의 이름. 모듈 간에는 쉼표(,)로 구분하십시오.",
        },
        "ja": {'label': 'Additional modules (optional)', 'info': 'Name(s) of modules apart from LoRA layers to be set as trainable. Use commas to separate multiple modules.'},
    },
    "rlhf_tab": {
        "en": {
            "label": "RLHF configurations",
        },
        "ru": {
            "label": "Конфигурации RLHF",
        },
        "zh": {'label': 'RLHF configurations'},
        "ko": {
            "label": "RLHF 구성",
        },
        "ja": {'label': 'RLHF configurations'},
    },
    "pref_beta": {
        "en": {
            "label": "Beta value",
            "info": "Value of the beta parameter in the loss.",
        },
        "ru": {
            "label": "Бета значение",
            "info": "Значение параметра бета в функции потерь.",
        },
        "zh": {'label': 'Beta value', 'info': 'Value of the beta parameter in the loss.'},
        "ko": {
            "label": "베타 값",
            "info": "손실 함수에서 베타 매개 변수의 값.",
        },
        "ja": {'label': 'Beta value', 'info': 'Value of the beta parameter in the loss.'},
    },
    "pref_ftx": {
        "en": {
            "label": "Ftx gamma",
            "info": "The weight of SFT loss in the final loss.",
        },
        "ru": {
            "label": "Ftx гамма",
            "info": "Вес потери SFT в итоговой потере.",
        },
        "zh": {'label': 'Ftx gamma', 'info': 'The weight of SFT loss in the final loss.'},
        "ko": {
            "label": "Ftx 감마",
            "info": "최종 로스 함수에서 SFT 로스의 가중치.",
        },
        "ja": {'label': 'Ftx gamma', 'info': 'The weight of SFT loss in the final loss.'},
    },
    "pref_loss": {
        "en": {
            "label": "Loss type",
            "info": "The type of the loss function.",
        },
        "ru": {
            "label": "Тип потерь",
            "info": "Тип функции потерь.",
        },
        "zh": {'label': 'Loss type', 'info': 'The type of the loss function.'},
        "ko": {
            "label": "로스 유형",
            "info": "로스 함수의 유형.",
        },
        "ja": {'label': 'Loss type', 'info': 'The type of the loss function.'},
    },
    "reward_model": {
        "en": {
            "label": "Reward model",
            "info": "Adapter of the reward model in PPO training.",
        },
        "ru": {
            "label": "Модель вознаграждения",
            "info": "Адаптер модели вознаграждения для обучения PPO.",
        },
        "zh": {'label': 'Reward model', 'info': 'Adapter of the reward model in PPO training.'},
        "ko": {
            "label": "리워드 모델",
            "info": "PPO 학습에서 사용할 리워드 모델의 어댑터.",
        },
        "ja": {'label': 'Reward model', 'info': 'Adapter of the reward model in PPO training.'},
    },
    "ppo_score_norm": {
        "en": {
            "label": "Score norm",
            "info": "Normalizing scores in PPO training.",
        },
        "ru": {
            "label": "Норма оценок",
            "info": "Нормализация оценок в тренировке PPO.",
        },
        "zh": {'label': 'Score norm', 'info': 'Normalizing scores in PPO training.'},
        "ko": {
            "label": "스코어 정규화",
            "info": "PPO 학습에서 스코어를 정규화합니다.",
        },
        "ja": {'label': 'Score norm', 'info': 'Normalizing scores in PPO training.'},
    },
    "ppo_whiten_rewards": {
        "en": {
            "label": "Whiten rewards",
            "info": "Whiten the rewards in PPO training.",
        },
        "ru": {
            "label": "Белые вознаграждения",
            "info": "Осветлите вознаграждения в обучении PPO.",
        },
        "zh": {'label': 'Whiten rewards', 'info': 'Whiten the rewards in PPO training.'},
        "ko": {
            "label": "보상 백화",
            "info": "PPO 훈련에서 보상을 백화(Whiten)합니다.",
        },
        "ja": {'label': 'Whiten rewards', 'info': 'Whiten the rewards in PPO training.'},
    },
    "mm_tab": {
        "en": {
            "label": "Multimodal configurations",
        },
        "ru": {
            "label": "Конфигурации мультимедиа",
        },
        "zh": {'label': 'Multimodal configurations'},
        "ko": {
            "label": "멀티모달 구성",
        },
        "ja": {'label': 'Multimodal configurations'},
    },
    "freeze_vision_tower": {
        "en": {
            "label": "Freeze vision tower",
            "info": "Freeze the vision tower in the model.",
        },
        "ru": {
            "label": "Заморозить башню визиона",
            "info": "Заморозить башню визиона в модели.",
        },
        "zh": {'label': 'Freeze vision tower', 'info': 'Freeze the vision tower in the model.'},
        "ko": {
            "label": "비전 타워 고정",
            "info": "모델의 비전 타워를 고정합니다.",
        },
        "ja": {'label': 'Freeze vision tower', 'info': 'Freeze the vision tower in the model.'},
    },
    "freeze_multi_modal_projector": {
        "en": {
            "label": "Freeze multi-modal projector",
            "info": "Freeze the multi-modal projector in the model.",
        },
        "ru": {
            "label": "Заморозить мультимодальный проектор",
            "info": "Заморозить мультимодальный проектор в модели.",
        },
        "zh": {'label': 'Freeze multi-modal projector', 'info': 'Freeze the multi-modal projector in the model.'},
        "ko": {
            "label": "멀티모달 프로젝터 고정",
            "info": "모델의 멀티모달 프로젝터를 고정합니다.",
        },
        "ja": {'label': 'Freeze multi-modal projector', 'info': 'Freeze the multi-modal projector in the model.'},
    },
    "freeze_language_model": {
        "en": {
            "label": "Freeze language model",
            "info": "Freeze the language model in the model.",
        },
        "ru": {
            "label": "Заморозить язык модели",
            "info": "Заморозить язык модели в модели.",
        },
        "zh": {'label': 'Freeze language model', 'info': 'Freeze the language model in the model.'},
        "ko": {
            "label": "언어 모델 고정",
            "info": "모델의 언어 모델을 고정합니다.",
        },
        "ja": {'label': 'Freeze language model', 'info': 'Freeze the language model in the model.'},
    },
    "image_max_pixels": {
        "en": {
            "label": "Image max pixels",
            "info": "The maximum number of pixels of image inputs.",
        },
        "ru": {
            "label": "Максимальное количество пикселей изображения",
            "info": "Максимальное количество пикселей изображения.",
        },
        "zh": {'label': 'Image max pixels', 'info': 'The maximum number of pixels of image inputs.'},
        "ko": {
            "label": "이미지 최대 픽셀",
            "info": "이미지 입력의 최대 픽셀 수입니다.",
        },
        "ja": {'label': 'Image max pixels', 'info': 'The maximum number of pixels of image inputs.'},
    },
    "image_min_pixels": {
        "en": {
            "label": "Image min pixels",
            "info": "The minimum number of pixels of image inputs.",
        },
        "ru": {
            "label": "Минимальное количество пикселей изображения",
            "info": "Минимальное количество пикселей изображения.",
        },
        "zh": {'label': 'Image min pixels', 'info': 'The minimum number of pixels of image inputs.'},
        "ko": {
            "label": "이미지 최소 픽셀",
            "info": "이미지 입력의 최소 픽셀 수입니다.",
        },
        "ja": {'label': 'Image min pixels', 'info': 'The minimum number of pixels of image inputs.'},
    },
    "video_max_pixels": {
        "en": {
            "label": "Video max pixels",
            "info": "The maximum number of pixels of video inputs.",
        },
        "ru": {
            "label": "Максимальное количество пикселей видео",
            "info": "Максимальное количество пикселей видео.",
        },
        "zh": {'label': 'Video max pixels', 'info': 'The maximum number of pixels of video inputs.'},
        "ko": {
            "label": "비디오 최대 픽셀",
            "info": "비디오 입력의 최대 픽셀 수입니다.",
        },
        "ja": {'label': 'Video max pixels', 'info': 'The maximum number of pixels of video inputs.'},
    },
    "video_min_pixels": {
        "en": {
            "label": "Video min pixels",
            "info": "The minimum number of pixels of video inputs.",
        },
        "ru": {
            "label": "Минимальное количество пикселей видео",
            "info": "Минимальное количество пикселей видео.",
        },
        "zh": {'label': 'Video min pixels', 'info': 'The minimum number of pixels of video inputs.'},
        "ko": {
            "label": "비디오 최소 픽셀",
            "info": "비디오 입력의 최소 픽셀 수입니다.",
        },
        "ja": {'label': 'Video min pixels', 'info': 'The minimum number of pixels of video inputs.'},
    },
    "galore_tab": {
        "en": {
            "label": "GaLore configurations",
        },
        "ru": {
            "label": "Конфигурации GaLore",
        },
        "zh": {'label': 'GaLore configurations'},
        "ko": {
            "label": "GaLore 구성",
        },
        "ja": {'label': 'GaLore configurations'},
    },
    "use_galore": {
        "en": {
            "label": "Use GaLore",
            "info": "Use [GaLore](https://github.com/jiaweizzhao/GaLore) optimizer.",
        },
        "ru": {
            "label": "Использовать GaLore",
            "info": "Используйте оптимизатор [GaLore](https://github.com/jiaweizzhao/GaLore).",
        },
        "zh": {'label': 'Use GaLore', 'info': 'Use [GaLore](https://github.com/jiaweizzhao/GaLore) optimizer.'},
        "ko": {
            "label": "GaLore 사용",
            "info": "[GaLore](https://github.com/jiaweizzhao/GaLore) 최적화를 사용하세요.",
        },
        "ja": {'label': 'Use GaLore', 'info': 'Use [GaLore](https://github.com/jiaweizzhao/GaLore) optimizer.'},
    },
    "galore_rank": {
        "en": {
            "label": "GaLore rank",
            "info": "The rank of GaLore gradients.",
        },
        "ru": {
            "label": "Ранг GaLore",
            "info": "Ранг градиентов GaLore.",
        },
        "zh": {'label': 'GaLore rank', 'info': 'The rank of GaLore gradients.'},
        "ko": {
            "label": "GaLore 랭크",
            "info": "GaLore 그레디언트의 랭크.",
        },
        "ja": {'label': 'GaLore rank', 'info': 'The rank of GaLore gradients.'},
    },
    "galore_update_interval": {
        "en": {
            "label": "Update interval",
            "info": "Number of steps to update the GaLore projection.",
        },
        "ru": {
            "label": "Интервал обновления",
            "info": "Количество шагов для обновления проекции GaLore.",
        },
        "zh": {'label': 'Update interval', 'info': 'Number of steps to update the GaLore projection.'},
        "ko": {
            "label": "업데이트 간격",
            "info": "GaLore 프로젝션을 업데이트할 간격의 스텝 수.",
        },
        "ja": {'label': 'Update interval', 'info': 'Number of steps to update the GaLore projection.'},
    },
    "galore_scale": {
        "en": {
            "label": "GaLore scale",
            "info": "GaLore scaling coefficient.",
        },
        "ru": {
            "label": "LoRA Alpha",
            "info": "Коэффициент масштабирования GaLore.",
        },
        "zh": {'label': 'GaLore scale', 'info': 'GaLore scaling coefficient.'},
        "ko": {
            "label": "GaLore 스케일",
            "info": "GaLore 스케일링 계수.",
        },
        "ja": {'label': 'GaLore scale', 'info': 'GaLore scaling coefficient.'},
    },
    "galore_target": {
        "en": {
            "label": "GaLore modules",
            "info": "Name(s) of modules to apply GaLore. Use commas to separate multiple modules.",
        },
        "ru": {
            "label": "Модули GaLore",
            "info": "Имена модулей для применения GaLore. Используйте запятые для разделения нескольких модулей.",
        },
        "zh": {'label': 'GaLore modules', 'info': 'Name(s) of modules to apply GaLore. Use commas to separate multiple modules.'},
        "ko": {
            "label": "GaLore 모듈",
            "info": "GaLore를 적용할 모듈의 이름. 모듈 간에는 쉼표(,)로 구분하십시오.",
        },
        "ja": {'label': 'GaLore modules', 'info': 'Name(s) of modules to apply GaLore. Use commas to separate multiple modules.'},
    },
    "apollo_tab": {
        "en": {
            "label": "APOLLO configurations",
        },
        "ru": {
            "label": "Конфигурации APOLLO",
        },
        "zh": {'label': 'APOLLO configurations'},
        "ko": {
            "label": "APOLLO 구성",
        },
        "ja": {'label': 'APOLLO configurations'},
    },
    "use_apollo": {
        "en": {
            "label": "Use APOLLO",
            "info": "Use [APOLLO](https://github.com/zhuhanqing/APOLLO) optimizer.",
        },
        "ru": {
            "label": "Использовать APOLLO",
            "info": "Используйте оптимизатор [APOLLO](https://github.com/zhuhanqing/APOLLO).",
        },
        "zh": {'label': 'Use APOLLO', 'info': 'Use [APOLLO](https://github.com/zhuhanqing/APOLLO) optimizer.'},
        "ko": {
            "label": "APOLLO 사용",
            "info": "[APOLLO](https://github.com/zhuhanqing/APOLLO) 최적화를 사용하세요.",
        },
        "ja": {'label': 'Use APOLLO', 'info': 'Use [APOLLO](https://github.com/zhuhanqing/APOLLO) optimizer.'},
    },
    "apollo_rank": {
        "en": {
            "label": "APOLLO rank",
            "info": "The rank of APOLLO gradients.",
        },
        "ru": {
            "label": "Ранг APOLLO",
            "info": "Ранг градиентов APOLLO.",
        },
        "zh": {'label': 'APOLLO rank', 'info': 'The rank of APOLLO gradients.'},
        "ko": {
            "label": "APOLLO 랭크",
            "info": "APOLLO 그레디언트의 랭크.",
        },
        "ja": {'label': 'APOLLO rank', 'info': 'The rank of APOLLO gradients.'},
    },
    "apollo_update_interval": {
        "en": {
            "label": "Update interval",
            "info": "Number of steps to update the APOLLO projection.",
        },
        "ru": {
            "label": "Интервал обновления",
            "info": "Количество шагов для обновления проекции APOLLO.",
        },
        "zh": {'label': 'Update interval', 'info': 'Number of steps to update the APOLLO projection.'},
        "ko": {
            "label": "업데이트 간격",
            "info": "APOLLO 프로젝션을 업데이트할 간격의 스텝 수.",
        },
        "ja": {'label': 'Update interval', 'info': 'Number of steps to update the APOLLO projection.'},
    },
    "apollo_scale": {
        "en": {
            "label": "APOLLO scale",
            "info": "APOLLO scaling coefficient.",
        },
        "ru": {
            "label": "LoRA Alpha",
            "info": "Коэффициент масштабирования APOLLO.",
        },
        "zh": {'label': 'APOLLO scale', 'info': 'APOLLO scaling coefficient.'},
        "ko": {
            "label": "APOLLO 스케일",
            "info": "APOLLO 스케일링 계수.",
        },
        "ja": {'label': 'APOLLO scale', 'info': 'APOLLO scaling coefficient.'},
    },
    "apollo_target": {
        "en": {
            "label": "APOLLO modules",
            "info": "Name(s) of modules to apply APOLLO. Use commas to separate multiple modules.",
        },
        "ru": {
            "label": "Модули APOLLO",
            "info": "Имена модулей для применения APOLLO. Используйте запятые для разделения нескольких модулей.",
        },
        "zh": {'label': 'APOLLO modules', 'info': 'Name(s) of modules to apply APOLLO. Use commas to separate multiple modules.'},
        "ko": {
            "label": "APOLLO 모듈",
            "info": "APOLLO를 적용할 모듈의 이름. 모듈 간에는 쉼표(,)로 구분하십시오.",
        },
        "ja": {'label': 'APOLLO modules', 'info': 'Name(s) of modules to apply APOLLO. Use commas to separate multiple modules.'},
    },
    "badam_tab": {
        "en": {
            "label": "BAdam configurations",
        },
        "ru": {
            "label": "Конфигурации BAdam",
        },
        "zh": {'label': 'BAdam configurations'},
        "ko": {
            "label": "BAdam 설정",
        },
        "ja": {'label': 'BAdam configurations'},
    },
    "use_badam": {
        "en": {
            "label": "Use BAdam",
            "info": "Enable the [BAdam](https://github.com/Ledzy/BAdam) optimizer.",
        },
        "ru": {
            "label": "Использовать BAdam",
            "info": "Включите оптимизатор [BAdam](https://github.com/Ledzy/BAdam).",
        },
        "zh": {'label': 'Use BAdam', 'info': 'Enable the [BAdam](https://github.com/Ledzy/BAdam) optimizer.'},
        "ko": {
            "label": "BAdam 사용",
            "info": "[BAdam](https://github.com/Ledzy/BAdam) 옵티마이저를 사용합니다.",
        },
        "ja": {'label': 'Use BAdam', 'info': 'Enable the [BAdam](https://github.com/Ledzy/BAdam) optimizer.'},
    },
    "badam_mode": {
        "en": {
            "label": "BAdam mode",
            "info": "Whether to use layer-wise or ratio-wise BAdam optimizer.",
        },
        "ru": {
            "label": "Режим BAdam",
            "info": "Использовать ли оптимизатор BAdam с послоевой или пропорциональной настройкой.",
        },
        "zh": {'label': 'BAdam mode', 'info': 'Whether to use layer-wise or ratio-wise BAdam optimizer.'},
        "ko": {
            "label": "BAdam 모드",
            "info": "레이어-BAdam 옵티마이저인지 비율-BAdam 옵티마이저인지.",
        },
        "ja": {'label': 'BAdam mode', 'info': 'Whether to use layer-wise or ratio-wise BAdam optimizer.'},
    },
    "badam_switch_mode": {
        "en": {
            "label": "Switch mode",
            "info": "The strategy of picking block to update for layer-wise BAdam.",
        },
        "ru": {
            "label": "Режим переключения",
            "info": "Стратегия выбора блока для обновления для послойного BAdam.",
        },
        "zh": {'label': 'Switch mode', 'info': 'The strategy of picking block to update for layer-wise BAdam.'},
        "ko": {
            "label": "스위치 모드",
            "info": "레이어-BAdam을 위한 블록 선택 전략.",
        },
        "ja": {'label': 'Switch mode', 'info': 'The strategy of picking block to update for layer-wise BAdam.'},
    },
    "badam_switch_interval": {
        "en": {
            "label": "Switch interval",
            "info": "Number of steps to update the block for layer-wise BAdam.",
        },
        "ru": {
            "label": "Интервал переключения",
            "info": "количество шагов для обновления блока для пошагового BAdam.",
        },
        "zh": {'label': 'Switch interval', 'info': 'Number of steps to update the block for layer-wise BAdam.'},
        "ko": {
            "label": "전환 간격",
            "info": "레이어-BAdam을 위한 블록 업데이트 간 스텝 수.",
        },
        "ja": {'label': 'Switch interval', 'info': 'Number of steps to update the block for layer-wise BAdam.'},
    },
    "badam_update_ratio": {
        "en": {
            "label": "Update ratio",
            "info": "The ratio of the update for ratio-wise BAdam.",
        },
        "ru": {
            "label": "Коэффициент обновления",
            "info": "Коэффициент обновления для BAdam с учётом соотношений.",
        },
        "zh": {'label': 'Update ratio', 'info': 'The ratio of the update for ratio-wise BAdam.'},
        "ko": {
            "label": "업데이트 비율",
            "info": "비율-BAdam의 업데이트 비율.",
        },
        "ja": {'label': 'Update ratio', 'info': 'The ratio of the update for ratio-wise BAdam.'},
    },
    "swanlab_tab": {
        "en": {
            "label": "SwanLab configurations",
        },
        "ru": {
            "label": "Конфигурации SwanLab",
        },
        "zh": {'label': 'SwanLab configurations'},
        "ko": {
            "label": "SwanLab 설정",
        },
        "ja": {'label': 'SwanLab configurations'},
    },
    "use_swanlab": {
        "en": {
            "label": "Use SwanLab",
            "info": "Enable [SwanLab](https://swanlab.cn/) for experiment tracking and visualization.",
        },
        "ru": {
            "label": "Использовать SwanLab",
            "info": "Включить [SwanLab](https://swanlab.cn/) для отслеживания и визуализации экспериментов.",
        },
        "zh": {'label': 'Use SwanLab', 'info': 'Enable [SwanLab](https://swanlab.cn/) for experiment tracking and visualization.'},
        "ko": {
            "label": "SwanLab 사용",
            "info": "[SwanLab](https://swanlab.cn/) 를 사용하여 실험을 추적하고 시각화합니다.",
        },
        "ja": {'label': 'Use SwanLab', 'info': 'Enable [SwanLab](https://swanlab.cn/) for experiment tracking and visualization.'},
    },
    "swanlab_project": {
        "en": {
            "label": "SwanLab project",
        },
        "ru": {
            "label": "SwanLab Проект",
        },
        "zh": {'label': 'SwanLab project'},
        "ko": {
            "label": "SwanLab 프로젝트",
        },
        "ja": {
            "label": "SwanLab プロジェクト",
        },
    },
    "swanlab_run_name": {
        "en": {
            "label": "SwanLab experiment name (optional)",
        },
        "ru": {
            "label": "SwanLab Имя эксперимента (опционально)",
        },
        "zh": {'label': 'SwanLab experiment name (optional)'},
        "ko": {
            "label": "SwanLab 실험 이름 (선택 사항)",
        },
        "ja": {'label': 'SwanLab experiment name (optional)'},
    },
    "swanlab_workspace": {
        "en": {
            "label": "SwanLab workspace (optional)",
            "info": "Workspace for SwanLab. Defaults to the personal workspace.",
        },
        "ru": {
            "label": "SwanLab Рабочая область (опционально)",
            "info": "Рабочая область SwanLab, если не заполнено, то по умолчанию в личной рабочей области.",
        },
        "zh": {'label': 'SwanLab workspace (optional)', 'info': 'Workspace for SwanLab. Defaults to the personal workspace.'},
        "ko": {
            "label": "SwanLab 작업 영역 (선택 사항)",
            "info": "SwanLab 조직의 작업 영역, 비어 있으면 기본적으로 개인 작업 영역에 있습니다.",
        },
        "ja": {'label': 'SwanLab workspace (optional)', 'info': 'Workspace for SwanLab. Defaults to the personal workspace.'},
    },
    "swanlab_api_key": {
        "en": {
            "label": "SwanLab API key (optional)",
            "info": "API key for SwanLab.",
        },
        "ru": {
            "label": "SwanLab API ключ (опционально)",
            "info": "API ключ для SwanLab.",
        },
        "zh": {'label': 'SwanLab API key (optional)', 'info': 'API key for SwanLab.'},
        "ko": {
            "label": "SwanLab API 키 (선택 사항)",
            "info": "SwanLab의 API 키.",
        },
        "ja": {
            "label": "SwanLab API キー（オプション）",
            "info": "SwanLab の API キー。",
        },
    },
    "swanlab_mode": {
        "en": {
            "label": "SwanLab mode",
            "info": "Cloud or offline version.",
        },
        "ru": {
            "label": "SwanLab Режим",
            "info": "Версия в облаке или локальная версия.",
        },
        "zh": {'label': 'SwanLab mode', 'info': 'Cloud or offline version.'},
        "ko": {
            "label": "SwanLab 모드",
            "info": "클라우드 버전 또는 오프라인 버전.",
        },
        "ja": {'label': 'SwanLab mode', 'info': 'Cloud or offline version.'},
    },
    "swanlab_logdir": {
        "en": {
            "label": "SwanLab log directory",
            "info": "The log directory for SwanLab.",
        },
        "ru": {
            "label": "SwanLab 로그 디렉토리",
            "info": "SwanLab의 로그 디렉토리.",
        },
        "zh": {'label': 'SwanLab log directory', 'info': 'The log directory for SwanLab.'},
        "ko": {
            "label": "SwanLab 로그 디렉토리",
            "info": "SwanLab의 로그 디렉토리.",
        },
        "ja": {
            "label": "SwanLab ログ ディレクトリ",
            "info": "SwanLab のログ ディレクトリ。",
        },
    },
    "cmd_preview_btn": {
        "en": {
            "value": "Preview command",
        },
        "ru": {
            "value": "Просмотр команды",
        },
        "zh": {'value': 'Preview command'},
        "ko": {
            "value": "명령어 미리보기",
        },
        "ja": {
            "value": "コマンドをプレビュー",
        },
    },
    "arg_save_btn": {
        "en": {
            "value": "Save arguments",
        },
        "ru": {
            "value": "Сохранить аргументы",
        },
        "zh": {'value': 'Save arguments'},
        "ko": {
            "value": "Argument 저장",
        },
        "ja": {'value': 'Save arguments'},
    },
    "arg_load_btn": {
        "en": {
            "value": "Load arguments",
        },
        "ru": {
            "value": "Загрузить аргументы",
        },
        "zh": {'value': 'Load arguments'},
        "ko": {
            "value": "Argument 불러오기",
        },
        "ja": {'value': 'Load arguments'},
    },
    "start_btn": {
        "en": {
            "value": "Start",
        },
        "ru": {
            "value": "Начать",
        },
        "zh": {'value': 'Start'},
        "ko": {
            "value": "시작",
        },
        "ja": {'value': 'Start'},
    },
    "stop_btn": {
        "en": {
            "value": "Abort",
        },
        "ru": {
            "value": "Прервать",
        },
        "zh": {'value': 'Abort'},
        "ko": {
            "value": "중단",
        },
        "ja": {'value': 'Abort'},
    },
    "output_dir": {
        "en": {
            "label": "Output dir",
            "info": "Directory for saving results.",
        },
        "ru": {
            "label": "Выходной каталог",
            "info": "Каталог для сохранения результатов.",
        },
        "zh": {'label': 'Output dir', 'info': 'Directory for saving results.'},
        "ko": {
            "label": "출력 디렉토리",
            "info": "결과를 저장할 디렉토리.",
        },
        "ja": {'label': 'Output dir', 'info': 'Directory for saving results.'},
    },
    "config_path": {
        "en": {
            "label": "Config path",
            "info": "Path to config saving arguments.",
        },
        "ru": {
            "label": "Путь к конфигурации",
            "info": "Путь для сохранения аргументов конфигурации.",
        },
        "zh": {'label': 'Config path', 'info': 'Path to config saving arguments.'},
        "ko": {
            "label": "설정 경로",
            "info": "Arguments 저장 파일 경로.",
        },
        "ja": {'label': 'Config path', 'info': 'Path to config saving arguments.'},
    },
    "device_count": {
        "en": {
            "label": "Device count",
            "info": "Number of devices available.",
        },
        "ru": {
            "label": "Количество устройств",
            "info": "Количество доступных устройств.",
        },
        "zh": {'label': 'Device count', 'info': 'Number of devices available.'},
        "ko": {
            "label": "디바이스 수",
            "info": "사용 가능한 디바이스 수.",
        },
        "ja": {'label': 'Device count', 'info': 'Number of devices available.'},
    },
    "ds_stage": {
        "en": {
            "label": "DeepSpeed stage",
            "info": "DeepSpeed stage for distributed training.",
        },
        "ru": {
            "label": "Этап DeepSpeed",
            "info": "Этап DeepSpeed для распределенного обучения.",
        },
        "zh": {'label': 'DeepSpeed stage', 'info': 'DeepSpeed stage for distributed training.'},
        "ko": {
            "label": "DeepSpeed 단계",
            "info": "분산 학습을 위한 DeepSpeed 단계.",
        },
        "ja": {
            "label": "DeepSpeed stage",
            "info": "マルチ GPU トレーニングの DeepSpeed stage。",
        },
    },
    "ds_offload": {
        "en": {
            "label": "Enable offload",
            "info": "Enable DeepSpeed offload (slow down training).",
        },
        "ru": {
            "label": "Включить выгрузку",
            "info": "включить выгрузку DeepSpeed (замедлит обучение).",
        },
        "zh": {'label': 'Enable offload', 'info': 'Enable DeepSpeed offload (slow down training).'},
        "ko": {
            "label": "오프로딩 활성화",
            "info": "DeepSpeed 오프로딩 활성화 (훈련 속도 느려짐).",
        },
        "ja": {'label': 'Enable offload', 'info': 'Enable DeepSpeed offload (slow down training).'},
    },
    "output_box": {
        "en": {
            "value": "Ready.",
        },
        "ru": {
            "value": "Готово.",
        },
        "zh": {'value': 'Ready.'},
        "ko": {
            "value": "준비 완료.",
        },
        "ja": {'value': 'Ready.'},
    },
    "loss_viewer": {
        "en": {
            "label": "Loss",
        },
        "ru": {
            "label": "Потери",
        },
        "zh": {'label': 'Loss'},
        "ko": {
            "label": "손실",
        },
        "ja": {'label': 'Loss'},
    },
    "predict": {
        "en": {
            "label": "Save predictions",
        },
        "ru": {
            "label": "Сохранить предсказания",
        },
        "zh": {'label': 'Save predictions'},
        "ko": {
            "label": "예측 결과 저장",
        },
        "ja": {'label': 'Save predictions'},
    },
    "infer_backend": {
        "en": {
            "label": "Inference engine",
        },
        "ru": {
            "label": "Инференс движок",
        },
        "zh": {'label': 'Inference engine'},
        "ko": {
            "label": "추론 엔진",
        },
        "ja": {'label': 'Inference engine'},
    },
    "infer_dtype": {
        "en": {
            "label": "Inference data type",
        },
        "ru": {
            "label": "Тип данных для вывода",
        },
        "zh": {'label': 'Inference data type'},
        "ko": {
            "label": "추론 데이터 유형",
        },
        "ja": {'label': 'Inference data type'},
    },
    "load_btn": {
        "en": {
            "value": "Load model",
        },
        "ru": {
            "value": "Загрузить модель",
        },
        "zh": {'value': 'Load model'},
        "ko": {
            "value": "모델 불러오기",
        },
        "ja": {'value': 'Load model'},
    },
    "unload_btn": {
        "en": {
            "value": "Unload model",
        },
        "ru": {
            "value": "Выгрузить модель",
        },
        "zh": {'value': 'Unload model'},
        "ko": {
            "value": "모델 언로드",
        },
        "ja": {
            "value": "モデルをアンロード",
        },
    },
    "info_box": {
        "en": {
            "value": "Model unloaded, please load a model first.",
        },
        "ru": {
            "value": "Модель не загружена, загрузите модель сначала.",
        },
        "zh": {'value': 'Model unloaded, please load a model first.'},
        "ko": {
            "value": "모델이 언로드되었습니다. 모델을 먼저 불러오십시오.",
        },
        "ja": {'value': 'Model unloaded, please load a model first.'},
    },
    "role": {
        "en": {
            "label": "Role",
        },
        "ru": {
            "label": "Роль",
        },
        "zh": {'label': 'Role'},
        "ko": {
            "label": "역할",
        },
        "ja": {'label': 'Role'},
    },
    "system": {
        "en": {
            "placeholder": "System prompt (optional)",
        },
        "ru": {
            "placeholder": "Системный запрос (по желанию)",
        },
        "zh": {'placeholder': 'System prompt (optional)'},
        "ko": {
            "placeholder": "시스템 프롬프트 (선택 사항)",
        },
        "ja": {
            "placeholder": "システムプロンプト（オプション）",
        },
    },
    "tools": {
        "en": {
            "placeholder": "Tools (optional)",
        },
        "ru": {
            "placeholder": "Инструменты (по желанию)",
        },
        "zh": {'placeholder': 'Tools (optional)'},
        "ko": {
            "placeholder": "툴 (선택 사항)",
        },
        "ja": {
            "placeholder": "ツールリスト（オプション）",
        },
    },
    "image": {
        "en": {
            "label": "Image (optional)",
        },
        "ru": {
            "label": "Изображение (по желанию)",
        },
        "zh": {'label': 'Image (optional)'},
        "ko": {
            "label": "이미지 (선택 사항)",
        },
        "ja": {'label': 'Image (optional)'},
    },
    "video": {
        "en": {
            "label": "Video (optional)",
        },
        "ru": {
            "label": "Видео (по желанию)",
        },
        "zh": {'label': 'Video (optional)'},
        "ko": {
            "label": "비디오 (선택 사항)",
        },
        "ja": {'label': 'Video (optional)'},
    },
    "query": {
        "en": {
            "placeholder": "Input...",
        },
        "ru": {
            "placeholder": "Ввод...",
        },
        "zh": {'placeholder': 'Input...'},
        "ko": {
            "placeholder": "입력...",
        },
        "ja": {'placeholder': 'Input...'},
    },
    "submit_btn": {
        "en": {
            "value": "Submit",
        },
        "ru": {
            "value": "Отправить",
        },
        "zh": {'value': 'Submit'},
        "ko": {
            "value": "제출",
        },
        "ja": {'value': 'Submit'},
    },
    "max_length": {
        "en": {
            "label": "Maximum length",
        },
        "ru": {
            "label": "Максимальная длина",
        },
        "zh": {'label': 'Maximum length'},
        "ko": {
            "label": "최대 길이",
        },
        "ja": {'label': 'Maximum length'},
    },
    "max_new_tokens": {
        "en": {
            "label": "Maximum new tokens",
        },
        "ru": {
            "label": "Максимальное количество новых токенов",
        },
        "zh": {'label': 'Maximum new tokens'},
        "ko": {
            "label": "응답의 최대 길이",
        },
        "ja": {'label': 'Maximum new tokens'},
    },
    "top_p": {
        "en": {
            "label": "Top-p",
        },
        "ru": {
            "label": "Лучшие-p",
        },
        "zh": {'label': 'Top-p'},
        "ko": {
            "label": "Top-p",
        },
        "ja": {
            "label": "Top-p",
        },
    },
    "temperature": {
        "en": {
            "label": "Temperature",
        },
        "ru": {
            "label": "Температура",
        },
        "zh": {'label': 'Temperature'},
        "ko": {
            "label": "온도",
        },
        "ja": {'label': 'Temperature'},
    },
    "seed": {
        "en": {
            "label": "Generation seed (-1 for random)",
        },
        "ru": {
            "label": "Generation seed (-1 = random)",
        },
        "zh": {'label': 'Generation seed (-1 for random)'},
        "ko": {
            "label": "Generation seed (-1 = random)",
        },
        "ja": {
            "label": "Generation seed (-1 = random)",
        },
    },
    "eval_seed": {
        "en": {
            "label": "Seed",
            "info": "Random seed for evaluation and prediction.",
        },
        "ru": {
            "label": "Seed",
            "info": "Random seed for evaluation and prediction.",
        },
        "zh": {'label': 'Seed', 'info': 'Random seed for evaluation and prediction.'},
        "ko": {
            "label": "Seed",
            "info": "Random seed for evaluation and prediction.",
        },
        "ja": {
            "label": "Seed",
            "info": "Random seed for evaluation and prediction.",
        },
    },
    "skip_special_tokens": {
        "en": {
            "label": "Skip special tokens",
        },
        "ru": {
            "label": "Пропустить специальные токены",
        },
        "zh": {'label': 'Skip special tokens'},
        "ko": {
            "label": "스페셜 토큰을 건너뛰기",
        },
        "ja": {
            "label": "スペシャルトークンをスキップ",
        },
    },
    "escape_html": {
        "en": {
            "label": "Escape HTML tags",
        },
        "ru": {
            "label": "Исключить HTML теги",
        },
        "zh": {'label': 'Escape HTML tags'},
        "ko": {
            "label": "HTML 태그 이스케이프",
        },
        "ja": {
            "label": "HTML タグをエスケープ",
        },
    },
    "clear_btn": {
        "en": {
            "value": "Clear history",
        },
        "ru": {
            "value": "Очистить историю",
        },
        "zh": {'value': 'Clear history'},
        "ko": {
            "value": "기록 지우기",
        },
        "ja": {'value': 'Clear history'},
    },
    "export_size": {
        "en": {
            "label": "Max shard size (GB)",
            "info": "The maximum size for a model file.",
        },
        "ru": {
            "label": "Максимальный размер фрагмента (ГБ)",
            "info": "Максимальный размер файла модели.",
        },
        "zh": {'label': 'Max shard size (GB)', 'info': 'The maximum size for a model file.'},
        "ko": {
            "label": "최대 샤드 크기 (GB)",
            "info": "모델 파일의 최대 크기.",
        },
        "ja": {'label': 'Max shard size (GB)', 'info': 'The maximum size for a model file.'},
    },
    "export_quantization_bit": {
        "en": {
            "label": "Export quantization bit.",
            "info": "Quantizing the exported model.",
        },
        "ru": {
            "label": "Экспорт бита квантования",
            "info": "Квантование экспортируемой модели.",
        },
        "zh": {'label': 'Export quantization bit.', 'info': 'Quantizing the exported model.'},
        "ko": {
            "label": "양자화 비트 내보내기",
            "info": "내보낸 모델의 양자화.",
        },
        "ja": {'label': 'Export quantization bit.', 'info': 'Quantizing the exported model.'},
    },
    "export_quantization_dataset": {
        "en": {
            "label": "Export quantization dataset",
            "info": "The calibration dataset used for quantization.",
        },
        "ru": {
            "label": "Экспорт набора данных для квантования",
            "info": "Набор данных калибровки, используемый для квантования.",
        },
        "zh": {'label': 'Export quantization dataset', 'info': 'The calibration dataset used for quantization.'},
        "ko": {
            "label": "양자화 데이터셋 내보내기",
            "info": "양자화에 사용되는 교정 데이터셋.",
        },
        "ja": {'label': 'Export quantization dataset', 'info': 'The calibration dataset used for quantization.'},
    },
    "export_device": {
        "en": {
            "label": "Export device",
            "info": "Which device should be used to export model.",
        },
        "ru": {
            "label": "Экспорт устройство",
            "info": "Какое устройство следует использовать для экспорта модели.",
        },
        "zh": {'label': 'Export device', 'info': 'Which device should be used to export model.'},
        "ko": {
            "label": "내보낼 장치",
            "info": "모델을 내보내는 데 사용할 장치.",
        },
        "ja": {'label': 'Export device', 'info': 'Which device should be used to export model.'},
    },
    "export_legacy_format": {
        "en": {
            "label": "Export legacy format",
            "info": "Do not use safetensors to save the model.",
        },
        "ru": {
            "label": "Экспорт в устаревший формат",
            "info": "Не использовать safetensors для сохранения модели.",
        },
        "zh": {'label': 'Export legacy format', 'info': 'Do not use safetensors to save the model.'},
        "ko": {
            "label": "레거시 형식 내보내기",
            "info": "모델을 저장하는 데 safetensors를 사용하지 않습니다.",
        },
        "ja": {'label': 'Export legacy format', 'info': 'Do not use safetensors to save the model.'},
    },
    "export_dir": {
        "en": {
            "label": "Export dir",
            "info": "Directory to save exported model.",
        },
        "ru": {
            "label": "Каталог экспорта",
            "info": "Каталог для сохранения экспортированной модели.",
        },
        "zh": {'label': 'Export dir', 'info': 'Directory to save exported model.'},
        "ko": {
            "label": "내보내기 디렉토리",
            "info": "내보낸 모델을 저장할 디렉토리.",
        },
        "ja": {'label': 'Export dir', 'info': 'Directory to save exported model.'},
    },
    "export_hub_model_id": {
        "en": {
            "label": "HF Hub ID (optional)",
            "info": "Repo ID for uploading model to Hugging Face hub.",
        },
        "ru": {
            "label": "HF Hub ID (опционально)",
            "info": "Идентификатор репозитория для загрузки модели на Hugging Face hub.",
        },
        "zh": {'label': 'HF Hub ID (optional)', 'info': 'Repo ID for uploading model to Hugging Face hub.'},
        "ko": {
            "label": "HF 허브 ID (선택 사항)",
            "info": "모델을 Hugging Face 허브에 업로드하기 위한 레포 ID.",
        },
        "ja": {
            "label": "HF Hub ID（オプション）",
            "info": "Hugging Face Hub にモデルをアップロードするためのリポジトリ ID。",
        },
    },
    "export_btn": {
        "en": {
            "value": "Export",
        },
        "ru": {
            "value": "Экспорт",
        },
        "zh": {'value': 'Export'},
        "ko": {
            "value": "내보내기",
        },
        "ja": {
            "value": "エクスポート",
        },
    },
    "device_memory": {
        "en": {
            "label": "Device memory",
            "info": "Current memory usage of the device (GB).",
        },
        "ru": {
            "label": "Память устройства",
            "info": "Текущая память на устройстве (GB).",
        },
        "zh": {'label': 'Device memory', 'info': 'Current memory usage of the device (GB).'},
        "ko": {
            "label": "디바이스 메모리",
            "info": "지금 사용 중인 기기 메모리 (GB).",
        },
        "ja": {'label': 'Device memory', 'info': 'Current memory usage of the device (GB).'},
    },
}


ALERTS = {
    "err_conflict": {
        "en": "A process is in running, please abort it first.",
        "ru": "Процесс уже запущен, пожалуйста, сначала прервите его.",
        "zh": 'A process is in running, please abort it first.',
        "ko": "프로세스가 실행 중입니다. 먼저 중단하십시오.",
        "ja": 'A process is in running, please abort it first.',
    },
    "err_exists": {
        "en": "You have loaded a model, please unload it first.",
        "ru": "Вы загрузили модель, сначала разгрузите ее.",
        "zh": 'You have loaded a model, please unload it first.',
        "ko": "모델이 로드되었습니다. 먼저 언로드하십시오.",
        "ja": 'You have loaded a model, please unload it first.',
    },
    "err_no_model": {
        "en": "Please select a model.",
        "ru": "Пожалуйста, выберите модель.",
        "zh": 'Please select a model.',
        "ko": "모델을 선택하십시오.",
        "ja": 'Please select a model.',
    },
    "err_no_path": {
        "en": "Model not found.",
        "ru": "Модель не найдена.",
        "zh": 'Model not found.',
        "ko": "모델을 찾을 수 없습니다.",
        "ja": 'Model not found.',
    },
    "err_no_dataset": {
        "en": "Please choose a dataset.",
        "ru": "Пожалуйста, выберите набор данных.",
        "zh": 'Please choose a dataset.',
        "ko": "데이터 세트를 선택하십시오.",
        "ja": 'Please choose a dataset.',
    },
    "err_no_adapter": {
        "en": "Please select an adapter.",
        "ru": "Пожалуйста, выберите адаптер.",
        "zh": 'Please select an adapter.',
        "ko": "어댑터를 선택하십시오.",
        "ja": 'Please select an adapter.',
    },
    "err_no_output_dir": {
        "en": "Please provide output dir.",
        "ru": "Пожалуйста, укажите выходную директорию.",
        "zh": 'Please provide output dir.',
        "ko": "출력 디렉토리를 제공하십시오.",
        "ja": 'Please provide output dir.',
    },
    "err_no_reward_model": {
        "en": "Please select a reward model.",
        "ru": "Пожалуйста, выберите модель вознаграждения.",
        "zh": 'Please select a reward model.',
        "ko": "리워드 모델을 선택하십시오.",
        "ja": 'Please select a reward model.',
    },
    "err_no_export_dir": {
        "en": "Please provide export dir.",
        "ru": "Пожалуйста, укажите каталог для экспорта.",
        "zh": 'Please provide export dir.',
        "ko": "Export 디렉토리를 제공하십시오.",
        "ja": 'Please provide export dir.',
    },
    "err_gptq_lora": {
        "en": "Please merge adapters before quantizing the model.",
        "ru": "Пожалуйста, объедините адаптеры перед квантованием модели.",
        "zh": 'Please merge adapters before quantizing the model.',
        "ko": "모델을 양자화하기 전에 어댑터를 병합하십시오.",
        "ja": 'Please merge adapters before quantizing the model.',
    },
    "err_failed": {
        "en": "Failed.",
        "ru": "Ошибка.",
        "zh": 'Failed.',
        "ko": "실패했습니다.",
        "ja": 'Failed.',
    },
    "err_demo": {
        "en": "Training is unavailable in demo mode, duplicate the space to a private one first.",
        "ru": "Обучение недоступно в демонстрационном режиме, сначала скопируйте пространство в частное.",
        "zh": 'Training is unavailable in demo mode, duplicate the space to a private one first.',
        "ko": "데모 모드에서는 훈련을 사용할 수 없습니다. 먼저 프라이빗 레포지토리로 작업 공간을 복제하십시오.",
        "ja": 'Training is unavailable in demo mode, duplicate the space to a private one first.',
    },
    "err_tool_name": {
        "en": "Tool name not found.",
        "ru": "Имя инструмента не найдено.",
        "zh": 'Tool name not found.',
        "ko": "툴 이름을 찾을 수 없습니다.",
        "ja": 'Tool name not found.',
    },
    "err_json_schema": {
        "en": "Invalid JSON schema.",
        "ru": "Неверная схема JSON.",
        "zh": 'Invalid JSON schema.',
        "ko": "잘못된 JSON 스키마입니다.",
        "ja": 'Invalid JSON schema.',
    },
    "err_config_not_found": {
        "en": "Config file is not found.",
        "ru": "Файл конфигурации не найден.",
        "zh": 'Config file is not found.',
        "ko": "Config 파일을 찾을 수 없습니다.",
        "ja": 'Config file is not found.',
    },
    "warn_no_cuda": {
        "en": "CUDA environment was not detected.",
        "ru": "Среда CUDA не обнаружена.",
        "zh": 'CUDA environment was not detected.',
        "ko": "CUDA 환경이 감지되지 않았습니다.",
        "ja": 'CUDA environment was not detected.',
    },
    "warn_output_dir_exists": {
        "en": "Output dir already exists, will resume training from here.",
        "ru": "Выходной каталог уже существует, обучение будет продолжено отсюда.",
        "zh": 'Output dir already exists, will resume training from here.',
        "ko": "출력 디렉토리가 이미 존재합니다. 위 출력 디렉토리에 저장된 학습을 재개합니다.",
        "ja": 'Output dir already exists, will resume training from here.',
    },
    "warn_no_instruct": {
        "en": "You are using a non-instruct model, please fine-tune it first.",
        "ru": "Вы используете модель без инструкции, пожалуйста, primeros выполните донастройку этой модели.",
        "zh": 'You are using a non-instruct model, please fine-tune it first.',
        "ko": "당신은 지시하지 않은 모델을 사용하고 있습니다. 먼저 이를 미세 조정해 주세요.",
        "ja": 'You are using a non-instruct model, please fine-tune it first.',
    },
    "info_aborting": {
        "en": "Aborted, wait for terminating...",
        "ru": "Прервано, ожидание завершения...",
        "zh": 'Aborted, wait for terminating...',
        "ko": "중단되었습니다. 종료를 기다리십시오...",
        "ja": 'Aborted, wait for terminating...',
    },
    "info_aborted": {
        "en": "Ready.",
        "ru": "Готово.",
        "zh": 'Ready.',
        "ko": "준비되었습니다.",
        "ja": 'Ready.',
    },
    "info_finished": {
        "en": "Finished.",
        "ru": "Завершено.",
        "zh": 'Finished.',
        "ko": "완료되었습니다.",
        "ja": 'Finished.',
    },
    "info_config_saved": {
        "en": "Arguments have been saved at: ",
        "ru": "Аргументы были сохранены по адресу: ",
        "zh": 'Arguments have been saved at: ',
        "ko": "매개변수가 저장되었습니다: ",
        "ja": 'Arguments have been saved at: ',
    },
    "info_config_loaded": {
        "en": "Arguments have been restored.",
        "ru": "Аргументы были восстановлены.",
        "zh": 'Arguments have been restored.',
        "ko": "매개변수가 복원되었습니다.",
        "ja": 'Arguments have been restored.',
    },
    "info_loading": {
        "en": "Loading model...",
        "ru": "Загрузка модели...",
        "zh": 'Loading model...',
        "ko": "모델 로딩 중...",
        "ja": 'Loading model...',
    },
    "info_unloading": {
        "en": "Unloading model...",
        "ru": "Выгрузка модели...",
        "zh": 'Unloading model...',
        "ko": "모델 언로딩 중...",
        "ja": 'Unloading model...',
    },
    "info_loaded": {
        "en": "Model loaded, now you can chat with your model!",
        "ru": "Модель загружена, теперь вы можете общаться с вашей моделью!",
        "zh": 'Model loaded, now you can chat with your model!',
        "ko": "모델이 로드되었습니다. 이제 모델과 채팅할 수 있습니다!",
        "ja": 'Model loaded, now you can chat with your model!',
    },
    "info_unloaded": {
        "en": "Model unloaded.",
        "ru": "Модель выгружена.",
        "zh": 'Model unloaded.',
        "ko": "모델이 언로드되었습니다.",
        "ja": "モデルがアンロードされました。",
    },
    "info_thinking": {
        "en": "🌀 Thinking...",
        "ru": "🌀 Думаю...",
        "zh": '🌀 Thinking...',
        "ko": "🌀 생각 중...",
        "ja": '🌀 Thinking...',
    },
    "info_thought": {
        "en": "✅ Thought",
        "ru": "✅ Думать закончено",
        "zh": '✅ Thought',
        "ko": "✅ 생각이 완료되었습니다",
        "ja": '✅ Thought',
    },
    "info_exporting": {
        "en": "Exporting model...",
        "ru": "Экспорт модели...",
        "zh": 'Exporting model...',
        "ko": "모델 내보내기 중...",
        "ja": 'Exporting model...',
    },
    "info_exported": {
        "en": "Model exported.",
        "ru": "Модель экспортирована.",
        "zh": 'Model exported.',
        "ko": "모델이 내보내졌습니다.",
        "ja": 'Model exported.',
    },
    "info_swanlab_link": {
        "en": "### SwanLab Link\n",
        "ru": "### SwanLab ссылка\n",
        "zh": '### SwanLab Link\n',
        "ko": "### SwanLab 링크\n",
        "ja": "### SwanLab リンク\n",
    },
}
