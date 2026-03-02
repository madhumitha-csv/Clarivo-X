"""
claude_service.py — ClarivoX
Groq FREE API — llama-3.3-70b-versatile
pip install groq
"""

import json
import re
from groq import Groq

# ── Paste your Groq API key here ──
client = Groq(api_key="your-groq-api-key-here")

PROFILES = {
    "Student":      "Explain using school/college analogies. Simple words. No banking jargon.",
    "Professional": "Use proper financial terms. Be concise and data-driven. SHAP values are fine.",
    "Elder":        "Very simple language. Use daily life examples like shops, farming, household. Be warm and friendly."
}

LANGS = {
    "Tamil":   "Respond entirely in Tamil language (தமிழ்). Use Tamil script only.",
    "Hindi":   "Respond entirely in Hindi language (हिंदी). Use Hindi script only.",
    "Telugu":  "Respond entirely in Telugu language (తెలుగు). Use Telugu script only.",
    "Kannada": "Respond entirely in Kannada language (ಕನ್ನಡ). Use Kannada script only.",
    "English": "Respond in English."
}

def safe_json(text):
    text = text.strip()
    text = re.sub(r"^```json|^```|```$", "", text, flags=re.MULTILINE).strip()
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
        return None


# ══════════════════════════════════════════════════
# 1. MAIN CHAT — Ask Banking Question
# ══════════════════════════════════════════════════
async def ask_claude(question, profile, language, topic, history=[]):
    lang_instr = LANGS.get(language, LANGS["English"])
    prof_instr = PROFILES.get(profile, PROFILES["Student"])

    system = f"""{prof_instr}
{lang_instr}
Topic area: {topic}

You are ClarivoX — an AI banking assistant that explains banking decisions simply.
Reply ONLY as valid JSON with no extra text outside JSON:
{{
  "answer": "2-3 sentence direct answer to the question",
  "confidence": "high/medium/low",
  "explanation_points": ["point1", "point2", "point3"],
  "analogy": "simple everyday analogy matching the profile",
  "follow_up_questions": ["question1?", "question2?"]
}}"""

    messages = [{"role": "system", "content": system}]
    for m in history[-6:]:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.5,
            max_tokens=800
        )
        text = response.choices[0].message.content
        result = safe_json(text)
        if result:
            return result
    except Exception as e:
        print(f"ask_claude error: {e}")

    return {
        "answer": "I apologize, I could not process your question. Please try again.",
        "confidence": "low",
        "explanation_points": ["Try rephrasing your question", "Make sure backend is running"],
        "analogy": "Like a phone call that dropped — try again!",
        "follow_up_questions": ["What is EMI?", "How to improve CIBIL score?"]
    }


# ══════════════════════════════════════════════════
# 2. LOAN / CHURN EXPLANATION
#    Returns: reasons + next_steps + reapply_timeline
# ══════════════════════════════════════════════════
async def shap_to_plain(shap_dict, prediction, profile, language, model_type,
                         loan_inputs=None):
    lang_instr = LANGS.get(language, LANGS["English"])
    prof_instr = PROFILES.get(profile, PROFILES["Student"])

    sorted_shap = sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
    positive_factors = [(f, v) for f, v in sorted_shap if v > 0]
    negative_factors = [(f, v) for f, v in sorted_shap if v < 0]

    pos_summary = ", ".join([f"{f.replace('_',' ')} (+{v:.2f})" for f, v in positive_factors[:3]])
    neg_summary = ", ".join([f"{f.replace('_',' ')} ({v:.2f})" for f, v in negative_factors[:3]])

    # Build extra context from actual inputs
    input_context = ""
    if loan_inputs and model_type == "loan":
        cibil   = loan_inputs.get("cibil_score", "?")
        income  = loan_inputs.get("income", "?")
        loan_am = loan_inputs.get("loan_amount", "?")
        income_str  = f"Rs.{income:,.0f}"  if isinstance(income,  (int, float)) else str(income)
        loan_am_str = f"Rs.{loan_am:,.0f}" if isinstance(loan_am, (int, float)) else str(loan_am)
        input_context = f"""
Actual values entered:
- CIBIL Score     : {cibil}
- Annual Income   : {income_str}
- Loan Amount     : {loan_am_str}
"""

    if model_type == "loan":
        verdict = "APPROVED" if prediction else "REJECTED"
        prompt = f"""
Loan application was {verdict}.
{input_context}
Positive SHAP factors (helped): {pos_summary if pos_summary else 'None'}
Negative SHAP factors (hurt)  : {neg_summary if neg_summary else 'None'}

Profile: {profile}
{prof_instr}
{lang_instr}

{"Since REJECTED — give specific reasons and clear action steps to improve and reapply." if not prediction else "Since APPROVED — explain why and what to do next to maintain this."}

Reply ONLY as valid JSON (no extra text):
{{
  "explanation_points": [
    "Factor 1 that most influenced decision — explain simply",
    "Factor 2 that influenced decision",
    "Factor 3 that influenced decision"
  ],
  "rejection_reasons": [
    "Main reason 1 why loan was {'rejected' if not prediction else 'approved'} — be specific with numbers",
    "Reason 2 — specific",
    "Reason 3 — specific"
  ],
  "next_steps": [
    "Step 1 — specific action to take {'to get approved' if not prediction else 'to maintain approval'}",
    "Step 2 — specific action",
    "Step 3 — specific action"
  ],
  "reapply_timeline": "{'Specific timeline like After 6 months when CIBIL improves' if not prediction else 'You are approved — proceed with documentation now'}",
  "improvement_tip": "Single most important thing to {'improve chances next time' if not prediction else 'maintain good standing'}",
  "analogy": "Simple daily life analogy matching {profile} profile",
  "transparency_score": 85
}}"""

    else:  # churn
        verdict = "LIKELY TO LEAVE" if prediction else "LIKELY TO STAY"
        prompt = f"""
Customer churn prediction: {verdict}.
Churn risk factors (negative SHAP): {neg_summary if neg_summary else 'None'}
Loyalty factors (positive SHAP)   : {pos_summary if pos_summary else 'None'}

Profile: {profile}
{prof_instr}
{lang_instr}

{"Since customer will LEAVE — give specific retention actions the bank should take." if prediction else "Since customer STAYS — explain positive signals and how to keep them."}

Reply ONLY as valid JSON (no extra text):
{{
  "explanation_points": [
    "Factor 1 that indicates {'churn risk' if prediction else 'loyalty'} — explain simply",
    "Factor 2",
    "Factor 3"
  ],
  "rejection_reasons": [
    "Main churn signal 1 — specific",
    "Churn signal 2 — specific",
    "Churn signal 3 — specific"
  ],
  "next_steps": [
    "Bank action 1 to {'retain' if prediction else 'reward'} this customer",
    "Bank action 2",
    "Bank action 3"
  ],
  "reapply_timeline": "{'How urgently bank must act — e.g. Within 2 weeks' if prediction else 'Next review timeline'}",
  "improvement_tip": "Single most important {'retention' if prediction else 'engagement'} action",
  "analogy": "Simple daily life analogy matching {profile} profile",
  "transparency_score": 82
}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"{prof_instr} {lang_instr} Reply only in valid JSON. No text outside JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        text = response.choices[0].message.content
        result = safe_json(text)
        if result:
            return result
    except Exception as e:
        print(f"shap_to_plain error: {e}")

    # ── FALLBACK — rule based using actual SHAP ──
    top_neg = negative_factors[0][0].replace("_", " ") if negative_factors else "credit score"
    top_pos = positive_factors[0][0].replace("_", " ") if positive_factors else "assets"

    if model_type == "loan":
        if prediction:
            return {
                "explanation_points": [
                    f"Your {top_pos} strongly supported your application",
                    "Your income is sufficient for the requested loan amount",
                    "Your CIBIL score met the minimum required threshold"
                ],
                "rejection_reasons": [
                    f"Strong {top_pos} was the key approval factor",
                    "Good income-to-loan ratio",
                    "Sufficient asset coverage provided security"
                ],
                "next_steps": [
                    "✅ Proceed with loan documentation immediately",
                    "📋 Maintain CIBIL score by paying all EMIs on time",
                    "🚫 Do not take additional loans while this is active"
                ],
                "reapply_timeline": "Loan approved — visit bank branch with documents now!",
                "improvement_tip": "Pay every EMI on time — this keeps your CIBIL score high for future loans",
                "analogy": "Like passing an exam with good marks — you qualified, now collect your certificate!",
                "transparency_score": 82
            }
        else:
            return {
                "explanation_points": [
                    f"Your {top_neg} was below the required threshold",
                    "The loan amount is high relative to your income",
                    "Additional financial commitments reduced eligibility"
                ],
                "rejection_reasons": [
                    f"❌ {top_neg.title()} did not meet the minimum criteria",
                    "❌ Loan-to-income ratio is too high",
                    "❌ Insufficient collateral assets"
                ],
                "next_steps": [
                    "📈 Improve CIBIL score: Pay ALL existing dues on time for 6 months",
                    "💰 Reduce existing debt: Close small loans/credit cards first",
                    "📊 Apply for a smaller loan amount — try 50% of current amount"
                ],
                "reapply_timeline": "Reapply after 6 months once CIBIL score crosses 750",
                "improvement_tip": "CIBIL score above 750 is the single biggest factor — focus on this first",
                "analogy": "Like needing 60% to pass an exam — study more and reappear next semester!",
                "transparency_score": 80
            }
    else:
        if prediction:
            return {
                "explanation_points": [
                    "Customer has raised multiple complaints — very dissatisfied",
                    "Low account balance shows reduced engagement with bank",
                    "Inactive membership status indicates customer is drifting away"
                ],
                "rejection_reasons": [
                    "⚠️ High complaint count — unresolved issues",
                    "⚠️ Low balance and product usage",
                    "⚠️ Satisfaction score below average"
                ],
                "next_steps": [
                    "📞 Call customer within 24 hours with personal apology",
                    "🎁 Offer loyalty bonus — interest waiver or cashback",
                    "✅ Resolve all pending complaints within 48 hours"
                ],
                "reapply_timeline": "Act within 2 weeks — after that customer is likely gone",
                "improvement_tip": "Resolve complaints immediately — that alone reduces churn by 40%",
                "analogy": "Like a regular at your shop who stopped coming — visit them personally now!",
                "transparency_score": 78
            }
        else:
            return {
                "explanation_points": [
                    f"Strong {top_pos} signals long-term loyalty",
                    "Customer is actively using multiple bank products",
                    "High satisfaction score shows positive experience"
                ],
                "rejection_reasons": [
                    "✅ Good tenure — loyal customer",
                    "✅ Multiple products — deeply engaged",
                    "✅ High satisfaction — happy with service"
                ],
                "next_steps": [
                    "🎁 Reward loyalty — offer exclusive interest rates",
                    "📱 Introduce new products that match their profile",
                    "💬 Send quarterly satisfaction check-in"
                ],
                "reapply_timeline": "Next churn review in 3 months — customer is stable",
                "improvement_tip": "Keep engaging with personalized offers to maintain this loyalty",
                "analogy": "Like a loyal customer at your favourite restaurant — they keep coming back!",
                "transparency_score": 85
            }


# ══════════════════════════════════════════════════
# 3. SIMPLIFY — Make Explanation Even Simpler
# ══════════════════════════════════════════════════
async def simplify(prev_answer, profile, language):
    lang_instr = LANGS.get(language, LANGS["English"])
    prof_instr = PROFILES.get(profile, PROFILES["Student"])

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"{prof_instr} {lang_instr} Reply only in valid JSON."},
                {"role": "user", "content": f"""
Make this explanation even simpler for a {profile}: "{prev_answer}"
Use one very simple sentence and a daily life analogy.
Reply ONLY as valid JSON:
{{
  "explanation_points": ["One very simple sentence explanation"],
  "analogy": "Very simple daily life analogy (shop, school, farm, kitchen)",
  "next_steps": ["One simple action they can take right now"]
}}"""}
            ],
            temperature=0.4,
            max_tokens=300
        )
        text = response.choices[0].message.content
        result = safe_json(text)
        if result:
            return result
    except Exception as e:
        print(f"simplify error: {e}")

    return {
        "explanation_points": ["The AI made a decision based on your financial information"],
        "analogy": "Like a teacher grading your exam based on your answers",
        "next_steps": ["Ask the AI a specific question for more details"]
    }


# ══════════════════════════════════════════════════
# 4. WHAT-IF EXPLANATION
# ══════════════════════════════════════════════════
async def whatif_explain(original_inputs, modified_inputs, original_result, new_result, profile, language):
    lang_instr = LANGS.get(language, LANGS["English"])
    prof_instr = PROFILES.get(profile, PROFILES["Student"])

    changes = []
    for key in modified_inputs:
        if key in original_inputs and original_inputs[key] != modified_inputs[key]:
            changes.append(f"{key.replace('_',' ')}: {original_inputs[key]} → {modified_inputs[key]}")

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"{prof_instr} {lang_instr} Reply only in valid JSON."},
                {"role": "user", "content": f"""
What-If Analysis:
Changes made: {', '.join(changes) if changes else 'No changes'}
Original result: {original_result}
New result: {new_result}

Explain clearly what changed and why it helped or hurt.
Reply ONLY as valid JSON:
{{
  "what_changed": "Simple explanation of what the person changed",
  "why_it_helped": "Why this change improved or worsened the decision",
  "key_insight": "Most important insight from this simulation",
  "next_best_action": "What to change next to improve further"
}}"""}
            ],
            temperature=0.4,
            max_tokens=400
        )
        text = response.choices[0].message.content
        result = safe_json(text)
        if result:
            return result
    except Exception as e:
        print(f"whatif_explain error: {e}")

    return {
        "what_changed": f"You changed: {', '.join(changes)}",
        "why_it_helped": "These changes affected the key factors the model evaluates",
        "key_insight": "CIBIL score and income are the most impactful factors",
        "next_best_action": "Try improving your CIBIL score above 750 for best results"
    }