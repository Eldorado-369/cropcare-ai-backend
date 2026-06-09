# CropCare AI – Backend

> FastAPI backend powering AI-driven crop disease detection for Indian farmers

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini%202.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Render](https://img.shields.io/badge/Deployed%20on%20Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://render.com/)
[![IBM SkillsBuild](https://img.shields.io/badge/IBM%20SkillsBuild%20AI--ML%20Internship-054ADA?style=for-the-badge&logo=ibm&logoColor=white)](https://skillsbuild.org/)

**Frontend Repo:** [cropcare-ai-frontend](https://github.com/Eldorado-369/cropcare-ai-frontend) · **Live Demo:** [cropcare-ai-frontend.vercel.app](https://cropcare-ai-frontend.vercel.app/)

Submitted as the **IBM SkillsBuild AI-ML Internship capstone project** by **Eldho K Shajee**

---

## Overview

CropCare AI is a REST API that accepts a crop leaf image and returns a structured disease diagnosis in any of **10 Indian languages**. It uses **Google Gemini 2.5 Flash** multimodal AI with carefully engineered prompts to deliver actionable results — disease name, severity, symptoms, treatment, and prevention — formatted as clean JSON for easy frontend consumption.

---

## Key Features

- **Multimodal AI Analysis** — Processes images directly via Gemini 2.5 Flash vision capabilities
- **10 Indian Languages** — English, Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi
- **Structured JSON Output** — Crop type, disease name, confidence score, severity (Mild / Moderate / Severe), symptoms, treatment steps, prevention tips
- **Image Validation** — File type and size checks via Pillow before API call
- **CORS Enabled** — Ready for cross-origin frontend consumption
- **Deployed on Render** — Auto-deploy from main branch

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| AI Model | Google Gemini 2.5 Flash (multimodal) |
| Image Processing | Pillow |
| Language | Python 3.11+ |
| Deployment | Render |

---

## API Reference

### `POST /analyze`

Accepts a crop leaf image and returns an AI-generated disease report.

**Request** — `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `image` | file | Crop leaf/plant photo (JPEG, PNG) |
| `language` | string | Target language code (e.g. `en`, `hi`, `ta`) |

**Response** — `application/json`

```json
{
  "crop_type": "Tomato",
  "disease_name": "Early Blight",
  "confidence": 92,
  "severity": "Moderate",
  "symptoms": ["Dark brown spots", "Yellow halos around lesions"],
  "treatment": ["Apply copper-based fungicide", "Remove infected leaves"],
  "prevention": ["Rotate crops annually", "Avoid overhead irrigation"]
}
```

---

## Local Setup

### Prerequisites
- Python 3.11+
- Google Gemini API key ([get one here](https://makersuite.google.com/app/apikey))

### Steps

```bash
# Clone the repo
git clone https://github.com/Eldorado-369/cropcare-ai-backend.git
cd cropcare-ai-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GEMINI_API_KEY=your_api_key_here

# Run the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Project Structure

```
cropcare-ai-backend/
├── main.py              # FastAPI app entry point & route definitions
├── requirements.txt     # Python dependencies
└── README.md
```

---

## Deployment

This backend is deployed on **Render** with automatic deploys from the `main` branch.

To deploy your own instance:
1. Fork this repo
2. Create a new Web Service on Render
3. Set `GEMINI_API_KEY` as an environment variable
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## About the Author

**Eldho K Shajee** — M.Sc. Data Science & Analytics, Jain University

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/eldho-k-shajee-723102279)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Eldorado-369)

---

## License

This project is open source and available under the [MIT License](LICENSE).
