import openai
import os

# Set up OpenAI API credentials
openai.api_key = "API_KEY" # *_ Put your key here! _*

# Function to generate text using GPT-3.5
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
    )

    message = response.choices[0].text.strip()
    return message

# Function to generate new descriptions and keywords for a product
def generate_descriptions(products):
    generated_products = []
    for product in products:
        cod, nome, breve_descrizione, descrizione = product
        prompt = f"New {nome} - {breve_descrizione}\n\n{descrizione}\n\n"
        new_breve_descrizione = generate_text(prompt + "Write a short description for the product.")
        new_descrizione = generate_text(prompt + "Write a detailed description for the product.")
        generated_product = (cod, nome, new_breve_descrizione, new_descrizione)
        generated_products.append(generated_product)
    return generated_products