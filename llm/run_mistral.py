import ollama

# Load the Mistral model using Ollama
model_name = "mistral"
ollama_client = ollama.Client()

# Generate text
input_text = "Once upon a time"
response = ollama_client.generate(model=model_name, prompt=input_text)
print(response)