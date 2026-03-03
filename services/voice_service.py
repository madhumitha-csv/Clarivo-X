"""
voice_service.py — BankIQ Voice AI Service
Handles voice-optimised plain-text responses for TTS and Twilio.
Extracted from claude_service.py.
"""

from groq import Groq

# ── Paste your Groq API key here ──
client = Groq(api_key="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")

PROFILES = {
    "Student":      "Explain using school/college analogies. Simple words. No banking jargon.",
    "Professional": "Use proper financial terms. Be concise and data-driven. SHAP values are fine.",
    "Elder":        "Very simple language. Use daily life examples like shops, farming, household. Be warm and friendly.",
    "Business":     "Use business-oriented language. Focus on ROI, risk, and strategy.",
    "Farmer":       "Use farming/agriculture analogies. Very simple words. Be warm and respectful."
}

LANGS = {
    "Tamil":     "CRITICAL INSTRUCTION: You MUST write ALL text in Tamil language (தமிழ்) ONLY. Every single word in explanation_points, rejection_reasons, next_steps, reapply_timeline, improvement_tip, analogy, voice_summary MUST be in Tamil script. NO English words allowed except proper nouns like CIBIL, EMI, SHAP.",
    "Hindi":     "CRITICAL INSTRUCTION: You MUST write ALL text in Hindi language (हिंदी) ONLY. Every single word in explanation_points, rejection_reasons, next_steps, reapply_timeline, improvement_tip, analogy, voice_summary MUST be in Hindi/Devanagari script. NO English words allowed except proper nouns like CIBIL, EMI, SHAP.",
    "Telugu":    "CRITICAL INSTRUCTION: You MUST write ALL text in Telugu language (తెలుగు) ONLY. Every single word in explanation_points, rejection_reasons, next_steps, reapply_timeline, improvement_tip, analogy, voice_summary MUST be in Telugu script. NO English words allowed except proper nouns like CIBIL, EMI, SHAP.",
    "Kannada":   "CRITICAL INSTRUCTION: You MUST write ALL text in Kannada language (ಕನ್ನಡ) ONLY. Every single word in explanation_points, rejection_reasons, next_steps, reapply_timeline, improvement_tip, analogy, voice_summary MUST be in Kannada script. NO English words allowed except proper nouns like CIBIL, EMI, SHAP.",
    "Malayalam": "CRITICAL INSTRUCTION: You MUST write ALL text in Malayalam language (മലയാളം) ONLY. Every single word in explanation_points, rejection_reasons, next_steps, reapply_timeline, improvement_tip, analogy, voice_summary MUST be in Malayalam script. NO English words allowed except proper nouns like CIBIL, EMI, SHAP.",
    "Marathi":   "CRITICAL INSTRUCTION: You MUST write ALL text in Marathi language (मराठी) ONLY. Every single word MUST be in Devanagari script. NO English words allowed except proper nouns like CIBIL, EMI, SHAP.",
    "Bengali":   "CRITICAL INSTRUCTION: You MUST write ALL text in Bengali language (বাংলা) ONLY. Every single word MUST be in Bengali script. NO English words allowed except proper nouns like CIBIL, EMI, SHAP.",
    "English":   "Respond in clear simple English."
}


# ══════════════════════════════════════════════════
# VOICE CHATBOT — Twilio-friendly plain text
#    Returns plain text (no JSON) for TTS/phone use
# ══════════════════════════════════════════════════
async def voice_ask(question: str, language: str = "English", profile: str = "Student") -> str:
    """
    Returns a SHORT plain-text answer suitable for:
    - Text-to-Speech (TTS) in browser
    - Twilio phone call TwiML response
    - Voice assistant playback
    """
    lang_instr = LANGS.get(language, LANGS["English"])
    prof_instr = PROFILES.get(profile, PROFILES["Student"])

    system = f"""{prof_instr}
{lang_instr}
You are BankIQ voice assistant. Answer in 2-3 SHORT sentences only.
No bullet points. No JSON. No special characters. Plain spoken language only.
This answer will be read aloud, so write naturally as if speaking.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": question}
            ],
            temperature=0.4,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"voice_ask error: {e}")
        return "Sorry, I could not answer your question. Please try again."
