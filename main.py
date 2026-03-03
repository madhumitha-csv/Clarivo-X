"""
main.py — BankIQ Enhanced Backend v3.0
Features Added:
  1. Voice AI — /api/voice/ask (browser TTS)
  2. Twilio Phone Call IVR — /api/twilio/voice, /api/twilio/gather
  3. Rejection Reasons + Approval Guidance — in /api/loan/predict
  4. Personalized AI Chatbot — /api/ask (multi-turn, voice-friendly)
  5. Language Selection at Login — /api/auth/login, /api/auth/set-language
  6. UI Localization — /api/ui/labels?language=Tamil
  7. Full multilingual support across all endpoints

Run:
  pip install fastapi uvicorn groq lightgbm scikit-learn shap twilio pydantic
  python models/ml_models.py   # train models first
  python main.py

Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional
import uvicorn, json, os

from services.claude_service import (
    ask_claude, shap_to_plain, simplify, whatif_explain,
    get_ui_labels
)
from services.voice_service import voice_ask
from services.twilio_service import handle_incoming_call, handle_gather, twilio_voice_response
from models.ml_models import predict_loan, predict_churn

app = FastAPI(title="BankIQ API", version="3.0",
              description="Explainable AI Banking with Voice, Multilingual & Twilio Support")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# In-memory session store (replace with Redis/DB in production)
# Structure: { username: { language, profile, login_time } }
user_sessions: dict = {}

SUPPORTED_LANGUAGES = ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada", "Marathi", "Bengali"]
# Primary languages (shown in UI): English, Tamil, Hindi, Malayalam
# Secondary languages (API-only): Telugu, Kannada, Marathi, Bengali
SUPPORTED_PROFILES   = ["Student", "Professional", "Elder", "Business", "Farmer"]


# ══════════════════════════════════════
# REQUEST MODELS
# ══════════════════════════════════════

class Msg(BaseModel):
    role: str
    content: str

class AskReq(BaseModel):
    question: str
    profile: str = "Student"
    language: str = "English"
    topic: str = "Loans & EMI"
    history: List[Msg] = []

class VoiceAskReq(BaseModel):
    question: str
    language: str = "English"
    profile: str = "Student"

class SimplifyReq(BaseModel):
    previous_answer: str
    profile: str = "Student"
    language: str = "English"

class LoanReq(BaseModel):
    income: float
    loan_amount: float
    cibil_score: int = 700
    education: str = "Graduate"
    self_employed: str = "No"
    loan_term: int = 12
    dependents: int = 0
    residential_assets: float = 0
    commercial_assets: float = 0
    luxury_assets: float = 0
    bank_assets: float = 0
    profile: str = "Student"
    language: str = "English"

class ChurnReq(BaseModel):
    tenure: int
    balance: float
    products: int = 1
    is_active: bool = True
    complaints: int = 0
    credit_score: int = 650
    age: int = 35
    salary: float = 50000
    satisfaction: int = 3
    points: int = 400
    profile: str = "Student"
    language: str = "English"

class WhatIfReq(BaseModel):
    original_inputs: dict
    modified_inputs: dict
    original_result: str
    new_result: str
    profile: str = "Student"
    language: str = "English"

class FeedbackReq(BaseModel):
    question: str
    answer: str
    rating: int
    profile: str
    language: str
    comment: str = ""

class LoginReq(BaseModel):
    username: str

class SetLanguageReq(BaseModel):
    username: str
    language: str
    profile: str = "Student"

class TwilioGatherReq(BaseModel):
    Digits: str = ""
    SpeechResult: str = ""
    CallSid: str = ""
    language: str = "English"
    call_stage: str = "greeting"


# ══════════════════════════════════════
# ROOT & HEALTH
# ══════════════════════════════════════

@app.get("/")
def root():
    return {
        "status": "BankIQ API Running! 🚀",
        "version": "3.0",
        "docs": "http://localhost:8000/docs",
        "new_features": [
            "Voice AI → POST /api/voice/ask",
            "Twilio IVR → POST /api/twilio/voice | POST /api/twilio/gather",
            "Language Login → POST /api/auth/login + POST /api/auth/set-language",
            "UI Labels → GET /api/ui/labels?language=Tamil",
            "Multilingual across all endpoints"
        ],
        "endpoints": [
            "POST /api/ask",
            "POST /api/voice/ask",
            "POST /api/simplify",
            "POST /api/loan/predict",
            "POST /api/churn/predict",
            "POST /api/whatif/explain",
            "POST /api/feedback",
            "GET  /api/feedback/stats",
            "POST /api/auth/login",
            "POST /api/auth/set-language",
            "GET  /api/ui/labels",
            "GET  /api/languages",
            "POST /api/twilio/voice",
            "POST /api/twilio/gather"
        ]
    }

@app.get("/health")
def health():
    loan_ready  = os.path.exists("models/loan_model.pkl")
    churn_ready = os.path.exists("models/churn_model.pkl")
    return {
        "status": "healthy",
        "loan_model":  "✅ Ready" if loan_ready  else "❌ Run ml_models.py",
        "churn_model": "✅ Ready" if churn_ready else "❌ Run ml_models.py",
        "active_sessions": len(user_sessions),
        "supported_languages": SUPPORTED_LANGUAGES,
        "features": ["voice", "twilio", "multilingual", "xai", "chatbot"]
    }


# ══════════════════════════════════════════════════════
# FEATURE 5 & 6 — LANGUAGE SELECTION AT LOGIN + UI LABELS
# ══════════════════════════════════════════════════════

@app.post("/api/auth/login")
def login(req: LoginReq):
    """
    Step 1 of login: User enters username.
    Returns a language selection prompt in all languages.
    Frontend should show language picker based on this response.
    """
    user_sessions[req.username] = {
        "username": req.username,
        "language": None,  # not set yet
        "profile": "Student",
        "logged_in": True
    }
    return {
        "success": True,
        "username": req.username,
        "message": "Please select your preferred language",
        "language_prompt": {
            "English":   "Please select your preferred language to continue",
            "Tamil":     "தொடர உங்கள் மொழியை தேர்ந்தெடுக்கவும்",
            "Hindi":     "जारी रखने के लिए अपनी भाषा चुनें",
            "Telugu":    "కొనసాగించడానికి మీ భాషను ఎంచుకోండి",
            "Kannada":   "ಮುಂದುವರಿಯಲು ನಿಮ್ಮ ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ",
            "Malayalam": "തുടരാൻ നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക",
            "Marathi":   "सुरू ठेवण्यासाठी तुमची भाषा निवडा",
            "Bengali":   "চালিয়ে যেতে আপনার ভাষা নির্বাচন করুন"
        },
        "available_languages": SUPPORTED_LANGUAGES,
        "available_profiles": SUPPORTED_PROFILES
    }


@app.post("/api/auth/set-language")
def set_language(req: SetLanguageReq):
    """
    Step 2 of login: User selects language and profile.
    Returns full UI labels in the chosen language.
    """
    if req.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language. Choose from: {SUPPORTED_LANGUAGES}")

    # Update or create session
    user_sessions[req.username] = {
        "username": req.username,
        "language": req.language,
        "profile":  req.profile,
        "logged_in": True
    }

    ui_labels = get_ui_labels(req.language)

    return {
        "success":  True,
        "username": req.username,
        "language": req.language,
        "profile":  req.profile,
        "ui_labels": ui_labels,
        "message":  ui_labels.get("welcome", f"Welcome, {req.username}!")
    }


@app.get("/api/ui/labels")
def get_labels(language: str = Query(default="English", description="Language code")):
    """
    Returns full UI label translations for website localization.
    Call this on language change to update ALL website text.
    Query: GET /api/ui/labels?language=Tamil
    """
    if language not in SUPPORTED_LANGUAGES:
        language = "English"
    return {
        "language": language,
        "labels": get_ui_labels(language)
    }


@app.get("/api/languages")
def get_languages():
    """Returns all supported languages and profiles."""
    return {
        "languages": SUPPORTED_LANGUAGES,
        "profiles":  SUPPORTED_PROFILES
    }


# ══════════════════════════════════════
# FEATURE 4 — AI CHATBOT (Text)
# ══════════════════════════════════════

@app.post("/api/ask")
async def ask(req: AskReq):
    """Personalized multilingual banking chatbot with conversation memory."""
    try:
        history = [{"role": m.role, "content": m.content} for m in req.history]
        data = await ask_claude(
            req.question, req.profile,
            req.language, req.topic, history
        )
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════
# FEATURE 1 — VOICE AI (Browser TTS)
# ══════════════════════════════════════

@app.post("/api/voice/ask")
async def voice_ask_api(req: VoiceAskReq):
    """
    Returns a SHORT plain-text answer optimized for Text-to-Speech.
    Frontend: use Web Speech API (SpeechSynthesis) to read this aloud.
    Supports multilingual TTS — Tamil, Hindi, Telugu, Kannada, English.

    Frontend JS example:
        const res = await fetch('/api/voice/ask', {...});
        const { voice_text } = await res.json();
        const utter = new SpeechSynthesisUtterance(voice_text);
        utter.lang = 'ta-IN'; // for Tamil
        window.speechSynthesis.speak(utter);

    Lang codes: en-IN, ta-IN, hi-IN, te-IN, kn-IN, ml-IN, mr-IN, bn-IN
    """
    try:
        text = await voice_ask(req.question, req.language, req.profile)

        lang_codes = {
            "English": "en-IN", "Tamil": "ta-IN", "Hindi": "hi-IN",
            "Telugu": "te-IN", "Kannada": "kn-IN", "Malayalam": "ml-IN",
            "Marathi": "mr-IN", "Bengali": "bn-IN"
        }

        return {
            "success": True,
            "voice_text": text,
            "language": req.language,
            "lang_code": lang_codes.get(req.language, "en-IN"),
            "tip": "Use Web Speech API (SpeechSynthesisUtterance) to play this text in the browser"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════
# FEATURE 2 — TWILIO PHONE CALL IVR
# ══════════════════════════════════════

@app.post("/api/twilio/voice")
async def twilio_incoming_call(request: Request):
    """
    Twilio webhook for incoming phone calls.
    Configure this URL in Twilio Console → Phone Number → Voice Webhook.
    Returns TwiML XML for IVR (Interactive Voice Response).

    Setup:
      1. pip install twilio
      2. Get Twilio account at twilio.com
      3. Buy a phone number
      4. Set Voice webhook to: https://your-server.com/api/twilio/voice
      5. Users call your Twilio number → BankIQ IVR starts
    """
    return await handle_incoming_call()


@app.post("/api/twilio/gather")
async def twilio_gather(request: Request, stage: str = Query(default="language_select")):
    """
    Handles digit/speech input from Twilio IVR.
    Progresses caller through: language_select → main_menu → faq
    """
    return await handle_gather(request, stage, user_sessions)


# ══════════════════════════════════════
# SIMPLIFY
# ══════════════════════════════════════

@app.post("/api/simplify")
async def simplify_api(req: SimplifyReq):
    try:
        data = await simplify(req.previous_answer, req.profile, req.language)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════════════════════
# FEATURE 3 — LOAN PREDICTION WITH REJECTION REASONS
# ══════════════════════════════════════════════════════

@app.post("/api/loan/predict")
async def loan_api(req: LoanReq):
    """
    Predicts loan approval/rejection.
    If REJECTED: returns clear rejection reasons + personalized improvement steps + reapply timeline.
    If APPROVED: returns why it was approved + next steps to maintain status.
    Full multilingual support.
    """
    try:
        approved, confidence, shap_dict = predict_loan(
            income             = req.income,
            loan_amount        = req.loan_amount,
            cibil_score        = req.cibil_score,
            education          = req.education,
            self_employed      = req.self_employed,
            loan_term          = req.loan_term,
            dependents         = req.dependents,
            residential_assets = req.residential_assets,
            commercial_assets  = req.commercial_assets,
            luxury_assets      = req.luxury_assets,
            bank_assets        = req.bank_assets
        )

        loan_inputs = {
            "cibil_score":  req.cibil_score,
            "income":       req.income,
            "loan_amount":  req.loan_amount,
            "education":    req.education,
            "self_employed":req.self_employed,
            "loan_term":    req.loan_term,
            "dependents":   req.dependents
        }

        explanation = await shap_to_plain(
            shap_dict, approved,
            req.profile, req.language,
            "loan", loan_inputs
        )

        result = {
            "success":    True,
            "prediction": "Approved" if approved else "Rejected",
            "confidence": confidence,
            "shap":       shap_dict,

            # Core explanation (multilingual)
            "explanation_points": explanation.get("explanation_points", []),
            "analogy":            explanation.get("analogy", ""),
            "transparency_score": explanation.get("transparency_score", 80),

            # FEATURE 3 — Rejection Reasons
            "rejection_reasons": explanation.get("rejection_reasons", []),

            # FEATURE 3 — What to do next
            "next_steps": explanation.get("next_steps", []),

            # FEATURE 3 — When to reapply
            "reapply_timeline": explanation.get("reapply_timeline", ""),

            # FEATURE 3 — Top improvement tip
            "improvement_tip": explanation.get("improvement_tip", ""),

            # FEATURE 1 — Voice-ready summary
            "voice_summary": explanation.get("voice_summary", ""),

            # Full explanation
            "explanation": explanation
        }

        _log_prediction("loan", loan_inputs, result)
        return result

    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Loan model not found! Run: python models/ml_models.py")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════
# CHURN PREDICTION
# ══════════════════════════════════════

@app.post("/api/churn/predict")
async def churn_api(req: ChurnReq):
    try:
        will_churn, risk_score, shap_dict = predict_churn(
            tenure       = req.tenure,
            balance      = req.balance,
            products     = req.products,
            is_active    = req.is_active,
            complaints   = req.complaints,
            credit_score = req.credit_score,
            age          = req.age,
            salary       = req.salary,
            satisfaction = req.satisfaction,
            points       = req.points
        )

        explanation = await shap_to_plain(
            shap_dict, will_churn,
            req.profile, req.language, "churn"
        )

        result = {
            "success":    True,
            "will_churn": will_churn,
            "risk_score": risk_score,
            "verdict":    "⚠️ High Churn Risk" if will_churn else "✅ Customer Will Stay",
            "shap":       shap_dict,

            "explanation_points": explanation.get("explanation_points", []),
            "analogy":            explanation.get("analogy", ""),
            "transparency_score": explanation.get("transparency_score", 80),
            "churn_reasons":      explanation.get("rejection_reasons", []),
            "next_steps":         explanation.get("next_steps", []),
            "action_timeline":    explanation.get("reapply_timeline", ""),
            "improvement_tip":    explanation.get("improvement_tip", ""),
            "voice_summary":      explanation.get("voice_summary", ""),
            "explanation":        explanation
        }

        _log_prediction("churn", req.dict(), result)
        return result

    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Churn model not found! Run: python models/ml_models.py")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════
# WHAT-IF EXPLAIN
# ══════════════════════════════════════

@app.post("/api/whatif/explain")
async def whatif_api(req: WhatIfReq):
    try:
        data = await whatif_explain(
            req.original_inputs, req.modified_inputs,
            req.original_result, req.new_result,
            req.profile, req.language
        )
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════
# FEEDBACK
# ══════════════════════════════════════

@app.post("/api/feedback")
async def feedback_api(req: FeedbackReq):
    try:
        data = []
        if os.path.exists("feedback.json"):
            with open("feedback.json", "r") as f:
                data = json.load(f)

        data.append({
            "question": req.question,
            "answer":   req.answer,
            "rating":   req.rating,
            "profile":  req.profile,
            "language": req.language,
            "comment":  req.comment
        })

        with open("feedback.json", "w") as f:
            json.dump(data, f, indent=2)

        return {"success": True, "message": "Feedback saved! Thank you 🙏"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/feedback/stats")
def feedback_stats():
    try:
        if not os.path.exists("feedback.json"):
            return {"total": 0, "helpful": 0, "not_helpful": 0, "rate": "N/A"}

        with open("feedback.json", "r") as f:
            data = json.load(f)

        helpful    = sum(1 for d in data if d["rating"] >= 4)
        avg_rating = sum(d["rating"] for d in data) / len(data) if data else 0
        return {
            "total":       len(data),
            "helpful":     helpful,
            "not_helpful": len(data) - helpful,
            "avg_rating":  round(avg_rating, 2),
            "rate":        f"{helpful / len(data) * 100:.1f}%" if data else "N/A"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════
# HELPER — Prediction Logger
# ══════════════════════════════════════

def _log_prediction(pred_type, inputs, result):
    try:
        log_file = "predictions_log.json"
        logs = []
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = json.load(f)
        logs.append({
            "type":          pred_type,
            "inputs":        inputs,
            "prediction":    result.get("prediction") or result.get("verdict"),
            "confidence":    result.get("confidence") or result.get("risk_score"),
            "reasons":       result.get("rejection_reasons") or result.get("churn_reasons", []),
            "next_steps":    result.get("next_steps", []),
            "voice_summary": result.get("voice_summary", "")
        })
        with open(log_file, "w") as f:
            json.dump(logs[-500:], f, indent=2)  # keep last 500
    except:
        pass  # don't crash if logging fails


# ══════════════════════════════════════
# START SERVER
# ══════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("🏦  BankIQ Backend v3.0 Starting...")
    print("📖  API Docs    → http://localhost:8000/docs")
    print("🔥  Health      → http://localhost:8000/health")
    print("🌐  Languages   → http://localhost:8000/api/languages")
    print("🎤  Voice API   → POST /api/voice/ask")
    print("📞  Twilio IVR  → POST /api/twilio/voice")
    print("🌍  UI Labels   → GET  /api/ui/labels?language=Tamil")
    print("=" * 60)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
