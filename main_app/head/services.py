import os
from openai import OpenAI
from django.conf import settings  # Import settings

def generate_tailored_resume(resume_text, vacancy_text):
    # Initialize the client by passing the OpenRouter key and address explicitly
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENROUTER_API_KEY,  # API Key from Django settings
    )

    prompt = f"""
           I have a resume:
           {resume_text}

           And a vacancy:
           {vacancy_text}

           Please do two things:
              1. Write a professional cover letter in English.
              2. Highlight the key skills (Keywords) that are missing from my resume for this position.

           IMPORTANT: Be sure to separate your cover letter and key skills with a line [SPLIT]. 
           Don't write anything else between them. Your answer should look EXACTLY like this:
           <cover letter text>
           [SPLIT]
           <text missing keywords>
           """

    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[
                {"role": "system", "content": "You are an expert HR manager and resume builder."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"