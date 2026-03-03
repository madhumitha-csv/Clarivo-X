"""
twilio_service.py — BankIQ Twilio IVR Service
Handles all Twilio phone call IVR logic.
Extracted from main.py (routes) and claude_service.py (twilio_voice_response).
"""

from fastapi import Request
from fastapi.responses import Response
from services.voice_service import voice_ask

# ══════════════════════════════════════════════════════════════
# TWILIO VOICE HANDLER — IVR Menu Response
# Returns TwiML-ready text for phone callers
# ══════════════════════════════════════════════════════════════
async def twilio_voice_response(user_input: str, language: str = "English",
                                 call_stage: str = "greeting") -> dict:
    """
    Handles Twilio IVR flow.
    call_stage: greeting | language_select | main_menu | loan_query | churn_query | faq
    Returns: { twiml_text, next_stage, gather_options }
    """
    if call_stage == "greeting":
        return {
            "twiml_text": (
                "Welcome to BankIQ AI Banking Assistant. "
                "Press 1 for English. "
                "Press 2 for Tamil. "
                "Press 3 for Hindi. "
                "Press 4 for Telugu. "
                "Press 5 for Kannada."
            ),
            "next_stage": "language_select",
            "gather_options": ["1", "2", "3", "4", "5"]
        }

    lang_map = {"1": "English", "2": "Tamil", "3": "Hindi", "4": "Telugu", "5": "Kannada"}

    if call_stage == "language_select":
        selected_lang = lang_map.get(user_input, "English")
        menu_texts = {
            "English": "Press 1 to ask a banking question. Press 2 for loan guidance. Press 3 to check CIBIL tips. Press 0 to repeat menu.",
            "Tamil": "வங்கி கேள்வி கேட்க 1 அழுத்தவும். கடன் வழிகாட்டுதலுக்கு 2 அழுத்தவும். CIBIL குறிப்புகளுக்கு 3 அழுத்தவும்.",
            "Hindi": "बैंकिंग प्रश्न के लिए 1 दबाएं। ऋण मार्गदर्शन के लिए 2 दबाएं। CIBIL टिप्स के लिए 3 दबाएं।",
            "Telugu": "బ్యాంకింగ్ ప్రశ్న కోసం 1 నొక్కండి. రుణ మార్గదర్శకత్వం కోసం 2 నొక్కండి. CIBIL చిట్కాల కోసం 3 నొక్కండి.",
            "Kannada": "ಬ್ಯಾಂಕಿಂಗ್ ಪ್ರಶ್ನೆಗೆ 1 ಒತ್ತಿ. ಸಾಲ ಮಾರ್ಗದರ್ಶನಕ್ಕೆ 2 ಒತ್ತಿ. CIBIL ಸಲಹೆಗಾಗಿ 3 ಒತ್ತಿ."
        }
        return {
            "twiml_text": menu_texts.get(selected_lang, menu_texts["English"]),
            "next_stage": "main_menu",
            "selected_language": selected_lang,
            "gather_options": ["1", "2", "3", "0"]
        }

    if call_stage == "faq":
        # Answer via voice AI
        answer = await voice_ask(user_input, language=language)
        return {
            "twiml_text": answer + " Press 1 to ask another question or press 9 to end the call.",
            "next_stage": "main_menu",
            "gather_options": ["1", "9"]
        }

    # Default
    return {
        "twiml_text": "Thank you for calling BankIQ. Goodbye!",
        "next_stage": "end",
        "gather_options": []
    }


# ══════════════════════════════════════════════════════════════
# TWILIO INCOMING CALL — Route handler logic
# ══════════════════════════════════════════════════════════════
async def handle_incoming_call() -> Response:
    """
    Twilio webhook for incoming phone calls.
    Configure this URL in Twilio Console → Phone Number → Voice Webhook.
    Returns TwiML XML for IVR (Interactive Voice Response).
    """
    greeting_text = (
        "Welcome to BankIQ AI Banking Assistant. "
        "Press 1 for English. "
        "Press 2 for Tamil. "
        "Press 3 for Hindi. "
        "Press 4 for Malayalam. "
        "Press 5 for Kannada."
    )

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Aditi" language="en-IN">{greeting_text}</Say>
    <Gather numDigits="1" action="/api/twilio/gather?stage=language_select" method="POST" timeout="10">
        <Say voice="Polly.Aditi" language="en-IN">Please press your choice now.</Say>
    </Gather>
    <Say voice="Polly.Aditi" language="en-IN">We did not receive your input. Goodbye.</Say>
    <Hangup/>
</Response>"""

    return Response(content=twiml, media_type="application/xml")


async def handle_gather(request: Request, stage: str, user_sessions: dict) -> Response:
    """
    Handles digit/speech input from Twilio IVR.
    Progresses caller through: language_select → main_menu → faq
    """
    form = await request.form()
    digits       = form.get("Digits", "")
    speech       = form.get("SpeechResult", "")
    user_input   = speech if speech else digits

    lang_map = {"1": "English", "2": "Tamil", "3": "Hindi", "4": "Malayalam", "5": "Kannada"}

    call_sid = form.get("CallSid", "unknown")
    language = user_sessions.get(f"twilio_{call_sid}", {}).get("language", "English")

    if stage == "language_select":
        language = lang_map.get(digits, "English")
        user_sessions[f"twilio_{call_sid}"] = {"language": language}

        menus = {
            "English":   "Press 1 to ask a banking question. Press 2 for loan tips. Press 3 for CIBIL advice. Press 9 to hang up.",
            "Tamil":     "வங்கி கேள்வி கேட்க 1 அழுத்தவும். கடன் குறிப்புகளுக்கு 2 அழுத்தவும். CIBIL ஆலோசனைக்கு 3 அழுத்தவும்.",
            "Hindi":     "बैंकिंग प्रश्न के लिए 1 दबाएं। ऋण सुझाव के लिए 2 दबाएं। सीबिल सलाह के लिए 3 दबाएं।",
            "Malayalam": "ബ്യാങ്കിംഗ് ചോദ്യത്തിന് 1 അമർത്തൂ. ലോൺ നുറുങ്ങുകൾക്ക് 2 അമർത്തൂ. CIBIL ഉപദേശത്തിന് 3 അമർത്തൂ.",
            "Kannada":   "ಬ್ಯಾಂಕಿಂಗ್ ಪ್ರಶ್ನೆಗೆ 1 ಒತ್ತಿ. ಸಾಲ ಸಲಹೆಗೆ 2 ಒತ್ತಿ. CIBIL ಸಲಹೆಗೆ 3 ಒತ್ತಿ."
        }

        lang_voices = {
            "English":   ("Polly.Aditi",  "en-IN"),
            "Tamil":     ("Polly.Aditi",  "en-IN"),
            "Hindi":     ("Polly.Aditi",  "hi-IN"),
            "Malayalam": ("Polly.Aditi",  "en-IN"),
            "Kannada":   ("Polly.Aditi",  "en-IN")
        }
        voice, lang_code = lang_voices.get(language, ("Polly.Aditi", "en-IN"))
        menu_text = menus.get(language, menus["English"])

        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="{voice}" language="{lang_code}">{menu_text}</Say>
    <Gather numDigits="1" action="/api/twilio/gather?stage=main_menu&amp;lang={language}" method="POST" timeout="10">
    </Gather>
    <Redirect>/api/twilio/gather?stage=language_select</Redirect>
</Response>"""
        return Response(content=twiml, media_type="application/xml")

    elif stage == "main_menu":
        language = request.query_params.get("lang", language)
        faq_map = {
            "1": "What is CIBIL score and how does it affect my loan?",
            "2": "How can I improve my chances of getting a loan approved?",
            "3": "What is the minimum CIBIL score needed for a loan?"
        }
        question = faq_map.get(digits, "What is CIBIL score?")

        if digits == "9":
            twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Aditi" language="en-IN">Thank you for calling BankIQ. Have a great day! Goodbye.</Say>
    <Hangup/>
</Response>"""
            return Response(content=twiml, media_type="application/xml")

        answer = await voice_ask(question, language=language, profile="Elder")
        answer_clean = answer.replace("&", "and").replace("<", "").replace(">", "")

        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Aditi" language="en-IN">{answer_clean}</Say>
    <Gather numDigits="1" action="/api/twilio/gather?stage=main_menu&amp;lang={language}" method="POST" timeout="10">
        <Say voice="Polly.Aditi" language="en-IN">Press 1 to ask another question, or press 9 to end the call.</Say>
    </Gather>
    <Hangup/>
</Response>"""
        return Response(content=twiml, media_type="application/xml")

    # Default end
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Aditi" language="en-IN">Thank you for using BankIQ. Goodbye!</Say>
    <Hangup/>
</Response>"""
    return Response(content=twiml, media_type="application/xml")
