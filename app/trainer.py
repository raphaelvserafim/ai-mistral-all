from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

# Load the pre-trained model and tokenizer
model_name = "mistralai/Mistral-7B-Instruct-v0.1"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Load your dataset (replace with your own dataset)
dataset = TextDataset(
    tokenizer=tokenizer,
    file_path="dataset.txt",
    block_size=128  # Adjust block size as needed
)

# Prepare data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # For language modeling tasks, set mlm to False
)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./fine-tuned-model",
    overwrite_output_dir=True,
    num_train_epochs=3,  # Adjust the number of epochs as needed
    per_device_train_batch_size=4,  # Adjust batch size as needed
    save_steps=10_000,
    save_total_limit=2,
)

# Create Trainer and fine-tune the model
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

trainer.train()
