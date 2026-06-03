# AI_Resume_Tailor  
# 🤖 Django AI Resume & Cover Letter Tailor (Backend)

A powerful, production-ready Django REST Framework backend that uses Advanced AI (via OpenRouter API) to analyze job descriptions and automatically tailor job applications. 

The system takes a candidate's base resume and a target vacancy description, analyzes the gaps, and dynamically generates a **professional personalized cover letter** and extracts **missing keywords/skills** that the developer should add to match the job requirements.

---

## ✨ Features

- 🧠 **AI Integration:** Seamless connection with OpenRouter API using flexible models (e.g., Llama 3.1, Gemini).
- ⚙️ **RESTful API:** Clean API endpoints built with Django REST Framework for submitting requests and retrieving analysis.
- 📋 **Application Management:** Full CRUD logic for tracking tailored application history, vacancy text, and states.
- 🔍 **Smart Prompt Engineering:** Tailored prompts that force the LLM to return structured, high-quality data.
- ⚡ **Automated Parsing:** Backend string parsing mechanism (`[SPLIT]` token processing) that safely separates the generated Cover Letter from the Missing Keywords before saving them into distinct database fields.
- 🛡️ **Robust Error Handling:** Integrated `try/except` safety blocks with automatic logging to handle upstream API rate limits (HTTP 429), timeouts, or server issues (HTTP 503) without crashing the application.
- 🚦 **Status Tracking:** Real-time state management for applications using status fields (`PENDING`, `SUCCESS`, `FAILED`).

---

## 🛠️ Tech Stack

- **Backend Framework:** Django & Django REST Framework (DRF)
- **AI Integration:** OpenRouter API / OpenAI Python SDK
- **Database:** PostgreSQL (or SQLite for local development)
- **Environment Management:** Python-dotenv

---

## 🚀 Getting Started

Follow these steps to get the AI Tailor backend running locally on your machine:

### 1️⃣ Clone the repository
```bash
git clone [https://github.com/MrD2ve/AI_Resume_Tailor.git](https://github.com/MrD2ve/AI_Resume_Tailor.git)
cd AI_Resume_Tailor
```

### 2️⃣ Create and activate venv
```bash
# On macOS/Linux:
python -m venv env
source env/bin/activate  

# On Windows:
python -m venv env
env\Scripts\activate
```

### 3️⃣ Install the requirement packages
```bash
pip install -r requirements.txt
```

### 4️⃣ Environment configuration ( .env )
```bash
# Django Settings
SECRET_KEY=your_django_secret_key_here
DEBUG=True

# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 5️⃣ Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate

### 6️⃣ Run the server
```bash
python manage.py runserver
```

---

## 🧪 API Testing with Postman

You can easily test the AI Resume Tailor API endpoints using **Postman**. Follow the guide below to structure your API requests and understand the backend responses.

### 📡 1. Match Resume & Generate Cover Letter
* **HTTP Method:** `POST`
* **Endpoint URL:** `http://127.0.0.1:8000/tailor/` (or your specific routing path)
* **Headers:** `Content-Type: application/json`

#### 📥 Headers Setup:
In Postman, go to the **Headers** tab and ensure you have:
| Key | Value |
| :--- | :--- |
| `Content-Type` | `application/json` |

#### 📝 Request Body (`raw` JSON):
Go to the **Body** tab, select **raw**, choose **JSON** from the dropdown, and paste the following payload:
```json
{
    "vacancy_description": "We are looking for a Junior Python Developer. Requirements: Django, REST Framework, PostgreSQL, Git, English B2."
}
```
## 📤 2. Understanding Backend Responses

The Django backend handles AI generation, custom token parsing, and response isolation dynamically. Depending on the server and upstream API state, you will receive one of the following responses:

### 🟢 Expected Successful Response (201 Created / 200 OK)
When the OpenRouter LLM successfully responds, the backend splits the markdown payload using the custom [SPLIT] logic and populates cover_letter and missing_keywords separately into individual fields:
```json
{
    "id": 13,
    "vacancy_description": "We are looking for a Junior Python Developer. Requirements: Django, REST Framework, PostgreSQL, Git, English B2.",
    "tailored_resume_text": null,
    "cover_letter": "Dear Hiring Manager,\n\nI am excited to apply for the Junior Python Developer position. As a Python developer with solid experience in Django...",
    "missing_keywords": "REST Framework (Django REST Framework), PostgreSQL, English B2",
    "status": "SUCCESS"
}
```

### 🟡 API Rate Limit / Provider Error Response (400 Bad Request)
If the upstream AI models (e.g., Llama, Gemini) hit free-tier rate limits (HTTP 429) or experience temporary downtime (HTTP 503), the robust try/except middleware catches the error, sets the status to FAILED, and safely returns the error payload instead of crashing the Django application:

```json
{
    "status": "FAILED",
    "error_details": "Error: Error code: 429 - {'error': {'message': 'Provider returned error... temporarily rate-limited upstream.'}}"
}
```

### 🔵 Initial Request State (Polling / Async Processing)
If your local instance handles requests asynchronously or returns an instant handshake tracking code, the endpoint might immediately return a tracking ID with a pending state while the AI finishes generating data in the background:

```json
{
    "id": 12,
    "vacancy_description": "We are looking for a Junior Python Developer...",
    "tailored_resume_text": null,
    "cover_letter": null,
    "missing_keywords": null,
    "status": "PENDING"
}
```
