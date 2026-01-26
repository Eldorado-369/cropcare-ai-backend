# CropCare AI – Backend  
**AI-Powered Crop Disease Detection API for Indian Farmers**

[![IBM SkillsBuild](https://img.shields.io/badge/IBM%20SkillsBuild-AI--ML%20Internship-blue?style=for-the-badge&logo=ibm)](https://skillsbuild.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)  
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)  
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

**Frontend Repo & Demo**: https://github.com/Eldorado-369/cropcare-ai-frontend | Live Demo: https://cropcare-ai-frontend.vercel.app/ 

Submitted as part of **IBM SkillsBuild AI-ML Internship** by **Eldho K Shajee**, 

## Overview
This backend powers CropCare AI, a web app for Indian farmers to detect crop diseases via leaf photos. It receives images and language preferences from the frontend, processes them using Pillow, analyzes with **Google Gemini 2.5-flash** (multimodal AI model), and returns multilingual JSON results (disease, symptoms, treatment, prevention).

Addresses challenges like manual detection delays and multilingual barriers in rural India, promoting sustainable farming.

## Key Features
- **API Endpoint**: POST `/api/analyze` – Accepts image file + language code; returns structured JSON in requested language (e.g., Hindi, Tamil).
- **Disease Detection**: Identifies diseases, crop type, severity (Mild/Moderate/Severe), confidence score; confirms healthy plants.
- **Multilingual Support**: Outputs in English + 9 Indian languages (Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi) via prompt engineering.
- **Image Handling**: Validates and processes uploads with Pillow.
- **Scalable & Free**: Deployed on Render's free tier; handles cold starts and memory limits.

## Tech Stack
- **Framework**: FastAPI (Python) for efficient API endpoints.
- **AI Integration**: Google Generative AI SDK with Gemini 2.5-flash (multimodal, strong Indic language support).
- **Image Processing**: Pillow.
- **Server**: Uvicorn (ASGI).
- **Environment**: Python 3.8+; env vars for `GOOGLE_API_KEY`.
- **Deployment**: Render (easy Python web service hosting, free for demos).

## Data Flow
1. Frontend sends image + language via POST `/api/analyze`.
2. Backend validates image with Pillow.
3. Prompts Gemini with structured instructions (including language).
4. Gemini analyzes and returns JSON in target language.
5. Backend responds to frontend.

