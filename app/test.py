from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model = AutoModelForSeq2SeqLM.from_pretrained('./mistral_finetuned')  
tokenizer = AutoTokenizer.from_pretrained('./mistral_finetuned')

def generate_response(prompt):

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding="max_length", max_length=512)

    
    outputs = model.generate(inputs['input_ids'], max_length=128, num_return_sequences=1)

    # Decodificar a resposta gerada
    generated_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_response

 
response = generate_response("Hi John")

print("Generated Response:", response)