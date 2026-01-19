from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Form
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI(title="CropCare AI Backend")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://*.vercel.app",
                   "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY not found in .env file!")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini API configured successfully!")

# Add this block right after genai.configure(...)
print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)



@app.get("/")
async def root():
    return {
        "message": "CropCare AI Backend is running! 🌾",
        "status": "healthy",
        "gemini_configured": bool(GEMINI_API_KEY)
    }

@app.post("/api/analyze")
async def analyze_crop(file: UploadFile = File(...),language: str = Form(default="en")):
    """
    Analyze crop image for disease detection using Gemini AI
    Supports multilingual output based on 'language' param (en, hi, ml, ta, etc.)
    """
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="Gemini API key not configured. Please add GEMINI_API_KEY to .env file"
        )
    
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        lang_map = {
            "en": "English",
            "hi": "Hindi (Devanagari script)",
            "ta": "Tamil",
            "te": "Telugu",
            "kn": "Kannada",
            "ml": "Malayalam",
            "bn": "Bengali",
            "mr": "Marathi",
            "gu": "Gujarati",
            "pa": "Punjabi (Gurmukhi script)",
        }
        target_lang = lang_map.get(language, "English")
        
        # Prepare prompt for Gemini
#         prompt = """
# You are an expert agricultural pathologist. Analyze this crop/plant image and provide:

# 1. **Disease Identification**: What disease or problem is affecting this plant? If healthy, state "Healthy Plant"
# 2. **Confidence Level**: Your confidence in this diagnosis (0-100%)
# 3. **Symptoms Observed**: List visible symptoms you can see
# 4. **Affected Crop**: What type of crop/plant is this?
# 5. **Severity**: Rate as Mild, Moderate, or Severe
# 6. **Treatment Recommendations**: Provide 3-4 actionable treatment steps
# 7. **Prevention Tips**: Provide 2-3 prevention measures for future

# Format your response as JSON with these exact keys:
# {
#     "disease_name": "name of disease or 'Healthy Plant'",
#     "confidence": confidence_score_as_number,
#     "crop_type": "type of crop",
#     "symptoms": ["symptom1", "symptom2"],
#     "severity": "Mild/Moderate/Severe",
#     "treatment": ["step1", "step2", "step3"],
#     "prevention": ["tip1", "tip2", "tip3"]
# }

# If you cannot identify the plant or it's not a crop image, return:
# {
#     "disease_name": "Not a crop image",
#     "confidence": 0,
#     "crop_type": "Unknown",
#     "symptoms": ["Unable to identify plant"],
#     "severity": "N/A",
#     "treatment": ["Please upload a clear image of crop leaves or plants"],
#     "prevention": []
# }
# """
        prompt = f"""
You are an expert agricultural pathologist. Analyze this crop/plant image carefully and provide the diagnosis **entirely in {target_lang} language**, using the correct native script.

Respond **only** in {target_lang}. Do NOT use English unless it's a proper name or technical term that has no natural translation.

Provide:

1. Disease name (or "Healthy Plant" translated to {target_lang} if no disease)
2. Confidence level (0-100%)
3. List of visible symptoms
4. Crop/plant type
5. Severity: Mild / Moderate / Severe (translated to {target_lang})
6. 3-4 actionable treatment steps
7. 2-3 prevention measures

Format as JSON with these exact English keys (do not translate the keys):
{{
    "disease_name": "...",
    "confidence": number,
    "crop_type": "...",
    "symptoms": ["symptom1 in {target_lang}", "symptom2 in {target_lang}"],
    "severity": "Mild" or "Moderate" or "Severe" (translated),
    "treatment": ["step1 in {target_lang}", ...],
    "prevention": ["tip1 in {target_lang}", ...]
}}

If not a crop image or cannot identify:
{{
    "disease_name": "Not a crop image" (translated),
    "confidence": 0,
    "crop_type": "Unknown" (translated),
    "symptoms": ["Unable to identify plant" (translated)],
    "severity": "N/A",
    "treatment": ["Please upload a clear image..." (translated)],
    "prevention": []
}}

Image to analyze:
"""
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Generate response
        response = model.generate_content([prompt, image])
        
        # Extract text from response
        response_text = response.text.strip()
        
        # Clean up response (remove markdown code blocks if present)
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif response_text.startswith('```'):
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        # Parse JSON response
        result = json.loads(response_text)
        
        # Add metadata
        result['filename'] = file.filename
        result['image_size'] = f"{image.size[0]}x{image.size[1]}"
        result['file_size_kb'] = round(len(contents) / 1024, 2)
        
        return result
        
    except json.JSONDecodeError as e:
        # If JSON parsing fails, return a structured error with raw response
        print(f"JSON Parse Error: {str(e)}")
        print(f"Raw response: {response_text[:500]}")
        
        return {
            "disease_name": "Analysis Complete",
            "confidence": 70,
            "crop_type": "Unable to parse",
            "symptoms": ["AI provided analysis but format was unclear"],
            "severity": "N/A",
            "treatment": [
                "The AI analyzed your image but couldn't structure the response properly.",
                "Raw response: " + response_text[:300] + "..."
            ],
            "prevention": ["Please try uploading a clearer image of the crop"],
            "error": "JSON parsing failed",
            "raw_response": response_text[:500]
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Error analyzing image: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "gemini_configured": bool(GEMINI_API_KEY),
        "model": "gemini-2.5-flash"
    }