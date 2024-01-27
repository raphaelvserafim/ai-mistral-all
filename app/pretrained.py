from transformers import GPT2LMHeadModel, GPT2Tokenizer

fine_tuned_model_path = "./fine-tuned-model"
fine_tuned_model = GPT2LMHeadModel.from_pretrained(fine_tuned_model_path)
tokenizer = GPT2Tokenizer.from_pretrained(fine_tuned_model_path)

prompt = "Hello"
max_length = 100  # Adjust as needed

input_ids = tokenizer.encode(prompt, return_tensors="pt")

# Generate text with the fine-tuned model
generated_text = fine_tuned_model.generate(input_ids, max_length=max_length, num_return_sequences=1)

# Decode the generated text
decoded_text = tokenizer.decode(generated_text[0], skip_special_tokens=True)
print(decoded_text)
