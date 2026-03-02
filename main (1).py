"""
main.py — ClarivoX Backend
Run: python main.py
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn, json, os

from claude_service import ask_claude, shap_to_plain, simplify, whatif_explain
from ml_models import predict_loan, predict_churn

app = FastAPI(title="ClarivoX API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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

# ══════════════════════════════════════
# ROUTES
# ══════════════════════════════════════

@app.get("/")
def root():
    return {
        "status": "ClarivoX API Running! 🚀",
        "version": "2.0",
        "docs": "http://localhost:8000/docs",
        "endpoints": [
            "GET  /health",
            "POST /api/ask",
            "POST /api/simplify",
            "POST /api/loan/predict",
            "POST /api/churn/predict",
            "POST /api/whatif/explain",
            "POST /api/feedback",
            "GET  /api/feedback/stats"
        ]
    }

@app.get("/health")
def health():
    loan_ready  = os.path.exists("models/loan_model.pkl")
    churn_ready = os.path.exists("models/churn_model.pkl")
    return {
        "status": "healthy",
        "loan_model":  "✅ Ready" if loan_ready  else "❌ Run ml_models.py",
        "churn_model": "✅ Ready" if churn_ready else "❌ Run ml_models.py"
    }


# ── ASK BANKING QUESTION ──
@app.post("/api/ask")
async def ask(req: AskReq):
    try:
        history = [{"role": m.role, "content": m.content} for m in req.history]
        data = await ask_claude(
            req.question, req.profile,
            req.language, req.topic, history
        )
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── SIMPLIFY EXPLANATION ──
@app.post("/api/simplify")
async def simplify_api(req: SimplifyReq):
    try:
        data = await simplify(req.previous_answer, req.profile, req.language)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── LOAN PREDICTION — FULL WITH REASONS + NEXT STEPS ──
@app.post("/api/loan/predict")
async def loan_api(req: LoanReq):
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

        # Pass actual inputs so Groq can give specific reasons
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

        # ── Build full response with all fields ──
        result = {
            "success":    True,
            "prediction": "Approved" if approved else "Rejected",
            "confidence": confidence,
            "shap":       shap_dict,

            # Core explanation
            "explanation_points": explanation.get("explanation_points", []),
            "analogy":            explanation.get("analogy", ""),
            "transparency_score": explanation.get("transparency_score", 80),

            # ✅ NEW — Reasons why approved/rejected
            "rejection_reasons": explanation.get("rejection_reasons", []),

            # ✅ NEW — What to do next
            "next_steps": explanation.get("next_steps", []),

            # ✅ NEW — When to reapply
            "reapply_timeline": explanation.get("reapply_timeline", ""),

            # ✅ NEW — Single most important tip
            "improvement_tip": explanation.get("improvement_tip", ""),

            # Full explanation object for frontend
            "explanation": explanation
        }

        # ── Log prediction to file (replace with DB later) ──
        _log_prediction("loan", loan_inputs, result)

        return result

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Loan model not found! Run: python ml_models.py"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── CHURN PREDICTION — FULL WITH REASONS + NEXT STEPS ──
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

            # Core explanation
            "explanation_points": explanation.get("explanation_points", []),
            "analogy":            explanation.get("analogy", ""),
            "transparency_score": explanation.get("transparency_score", 80),

            # ✅ NEW — Churn signals
            "churn_reasons": explanation.get("rejection_reasons", []),

            # ✅ NEW — Bank actions to retain
            "next_steps": explanation.get("next_steps", []),

            # ✅ NEW — Urgency timeline
            "action_timeline": explanation.get("reapply_timeline", ""),

            # ✅ NEW — Top retention tip
            "improvement_tip": explanation.get("improvement_tip", ""),

            "explanation": explanation
        }

        _log_prediction("churn", req.dict(), result)
        return result

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Churn model not found! Run: python ml_models.py"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── WHAT-IF EXPLAIN ──
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


# ── FEEDBACK ──
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

        helpful = sum(1 for d in data if d["rating"] >= 4)
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


# ── HELPER — Log predictions to JSON (replace with DB later) ──
def _log_prediction(pred_type, inputs, result):
    try:
        log_file = "predictions_log.json"
        logs = []
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = json.load(f)
        logs.append({
            "type":       pred_type,
            "inputs":     inputs,
            "prediction": result.get("prediction") or result.get("verdict"),
            "confidence": result.get("confidence") or result.get("risk_score"),
            "reasons":    result.get("rejection_reasons") or result.get("churn_reasons", []),
            "next_steps": result.get("next_steps", [])
        })
        with open(log_file, "w") as f:
            json.dump(logs[-500:], f, indent=2)  # keep last 500
    except:
        pass  # don't crash if logging fails


# ══════════════════════════════════════
# START SERVER
# ══════════════════════════════════════
if __name__ == "__main__":
    print("=" * 55)
    print("🏦  ClarivoX Backend v2.0 Starting...")
    print("📖  API Docs  → http://localhost:8000/docs")
    print("🔥  Health    → http://localhost:8000/health")
    print("=" * 55)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)