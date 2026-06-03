import os
from openai import OpenAI
from django.conf import settings  # Импортируем настройки

def generate_tailored_resume(resume_text, vacancy_text):
    # Инициализируем клиент, передавая ключ и адрес OpenRouter явно
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENROUTER_API_KEY,  # Берём ключ из настроек Django
    )

    prompt = f"""
           У меня есть резюме:
           {resume_text}

           И вакансия:
           {vacancy_text}

           Пожалуйста, сделай две вещи:
           1. Напиши профессиональное сопроводительное письмо (Cover Letter) на английском.
           2. Выдели список ключевых навыков (Keywords), которых не хватает в моем резюме для этой вакансии.

           ВАЖНО: Обязательно раздели сопроводительное письмо и ключевые навыки строкой [SPLIT]. 
           Ничего другого между ними не пиши. Твой ответ должен выглядеть ТОЧНО так:
           <текст сопроводительного письма>
           [SPLIT]
           <текст missing keywords>
           """

    try:
        response = client.chat.completions.create(
            model="openrouter/owl-alpha",
            messages=[
                {"role": "system", "content": "You are an expert HR manager and resume builder."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"