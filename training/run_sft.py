from peft import LoraConfig
from trl import SFTConfig, SFTTrainer
from datasets import load_dataset

MODEL_NAME='unsloth/Meta-Llama-3.1-8B-Instruct'
DATASET_PATH='notebooks/dataset.jsonl'
OUTPUT_DIR='finetuned_model'

if __name__=='__main__':

    sft_config = SFTConfig(
        output_dir=OUTPUT_DIR,
        bf16=True,
        max_length=1024,
        learning_rate=1e-5,
        per_device_train_batch_size=8,
        gradient_accumulation_steps=1,
        num_train_epochs=10,
        warmup_ratio=0.1,
        save_strategy='epoch',
        save_total_limit=1,
        save_only_model=True,
    )

    lora_config = LoraConfig(
        r=16,
        lora_alpha=16,
        use_rslora=True
    )

    dataset = load_dataset('json', data_files=DATASET_PATH, split='train')

    trainer = SFTTrainer(
        model=MODEL_NAME,
        peft_config=lora_config,
        args=sft_config,
        train_dataset=dataset,
    )

    num_train_params = trainer.get_num_trainable_parameters()
    print(f'Trainable params: {num_train_params/1e6:.2F}M')

    trainer.train()