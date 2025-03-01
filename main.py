from fastapi import FastAPI
from pydantic import BaseModel
import csv
import random

# Initialize the FastAPI app
app = FastAPI()

# Pydantic models for input validation
class Character(BaseModel):
    name: str
    age: int
    role: str
    faction: str
    weapon: str
    location: str
    strength: int
    intelligence: int

class Quote(BaseModel):
    character_name: str
    quote: str

# Function to read characters from the CSV file
def get_characters_from_csv():
    characters = []
    try:
        with open('characters.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                characters.append(row)
    except FileNotFoundError:
        return []
    return characters

# Function to read quotes from the CSV file
def get_quotes_from_csv():
    quotes = []
    try:
        with open('quote.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                quotes.append(row)
    except FileNotFoundError:
        return []
    return quotes

# POST route to create a new character
@app.post("/create_characters")
async def create_character(character: Character):
    # Open the CSV file in append mode and add the new character
    with open('characters.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=character.dict().keys())
        # If the file is empty, write the header first
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(character.dict())
    return {"message": "Character created successfully", "character": character}

# POST route to create a new quote
@app.post("/create_quote")
async def create_quote(quote: Quote):
    # Open the CSV file in append mode and add the new quote
    with open('quote.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=quote.dict().keys())
        # If the file is empty, write the header first
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(quote.dict())
    return {"message": "Quote created successfully", "quote": quote}

# Route to get a random quote
@app.get("/quote")
async def get_random_quote():
    quotes = get_quotes_from_csv()
    if quotes:
        quote = random.choice(quotes)
        return {"quote": quote}
    return {"error": "No quotes available"}

# Route to get all characters
@app.get("/characters")
async def get_characters():
    characters = get_characters_from_csv()
    return {"characters": characters}

# Route to get a specific character by name
@app.get("/characters/{name}")
async def get_character(name: str):
    characters = get_characters_from_csv()
    character = next((c for c in characters if c["name"].lower() == name.lower()), None)
    if character:
        return {"character": character}
    return {"error": "Character not found"}, 404
