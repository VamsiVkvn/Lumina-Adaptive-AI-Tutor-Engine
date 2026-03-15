import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_quiz_from_chunk(text_chunk, difficulty="medium"):
    prompt = f"""
    You are an expert teacher. Based on the following educational text, generate 3 questions:
    1 MCQ, 1 True/False, and 1 Fill-in-the-blank.
    
    Text: "{text_chunk}"
    Difficulty: {difficulty}
    
    Return ONLY a JSON list:
    [
      {{
        "question": "string",
        "type": "MCQ",
        "options": ["choice1", "choice2", "choice3", "choice4"],
        "answer": "the correct string",
        "difficulty": "{difficulty}"
      }},
      ...
    ]
    """
    
    response = client.chat.completions.create(
        model="gpt-4o", # or "gpt-3.5-turbo"
        messages=[{"role": "system", "content": "You output strictly valid JSON."},
                  {"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    
    return json.loads(response.choices[0].message.content)
