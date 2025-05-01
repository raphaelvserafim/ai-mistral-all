from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import Dataset

model_name = "mistralai/Ministral-8B-Instruct-2410"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def load_txt(file_path):
    with open(file_path, "r") as f:
        text = f.read().strip()
    
    examples = []
    segments = text.split("\n### Instruction:")
    
    for segment in segments[1:]: 
        lines = segment.strip().split("\n")
        instruction = lines[0].replace("Instruction:", "").strip()
        user_input = lines[1].replace("Input:", "").strip()
        response = lines[2].replace("Response:", "").strip()
        examples.append({"instruction": instruction, "input": user_input, "output": response})
    
    return examples

 
train_data = load_txt("../dataset/train.txt")
train_dataset = Dataset.from_dict({"instruction": [x["instruction"] for x in train_data], 
                                   "input": [x["input"] for x in train_data], 
                                   "output": [x["output"] for x in train_data]})


def preprocess(example):
    prompt = f"### Instruction:\n{example['instruction']}\n### Input:\n{example['input']}\n### Response:"
    tokenized = tokenizer(prompt, max_length=512, truncation=True, padding="max_length")
    labels = tokenizer(example["output"], max_length=128, truncation=True, padding="max_length")
    tokenized["labels"] = labels["input_ids"]
    return tokenized

tokenized_dataset = train_dataset.map(preprocess)


training_args = TrainingArguments(
    output_dir="./mistral_finetuned",  
    per_device_train_batch_size=2,
    num_train_epochs=10,
    logging_steps=10,
    save_strategy="no",  
    fp16=False   
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
)

trainer.train()

model.save_pretrained("./mistral_finetuned")
tokenizer.save_pretrained("./mistral_finetuned")