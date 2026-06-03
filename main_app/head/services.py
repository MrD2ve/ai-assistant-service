import os
from openai import OpenAI
from django.conf import settings


def generate_tailored_resume(resume_text, vacancy_text):
    # Инициализируем клиент, но перенаправляем его на OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    prompt = f"""
    У меня есть резюме:
    {resume_text}

    И вакансия:
    {vacancy_text}

    Пожалуйста, сделай две вещи:
    1. Напиши профессиональное сопроводительное письмо (Cover Letter) на английском.
    2. Выдели список ключевых навыков (Keywords), которых не хватает в моем резюме для этой вакансии.
    """

    try:
        response = client.chat.completions.create(
            # Используем мощную и бесплатную модель Llama 3.3 70B
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "system", "content": "You are an expert HR manager and resume builder."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"