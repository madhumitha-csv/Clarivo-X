"""
claude_service.py — BankIQ Enhanced
Features:
  - Multilingual AI responses (Tamil, Hindi, Telugu, Kannada, English)
  - Loan rejection reasons + approval guidance
  - Personalized chatbot with conversation memory
  - Voice-friendly response formatting
  - What-if analysis explanations
pip install groq
"""

import json
import re
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

# Translated fallback messages for when Groq API fails
FALLBACK_MSGS = {
    "English": {
        "loan_approved_exp": ["Your CIBIL score strongly supported your application", "Your income is sufficient for the loan amount", "Your assets provided good security"],
        "loan_approved_steps": ["✅ Proceed with loan documentation immediately", "📋 Pay all EMIs on time to maintain CIBIL score", "🚫 Avoid taking additional loans while this is active"],
        "loan_approved_tip": "Pay every EMI on time to keep your CIBIL score high",
        "loan_approved_voice": "Great news! Your loan has been approved.",
        "loan_approved_timeline": "Loan approved — visit bank branch with documents now!",
        "loan_rejected_exp": ["Your CIBIL score was below the required threshold", "The loan amount is high relative to your income", "Insufficient collateral assets"],
        "loan_rejected_steps": ["📈 Improve CIBIL score: Pay ALL dues on time for 6 months", "💰 Reduce existing debt: Close small loans first", "📊 Apply for a smaller loan amount"],
        "loan_rejected_tip": "CIBIL score above 750 is the single biggest factor — focus on this first",
        "loan_rejected_voice": "Your loan was rejected. Improve your CIBIL score and reapply in 6 months.",
        "loan_rejected_timeline": "Reapply after 6 months once CIBIL score crosses 750",
        "churn_yes_exp": ["Customer has raised multiple complaints", "Low account balance shows reduced engagement", "Inactive membership indicates customer is drifting away"],
        "churn_yes_steps": ["📞 Call customer within 24 hours with personal apology", "🎁 Offer loyalty bonus — cashback or interest waiver", "✅ Resolve all pending complaints within 48 hours"],
        "churn_yes_tip": "Resolve complaints immediately — that alone reduces churn by 40%",
        "churn_yes_voice": "High churn risk detected. Immediate retention action required.",
        "churn_yes_timeline": "Act within 2 weeks — after that customer is likely gone",
        "churn_no_exp": ["Strong loyalty signals detected", "Customer actively uses multiple bank products", "High satisfaction score shows positive experience"],
        "churn_no_steps": ["🎁 Reward loyalty — offer exclusive interest rates", "📱 Introduce new products matching their profile", "💬 Send quarterly satisfaction check-in"],
        "churn_no_tip": "Keep engaging with personalized offers to maintain loyalty",
        "churn_no_voice": "Customer is loyal and likely to stay. Keep up the good service.",
        "churn_no_timeline": "Next churn review in 3 months — customer is stable",
        "analogy_pass": "Like passing an exam — you qualified, now collect your certificate!",
        "analogy_fail": "Like needing 60% to pass — study more and reappear next semester!",
        "analogy_churn": "Like a regular at your shop who stopped coming — visit them personally!",
        "analogy_loyal": "Like a loyal customer at your favourite restaurant — they keep coming back!",
    },
    "Tamil": {
        "loan_approved_exp": ["உங்கள் CIBIL மதிப்பெண் விண்ணப்பத்தை வலுவாக ஆதரித்தது", "கடன் தொகைக்கு உங்கள் வருமானம் போதுமானது", "உங்கள் சொத்துக்கள் நல்ல பாதுகாப்பை வழங்கின"],
        "loan_approved_steps": ["✅ உடனடியாக கடன் ஆவணங்களை தயாரிக்கவும்", "📋 CIBIL மதிப்பெண்ணை பராமரிக்க EMI சரியான நேரத்தில் செலுத்தவும்", "🚫 இந்த கடன் செயலில் இருக்கும்போது கூடுதல் கடன் வாங்க வேண்டாம்"],
        "loan_approved_tip": "ஒவ்வொரு EMI-ஐயும் சரியான நேரத்தில் செலுத்துங்கள் — இது CIBIL மதிப்பெண்ணை உயர்வாக வைக்கும்",
        "loan_approved_voice": "நல்ல செய்தி! உங்கள் கடன் விண்ணப்பம் அனுமதிக்கப்பட்டது.",
        "loan_approved_timeline": "கடன் அனுமதிக்கப்பட்டது — இப்போதே வங்கிக் கிளைக்கு ஆவணங்களுடன் செல்லுங்கள்!",
        "loan_rejected_exp": ["உங்கள் CIBIL மதிப்பெண் தேவையான அளவை விட குறைவாக இருந்தது", "கடன் தொகை வருமானத்துடன் ஒப்பிடும்போது அதிகமாக உள்ளது", "போதுமான சொத்து பாதுகாப்பு இல்லை"],
        "loan_rejected_steps": ["📈 CIBIL மேம்படுத்து: 6 மாதம் அனைத்து நிலுவைகளையும் சரியான நேரத்தில் செலுத்துங்கள்", "💰 ஏற்கனவே உள்ள கடன்களை குறைக்கவும்: முதலில் சிறிய கடன்களை மூடுங்கள்", "📊 குறைந்த கடன் தொகைக்கு விண்ணப்பிக்கவும்"],
        "loan_rejected_tip": "750-க்கு மேல் CIBIL மதிப்பெண் மிக முக்கியமான காரணி — இதில் கவனம் செலுத்துங்கள்",
        "loan_rejected_voice": "கடன் நிராகரிக்கப்பட்டது. CIBIL மதிப்பெண்ணை மேம்படுத்தி 6 மாதங்களில் மீண்டும் விண்ணப்பிக்கவும்.",
        "loan_rejected_timeline": "CIBIL மதிப்பெண் 750 கடந்த பிறகு 6 மாதங்களில் மீண்டும் விண்ணப்பிக்கவும்",
        "churn_yes_exp": ["வாடிக்கையாளர் பல புகார்கள் தெரிவித்துள்ளார்", "குறைந்த கணக்கு இருப்பு ஈடுபாடு குறைவதை காட்டுகிறது", "செயலற்ற உறுப்பினர் நிலை வாடிக்கையாளர் விலகுவதை காட்டுகிறது"],
        "churn_yes_steps": ["📞 தனிப்பட்ட மன்னிப்புடன் 24 மணி நேரத்தில் வாடிக்கையாளரை அழைக்கவும்", "🎁 விசுவாச போனஸ் வழங்கவும் — கேஷ்பேக் அல்லது வட்டி தள்ளுபடி", "✅ அனைத்து நிலுவை புகார்களையும் 48 மணி நேரத்தில் தீர்க்கவும்"],
        "churn_yes_tip": "புகார்களை உடனடியாக தீர்க்கவும் — இது மட்டுமே வாடிக்கையாளர் இழப்பை 40% குறைக்கும்",
        "churn_yes_voice": "அதிக வாடிக்கையாளர் இழப்பு அபாயம் கண்டறியப்பட்டது. உடனடி நடவடிக்கை தேவை.",
        "churn_yes_timeline": "2 வாரங்களுக்குள் செயல்படுங்கள் — அதற்குப் பிறகு வாடிக்கையாளர் போய்விடுவார்",
        "churn_no_exp": ["வலுவான விசுவாச சமிக்ஞைகள் கண்டறியப்பட்டன", "வாடிக்கையாளர் பல வங்கி தயாரிப்புகளை பயன்படுத்துகிறார்", "அதிக திருப்தி மதிப்பெண் நேர்மறையான அனுபவத்தை காட்டுகிறது"],
        "churn_no_steps": ["🎁 விசுவாசத்திற்கு வெகுமதி — சிறப்பு வட்டி விகிதங்கள் வழங்கவும்", "📱 அவர்களின் சுயவிவரத்திற்கு பொருந்தும் புதிய தயாரிப்புகளை அறிமுகப்படுத்தவும்", "💬 காலாண்டு திருப்தி கண்காணிப்பு அனுப்பவும்"],
        "churn_no_tip": "விசுவாசத்தை பராமரிக்க தனிப்பயன் சலுகைகளுடன் தொடர்ந்து ஈடுபடுங்கள்",
        "churn_no_voice": "வாடிக்கையாளர் விசுவாசமானவர், தொடர்வார். நல்ல சேவையை தொடருங்கள்.",
        "churn_no_timeline": "3 மாதங்களில் அடுத்த வாடிக்கையாளர் இழப்பு மதிப்பாய்வு — வாடிக்கையாளர் நிலையானவர்",
        "analogy_pass": "தேர்வில் தேர்ச்சி பெற்றது போல் — தகுதி பெற்றீர்கள், இப்போது சான்றிதழ் வாங்குங்கள்!",
        "analogy_fail": "தேர்வில் 60% தேவை போல் — இன்னும் படித்து அடுத்த தேர்வில் வெற்றி பெறுங்கள்!",
        "analogy_churn": "வழக்கமாக வரும் கடை வாடிக்கையாளர் நிறுத்தியது போல் — இப்போதே நேரில் சந்தியுங்கள்!",
        "analogy_loyal": "விரும்பிய உணவகத்தின் விசுவாச வாடிக்கையாளர் போல் — திரும்பவும் வருவார்!",
    },
    "Hindi": {
        "loan_approved_exp": ["आपका CIBIL स्कोर ने आवेदन को मजबूती से समर्थन दिया", "ऋण राशि के लिए आपकी आय पर्याप्त है", "आपकी संपत्तियों ने अच्छी सुरक्षा प्रदान की"],
        "loan_approved_steps": ["✅ तुरंत ऋण दस्तावेज़ तैयार करें", "📋 CIBIL स्कोर बनाए रखने के लिए समय पर EMI चुकाएं", "🚫 इस ऋण के सक्रिय रहते अतिरिक्त ऋण न लें"],
        "loan_approved_tip": "हर EMI समय पर चुकाएं — इससे भविष्य के लिए CIBIL स्कोर ऊंचा रहेगा",
        "loan_approved_voice": "बधाई हो! आपका ऋण आवेदन स्वीकृत हो गया है।",
        "loan_approved_timeline": "ऋण स्वीकृत — अभी बैंक शाखा में दस्तावेज़ लेकर जाएं!",
        "loan_rejected_exp": ["आपका CIBIL स्कोर आवश्यक सीमा से कम था", "ऋण राशि आय की तुलना में अधिक है", "पर्याप्त संपार्श्विक संपत्ति नहीं है"],
        "loan_rejected_steps": ["📈 CIBIL सुधारें: 6 महीने सभी बकाया समय पर चुकाएं", "💰 मौजूदा कर्ज कम करें: पहले छोटे ऋण बंद करें", "📊 कम ऋण राशि के लिए आवेदन करें"],
        "loan_rejected_tip": "750 से ऊपर CIBIL स्कोर सबसे महत्वपूर्ण कारक है — पहले इस पर ध्यान दें",
        "loan_rejected_voice": "ऋण अस्वीकृत हुआ। CIBIL स्कोर सुधारें और 6 महीने में फिर आवेदन करें।",
        "loan_rejected_timeline": "CIBIL स्कोर 750 पार होने के बाद 6 महीने में फिर आवेदन करें",
        "churn_yes_exp": ["ग्राहक ने कई शिकायतें दर्ज की हैं", "कम खाता शेष कम जुड़ाव दिखाता है", "निष्क्रिय सदस्यता दिखाती है कि ग्राहक दूर जा रहा है"],
        "churn_yes_steps": ["📞 व्यक्तिगत माफी के साथ 24 घंटे में ग्राहक को कॉल करें", "🎁 वफादारी बोनस दें — कैशबैक या ब्याज छूट", "✅ सभी लंबित शिकायतें 48 घंटे में हल करें"],
        "churn_yes_tip": "शिकायतें तुरंत हल करें — इससे अकेले ग्राहक हानि 40% कम होती है",
        "churn_yes_voice": "उच्च ग्राहक हानि जोखिम पाया गया। तत्काल कार्रवाई आवश्यक है।",
        "churn_yes_timeline": "2 सप्ताह में काम करें — उसके बाद ग्राहक के जाने की संभावना है",
        "churn_no_exp": ["मजबूत वफादारी संकेत मिले", "ग्राहक कई बैंक उत्पाद सक्रिय रूप से उपयोग करता है", "उच्च संतुष्टि स्कोर सकारात्मक अनुभव दिखाता है"],
        "churn_no_steps": ["🎁 वफादारी का इनाम दें — विशेष ब्याज दर", "📱 उनकी प्रोफाइल से मेल खाते नए उत्पाद पेश करें", "💬 तिमाही संतुष्टि जांच भेजें"],
        "churn_no_tip": "वफादारी बनाए रखने के लिए व्यक्तिगत ऑफर के साथ जुड़ते रहें",
        "churn_no_voice": "ग्राहक वफादार है और रहने की संभावना है। अच्छी सेवा जारी रखें।",
        "churn_no_timeline": "3 महीने में अगली चर्न समीक्षा — ग्राहक स्थिर है",
        "analogy_pass": "परीक्षा पास करने जैसा — आप योग्य हैं, अब प्रमाण पत्र लीजिए!",
        "analogy_fail": "60% चाहिए जैसा — और पढ़ें और अगली परीक्षा दें!",
        "analogy_churn": "दुकान का नियमित ग्राहक आना बंद हो गया — अभी जाकर मिलें!",
        "analogy_loyal": "पसंदीदा रेस्टोरेंट का वफादार ग्राहक — वे वापस आते रहते हैं!",
    },
    "Telugu": {
        "loan_approved_exp": ["మీ CIBIL స్కోర్ దరఖాస్తును బలంగా మద్దతు ఇచ్చింది", "లోన్ మొత్తానికి మీ ఆదాయం సరిపోతుంది", "మీ ఆస్తులు మంచి భద్రతను అందించాయి"],
        "loan_approved_steps": ["✅ వెంటనే లోన్ పత్రాలు సిద్ధం చేయండి", "📋 CIBIL స్కోర్ నిర్వహించడానికి సకాలంలో EMI చెల్లించండి", "🚫 ఈ లోన్ సక్రియంగా ఉన్నప్పుడు అదనపు లోన్లు తీసుకోకండి"],
        "loan_approved_tip": "ప్రతి EMI సకాలంలో చెల్లించండి — ఇది CIBIL స్కోర్ ఎక్కువగా ఉంచుతుంది",
        "loan_approved_voice": "శుభవార్త! మీ లోన్ దరఖాస్తు అనుమతించబడింది.",
        "loan_approved_timeline": "లోన్ అనుమతించబడింది — ఇప్పుడే పత్రాలతో బ్యాంక్ శాఖకు వెళ్ళండి!",
        "loan_rejected_exp": ["మీ CIBIL స్కోర్ అవసరమైన స్థాయి కంటే తక్కువగా ఉంది", "లోన్ మొత్తం ఆదాయంతో పోల్చితే ఎక్కువగా ఉంది", "తగినంత హామీ ఆస్తులు లేవు"],
        "loan_rejected_steps": ["📈 CIBIL మెరుగుపరచండి: 6 నెలలు అన్ని బకాయిలు సకాలంలో చెల్లించండి", "💰 ఉన్న అప్పులు తగ్గించండి: మొదట చిన్న లోన్లు మూసివేయండి", "📊 తక్కువ లోన్ మొత్తానికి దరఖాస్తు చేయండి"],
        "loan_rejected_tip": "750 పైన CIBIL స్కోర్ అతి ముఖ్యమైన అంశం — ముందు దీనిపై దృష్టి పెట్టండి",
        "loan_rejected_voice": "లోన్ తిరస్కరించబడింది. CIBIL స్కోర్ మెరుగుపరచి 6 నెలల్లో మళ్ళీ దరఖాస్తు చేయండి.",
        "loan_rejected_timeline": "CIBIL స్కోర్ 750 దాటిన తర్వాత 6 నెలల్లో మళ్ళీ దరఖాస్తు చేయండి",
        "churn_yes_exp": ["కస్టమర్ అనేక ఫిర్యాదులు నమోదు చేశారు", "తక్కువ బ్యాలెన్స్ తక్కువ నిమగ్నత చూపిస్తుంది", "నిష్క్రియ సభ్యత్వం కస్టమర్ దూరమవుతున్నట్లు చూపిస్తుంది"],
        "churn_yes_steps": ["📞 వ్యక్తిగత క్షమాపణతో 24 గంటల్లో కస్టమర్‌కు కాల్ చేయండి", "🎁 విధేయత బోనస్ ఇవ్వండి — క్యాష్‌బ్యాక్ లేదా వడ్డీ మినహాయింపు", "✅ అన్ని పెండింగ్ ఫిర్యాదులు 48 గంటల్లో పరిష్కరించండి"],
        "churn_yes_tip": "ఫిర్యాదులు వెంటనే పరిష్కరించండి — ఇది మాత్రమే చర్న్‌ను 40% తగ్గిస్తుంది",
        "churn_yes_voice": "అధిక చర్న్ రిస్క్ గుర్తించబడింది. తక్షణ చర్య అవసరం.",
        "churn_yes_timeline": "2 వారాల్లో చర్య తీసుకోండి — తర్వాత కస్టమర్ వెళ్ళిపోయే అవకాశం ఉంది",
        "churn_no_exp": ["బలమైన విధేయత సంకేతాలు గుర్తించబడ్డాయి", "కస్టమర్ అనేక బ్యాంక్ ఉత్పత్తులను చురుగ్గా ఉపయోగిస్తున్నారు", "అధిక సంతృప్తి స్కోర్ సానుకూల అనుభవాన్ని చూపిస్తుంది"],
        "churn_no_steps": ["🎁 విధేయతకు బహుమతి — ప్రత్యేక వడ్డీ రేట్లు", "📱 వారి ప్రొఫైల్‌కు నప్పే కొత్త ఉత్పత్తులు పరిచయం చేయండి", "💬 త్రైమాసిక సంతృప్తి తనిఖీ పంపండి"],
        "churn_no_tip": "విధేయత నిలబెట్టుకోవడానికి వ్యక్తిగతీకరించిన ఆఫర్‌లతో నిరంతరం నిమగ్నమవ్వండి",
        "churn_no_voice": "కస్టమర్ విధేయంగా ఉన్నారు మరియు ఉండే అవకాశం ఉంది. మంచి సేవ కొనసాగించండి.",
        "churn_no_timeline": "3 నెలల్లో తదుపరి చర్న్ సమీక్ష — కస్టమర్ స్థిరంగా ఉన్నారు",
        "analogy_pass": "పరీక్షలో పాస్ అయినట్లు — అర్హత సాధించారు, ఇప్పుడు సర్టిఫికేట్ తీసుకోండి!",
        "analogy_fail": "60% కావాలని — ఇంకా చదివి తదుపరి పరీక్షలో వెళ్ళండి!",
        "analogy_churn": "మీ దుకాణానికి వచ్చే నిత్య కస్టమర్ ఆగిపోయినట్లు — ఇప్పుడే వెళ్ళి కలవండి!",
        "analogy_loyal": "మీకు ఇష్టమైన రెస్టారెంట్ యొక్క విశ్వాసపాత్రుడైన కస్టమర్ — వారు తిరిగి వస్తారు!",
    },
    "Kannada": {
        "loan_approved_exp": ["ನಿಮ್ಮ CIBIL ಸ್ಕೋರ್ ಅರ್ಜಿಯನ್ನು ಬಲವಾಗಿ ಬೆಂಬಲಿಸಿತು", "ಸಾಲದ ಮೊತ್ತಕ್ಕೆ ನಿಮ್ಮ ಆದಾಯ ಸಾಕಾಗುತ್ತದೆ", "ನಿಮ್ಮ ಆಸ್ತಿಗಳು ಉತ್ತಮ ಭದ್ರತೆ ಒದಗಿಸಿದವು"],
        "loan_approved_steps": ["✅ ತಕ್ಷಣ ಸಾಲದ ದಾಖಲೆಗಳನ್ನು ತಯಾರಿಸಿ", "📋 CIBIL ಸ್ಕೋರ್ ಕಾಪಾಡಲು ಸಮಯಕ್ಕೆ EMI ಪಾವತಿಸಿ", "🚫 ಈ ಸಾಲ ಸಕ್ರಿಯವಾಗಿರುವಾಗ ಹೆಚ್ಚುವರಿ ಸಾಲ ತೆಗೆಯಬೇಡಿ"],
        "loan_approved_tip": "ಪ್ರತಿ EMI ಸಮಯಕ್ಕೆ ಪಾವತಿಸಿ — ಇದು CIBIL ಸ್ಕೋರ್ ಎತ್ತರದಲ್ಲಿ ಇಡುತ್ತದೆ",
        "loan_approved_voice": "ಶುಭ ಸುದ್ದಿ! ನಿಮ್ಮ ಸಾಲದ ಅರ್ಜಿ ಅನುಮೋದಿಸಲಾಗಿದೆ.",
        "loan_approved_timeline": "ಸಾಲ ಅನುಮೋದಿಸಲಾಗಿದೆ — ಈಗಲೇ ದಾಖಲೆಗಳೊಂದಿಗೆ ಬ್ಯಾಂಕ್ ಶಾಖೆಗೆ ಹೋಗಿ!",
        "loan_rejected_exp": ["ನಿಮ್ಮ CIBIL ಸ್ಕೋರ್ ಅಗತ್ಯ ಮಿತಿಗಿಂತ ಕಡಿಮೆ ಇತ್ತು", "ಸಾಲದ ಮೊತ್ತ ಆದಾಯಕ್ಕೆ ಹೋಲಿಸಿದರೆ ಹೆಚ್ಚಾಗಿದೆ", "ಸಾಕಷ್ಟು ಭದ್ರತಾ ಆಸ್ತಿ ಇಲ್ಲ"],
        "loan_rejected_steps": ["📈 CIBIL ಸುಧಾರಿಸಿ: 6 ತಿಂಗಳು ಎಲ್ಲಾ ಬಾಕಿಗಳನ್ನು ಸಮಯಕ್ಕೆ ಪಾವತಿಸಿ", "💰 ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ ಸಾಲ ಕಡಿಮೆ ಮಾಡಿ: ಮೊದಲು ಚಿಕ್ಕ ಸಾಲಗಳನ್ನು ಮುಚ್ಚಿ", "📊 ಕಡಿಮೆ ಸಾಲದ ಮೊತ್ತಕ್ಕೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ"],
        "loan_rejected_tip": "750 ಮೇಲೆ CIBIL ಸ್ಕೋರ್ ಅತ್ಯಂತ ಮುಖ್ಯ ಅಂಶ — ಮೊದಲು ಇದರ ಮೇಲೆ ಗಮನಹರಿಸಿ",
        "loan_rejected_voice": "ಸಾಲ ತಿರಸ್ಕರಿಸಲಾಗಿದೆ. CIBIL ಸ್ಕೋರ್ ಸುಧಾರಿಸಿ 6 ತಿಂಗಳಲ್ಲಿ ಮತ್ತೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.",
        "loan_rejected_timeline": "CIBIL ಸ್ಕೋರ್ 750 ದಾಟಿದ ನಂತರ 6 ತಿಂಗಳಲ್ಲಿ ಮತ್ತೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
        "churn_yes_exp": ["ಗ್ರಾಹಕರು ಹಲವಾರು ದೂರುಗಳನ್ನು ದಾಖಲಿಸಿದ್ದಾರೆ", "ಕಡಿಮೆ ಶಿಲ್ಕು ಕಡಿಮೆ ತೊಡಗಿಸಿಕೊಳ್ಳುವಿಕೆ ತೋರಿಸುತ್ತದೆ", "ನಿಷ್ಕ್ರಿಯ ಸದಸ್ಯತ್ವ ಗ್ರಾಹಕರು ದೂರ ಹೋಗುತ್ತಿದ್ದಾರೆ ಎಂದು ತೋರಿಸುತ್ತದೆ"],
        "churn_yes_steps": ["📞 ವೈಯಕ್ತಿಕ ಕ್ಷಮೆಯಾಚನೆಯೊಂದಿಗೆ 24 ಗಂಟೆಯಲ್ಲಿ ಗ್ರಾಹಕರನ್ನು ಕರೆ ಮಾಡಿ", "🎁 ನಿಷ್ಠಾ ಬೋನಸ್ ನೀಡಿ — ಕ್ಯಾಶ್‌ಬ್ಯಾಕ್ ಅಥವಾ ಬಡ್ಡಿ ಮಿನಹಾಯಿಸಿ", "✅ ಎಲ್ಲಾ ಬಾಕಿ ದೂರುಗಳನ್ನು 48 ಗಂಟೆಯಲ್ಲಿ ಪರಿಹರಿಸಿ"],
        "churn_yes_tip": "ದೂರುಗಳನ್ನು ತಕ್ಷಣ ಪರಿಹರಿಸಿ — ಇದು ಮಾತ್ರ ಗ್ರಾಹಕ ನಷ್ಟವನ್ನು 40% ಕಡಿಮೆ ಮಾಡುತ್ತದೆ",
        "churn_yes_voice": "ಹೆಚ್ಚಿನ ಗ್ರಾಹಕ ನಷ್ಟ ಅಪಾಯ ಪತ್ತೆಯಾಗಿದೆ. ತಕ್ಷಣ ಕ್ರಮ ಅಗತ್ಯ.",
        "churn_yes_timeline": "2 ವಾರಗಳಲ್ಲಿ ಕ್ರಮ ತೆಗೆದುಕೊಳ್ಳಿ — ನಂತರ ಗ್ರಾಹಕರು ಹೋಗಬಹುದು",
        "churn_no_exp": ["ಬಲವಾದ ನಿಷ್ಠಾ ಸಂಕೇತಗಳು ಪತ್ತೆಯಾಗಿವೆ", "ಗ್ರಾಹಕರು ಅನೇಕ ಬ್ಯಾಂಕ್ ಉತ್ಪನ್ನಗಳನ್ನು ಸಕ್ರಿಯವಾಗಿ ಬಳಸುತ್ತಿದ್ದಾರೆ", "ಹೆಚ್ಚಿನ ತೃಪ್ತಿ ಸ್ಕೋರ್ ಧನಾತ್ಮಕ ಅನುಭವ ತೋರಿಸುತ್ತದೆ"],
        "churn_no_steps": ["🎁 ನಿಷ್ಠೆಗೆ ಪ್ರತಿಫಲ — ವಿಶೇಷ ಬಡ್ಡಿ ದರಗಳು", "📱 ಅವರ ಪ್ರೊಫೈಲ್‌ಗೆ ಸರಿಹೊಂದುವ ಹೊಸ ಉತ್ಪನ್ನಗಳನ್ನು ಪರಿಚಯಿಸಿ", "💬 ತ್ರೈಮಾಸಿಕ ತೃಪ್ತಿ ಪರಿಶೀಲನೆ ಕಳುಹಿಸಿ"],
        "churn_no_tip": "ನಿಷ್ಠೆ ಕಾಪಾಡಲು ವೈಯಕ್ತಿಕ ಆಫರ್‌ಗಳೊಂದಿಗೆ ನಿರಂತರ ತೊಡಗಿಸಿಕೊಳ್ಳಿ",
        "churn_no_voice": "ಗ್ರಾಹಕರು ನಿಷ್ಠಾವಂತರು ಮತ್ತು ಉಳಿಯಬಹುದು. ಒಳ್ಳೆಯ ಸೇವೆ ಮುಂದುವರಿಸಿ.",
        "churn_no_timeline": "3 ತಿಂಗಳಲ್ಲಿ ಮುಂದಿನ ಚರ್ನ್ ಪರಿಶೀಲನೆ — ಗ್ರಾಹಕರು ಸ್ಥಿರವಾಗಿದ್ದಾರೆ",
        "analogy_pass": "ಪರೀಕ್ಷೆ ಪಾಸ್ ಮಾಡಿದಂತೆ — ಅರ್ಹರಾಗಿದ್ದೀರಿ, ಈಗ ಪ್ರಮಾಣಪತ್ರ ತೆಗೆಕೊಳ್ಳಿ!",
        "analogy_fail": "60% ಬೇಕು ಎಂದಂತೆ — ಇನ್ನಷ್ಟು ಓದಿ ಮುಂದಿನ ಪರೀಕ್ಷೆ ಬರೆಯಿರಿ!",
        "analogy_churn": "ನಿಮ್ಮ ಅಂಗಡಿಗೆ ಬರುತ್ತಿದ್ದ ಗ್ರಾಹಕರು ನಿಂತಂತೆ — ಈಗಲೇ ಭೇಟಿ ಮಾಡಿ!",
        "analogy_loyal": "ನೆಚ್ಚಿನ ರೆಸ್ಟೋರೆಂಟ್‌ನ ನಿಷ್ಠಾವಂತ ಗ್ರಾಹಕರಂತೆ — ಅವರು ಮತ್ತೆ ಬರುತ್ತಾರೆ!",
    },
    "Malayalam": {
        "loan_approved_exp": ["നിങ്ങളുടെ CIBIL സ്കോർ അപേക്ഷയെ ശക്തമായി പിന്തുണച്ചു", "ലോൺ തുകയ്ക്ക് നിങ്ങളുടെ വരുമാനം മതിയാകുന്നു", "നിങ്ങളുടെ ആസ്തികൾ നല്ല സുരക്ഷ നൽകി"],
        "loan_approved_steps": ["✅ ഉടനടി ലോൺ രേഖകൾ തയ്യാറാക്കുക", "📋 CIBIL സ്കോർ നിലനിർത്താൻ EMI സമയത്ത് അടയ്ക്കുക", "🚫 ഈ ലോൺ സജീവമായിരിക്കുമ്പോൾ അധിക ലോണുകൾ എടുക്കരുത്"],
        "loan_approved_tip": "എല്ലാ EMI-യും സമയത്ത് അടയ്ക്കുക — ഇത് CIBIL സ്കോർ ഉയർന്നു നിലനിർത്തും",
        "loan_approved_voice": "സന്തോഷ വാർത്ത! നിങ്ങളുടെ ലോൺ അപേക്ഷ അനുവദിച്ചു.",
        "loan_approved_timeline": "ലോൺ അനുവദിച്ചു — ഇപ്പോൾ തന്നെ രേഖകളുമായി ബ്യാങ്ക് ശാഖയിൽ പോകുക!",
        "loan_rejected_exp": ["നിങ്ങളുടെ CIBIL സ്കോർ ആവശ്യമായ നിലവാരത്തിൽ ഇല്ലായിരുന്നു", "ലോൺ തുക വരുമാനവുമായി താരതമ്യം ചെയ്യുമ്പോൾ കൂടുതലാണ്", "ആവശ്യമായ ജാമ്യ ആസ്തികൾ ഇല്ല"],
        "loan_rejected_steps": ["📈 CIBIL മെച്ചപ്പെടുത്തുക: 6 മാസം എല്ലാ കുടിശ്ശിക സമയത്ത് അടയ്ക്കുക", "💰 നിലവിലുള്ള കടം കുറക്കുക: ആദ്യം ചെറിയ ലോണുകൾ അടക്കുക", "📊 കുറഞ്ഞ ലോൺ തുകയ്ക്ക് അപേക്ഷിക്കുക"],
        "loan_rejected_tip": "750-ന് മുകളിൽ CIBIL സ്കോർ ഏറ്റവും പ്രധാന ഘടകം — ആദ്യം ഇതിൽ ശ്രദ്ധ കേന്ദ്രീകരിക്കുക",
        "loan_rejected_voice": "ലോൺ നിരസിച്ചു. CIBIL സ്കോർ മെച്ചപ്പെടുത്തി 6 മാസത്തിൽ വീണ്ടും അപേക്ഷിക്കുക.",
        "loan_rejected_timeline": "CIBIL സ്കോർ 750 കടന്നതിന് ശേഷം 6 മാസത്തിൽ വീണ്ടും അപേക്ഷിക്കുക",
        "churn_yes_exp": ["ഉപഭോക്താവ് നിരവധി പരാതികൾ നൽകിയിട്ടുണ്ട്", "കുറഞ്ഞ ബ്യാലൻസ് കുറഞ്ഞ ഇടപഴകൽ കാണിക്കുന്നു", "നിഷ്ക്രിയ അംഗത്വം ഉപഭോക്താവ് ദൂരം പോകുന്നതായി കാണിക്കുന്നു"],
        "churn_yes_steps": ["📞 വ്യക്തിഗത ക്ഷമാപണത്തോടെ 24 മണിക്കൂറിൽ ഉപഭോക്താവിനെ വിളിക്കുക", "🎁 വിശ്വസ്തതാ ബോണസ് നൽകുക — ക്യാഷ്ബ്യാക്ക് അല്ലെങ്കിൽ പലിശ ഇളവ്", "✅ എല്ലാ തീർപ്പാക്കാത്ത പരാതികളും 48 മണിക്കൂറിൽ പരിഹരിക്കുക"],
        "churn_yes_tip": "പരാതികൾ ഉടനടി പരിഹരിക്കുക — ഇത് മാത്രം ചേർൺ 40% കുറക്കും",
        "churn_yes_voice": "ഉയർന്ന ചേർൺ റിസ്ക് കണ്ടെത്തി. ഉടനടി നടപടി ആവശ്യമാണ്.",
        "churn_yes_timeline": "2 ആഴ്ചക്കുള്ളിൽ നടപടി എടുക്കുക — അതിനുശേഷം ഉപഭോക്താവ് പോകാൻ സാധ്യതയുണ്ട്",
        "churn_no_exp": ["ശക്തമായ വിശ്വസ്തതാ സൂചനകൾ കണ്ടെത്തി", "ഉപഭോക്താവ് ഒന്നിലധികം ബ്യാങ്ക് ഉൽപ്പന്നങ്ങൾ സജീവമായി ഉപയോഗിക്കുന്നു", "ഉയർന്ന സംതൃപ്തി സ്കോർ നല്ല അനുഭവം കാണിക്കുന്നു"],
        "churn_no_steps": ["🎁 വിശ്വസ്തതയ്ക്ക് പ്രതിഫലം — പ്രത്യേക പലിശ നിരക്കുകൾ", "📱 അവരുടെ പ്രൊഫൈലിന് അനുയോജ്യമായ പുതിയ ഉൽപ്പന്നങ്ങൾ അവതരിപ്പിക്കുക", "💬 ത്രൈമാസ സംതൃപ്തി പരിശോധന അയക്കുക"],
        "churn_no_tip": "വിശ്വസ്തത നിലനിർത്താൻ വ്യക്തിഗതമാക്കിയ ഓഫറുകളിൽ തുടർന്നും ഇടപഴകുക",
        "churn_no_voice": "ഉപഭോക്താവ് വിശ്വസ്തനാണ് തുടരും. നല്ല സേവനം തുടരുക.",
        "churn_no_timeline": "3 മാസത്തിൽ അടുത്ത ചേർൺ അവലോകനം — ഉപഭോക്താവ് സ്ഥിരനാണ്",
        "analogy_pass": "പരീക്ഷ പാസ്സായതു പോലെ — യോഗ്യത നേടി, ഇപ്പോൾ സർട്ടിഫിക്കറ്റ് വാങ്ങൂ!",
        "analogy_fail": "60% വേണം പോലെ — കൂടുതൽ പഠിച്ച് അടുത്ത പരീക്ഷ എഴുതൂ!",
        "analogy_churn": "നിങ്ങളുടെ കടയിൽ വന്നിരുന്ന സ്ഥിരം ഉപഭോക്താവ് നിർത്തിയതു പോലെ — ഇപ്പോൾ നേരിൽ കാണൂ!",
        "analogy_loyal": "ഇഷ്ടമുള്ള റെസ്റ്റോറന്റിലെ വിശ്വസ്ത ഉപഭോക്താവിനെ പോലെ — അവർ തിരിച്ചു വരും!",
    },
}

# UI labels for full website localization
UI_TRANSLATIONS = {
    "English": {
        # Login
        "welcome": "Welcome to BankIQ",
        "select_language": "Select your preferred language",
        "select_profile": "Select your profile",
        "language_prompt": "Please select your preferred language to continue",
        "login": "Login", "logout": "Logout", "username": "Username",
        # Nav tabs
        "nav_home": "🏠 Home", "nav_loan": "🏦 Loan Check",
        "nav_churn": "📊 Churn", "nav_chat": "🤖 AI Chat",
        # Hero
        "hero_title": "AI-Powered Banking\nMade Simple",
        "hero_sub": "Explainable decisions. Voice support. Your language. For everyone.",
        "card_loan_title": "Loan Eligibility", "card_loan_sub": "Check approval chances with AI explanation",
        "card_churn_title": "Churn Analysis", "card_churn_sub": "Predict if a customer will stay or leave",
        "card_chat_title": "Voice AI Chat", "card_chat_sub": "Ask anything in your language by voice",
        # Loan page
        "loan_check": "Loan Eligibility Check", "loan_form_title": "Enter Loan Details",
        "label_income": "Annual Income (₹)", "label_loan_amt": "Loan Amount (₹)",
        "label_cibil": "CIBIL Score", "label_term": "Loan Term (months)",
        "label_edu": "Education", "label_self": "Self Employed",
        "label_dep": "Dependents", "label_res": "Residential Assets (₹)",
        "btn_check_loan": "🔍 Check Eligibility",
        "opt_graduate": "Graduate", "opt_notgraduate": "Not Graduate",
        "opt_yes": "Yes", "opt_no": "No",
        # Churn page
        "churn_check": "Customer Churn Analysis", "churn_form_title": "Customer Details",
        "label_credit": "Credit Score", "label_age": "Age",
        "label_tenure": "Tenure (years)", "label_balance": "Balance (₹)",
        "label_products": "No. of Products", "label_sat": "Satisfaction (1-5)",
        "label_complaints": "Complaints Filed", "label_active": "Active Member?",
        "btn_check_churn": "🔍 Analyze Churn Risk",
        # Chat page
        "chat": "AI Banking Assistant", "chat_placeholder": "Type your question...",
        "chat_welcome": "👋 Hello! I am BankIQ, your AI banking assistant. Ask me anything about loans, CIBIL, EMI in your own language!",
        "fq1": "What is CIBIL score?", "fq2": "How to improve loan chances?",
        "fq3": "What is EMI?", "fq4": "Increase CIBIL fast",
        # Results
        "approved": "✅ Approved", "rejected": "❌ Rejected",
        "why_approved": "✅ Why Approved", "why_rejected": "❌ Why Rejected",
        "next_steps": "📋 Next Steps", "factor_impact": "📈 Factor Impact",
        "risk_signals": "⚠️ Risk Signals", "loyalty_signals": "✅ Loyalty Signals",
        "bank_actions": "🎯 Recommended Actions",
        "reapply_in": "You can reapply in", "improvement_tip": "Key improvement tip",
        "speak": "🎤 Speak", "stop": "⏹ Stop", "listen": "🔊 Listen",
        "churn_risk": "Churn Risk", "will_stay": "✅ Will Stay", "will_leave": "⚠️ High Churn Risk",
        "confidence": "Confidence",
        # Profile
        "profile_student": "Student", "profile_professional": "Professional",
        "profile_elder": "Elder", "profile_business": "Business",
        "profile_farmer": "Farmer", "profile_other": "Other",
        "enter_btn": "Enter BankIQ 🚀", "change_lang": "Change Language", "btn_cancel": "Cancel",
    },
    "Tamil": {
        "welcome": "BankIQ-க்கு வரவேற்கிறோம்",
        "select_language": "உங்கள் மொழியை தேர்ந்தெடுக்கவும்",
        "select_profile": "உங்கள் சுயவிவரத்தை தேர்ந்தெடுக்கவும்",
        "language_prompt": "தொடர உங்கள் மொழியை தேர்ந்தெடுக்கவும்",
        "login": "உள்நுழைவு", "logout": "வெளியேறு", "username": "பயனர்பெயர்",
        "nav_home": "🏠 முகப்பு", "nav_loan": "🏦 கடன் சரிபார்",
        "nav_churn": "📊 வாடிக்கையாளர்", "nav_chat": "🤖 AI உரை",
        "hero_title": "AI வங்கி சேவை\nஎளிமையாக்கப்பட்டது",
        "hero_sub": "தெளிவான முடிவுகள். குரல் ஆதரவு. உங்கள் மொழியில். அனைவருக்கும்.",
        "card_loan_title": "கடன் தகுதி", "card_loan_sub": "AI விளக்கத்துடன் அனுமதி வாய்ப்பு சரிபார்க்கவும்",
        "card_churn_title": "வாடிக்கையாளர் பகுப்பு", "card_churn_sub": "வாடிக்கையாளர் தங்குவாரா போவாரா கணிக்கவும்",
        "card_chat_title": "குரல் AI உரை", "card_chat_sub": "உங்கள் மொழியில் குரல் மூலம் கேளுங்கள்",
        "loan_check": "கடன் தகுதி சரிபார்ப்பு", "loan_form_title": "கடன் விவரங்களை உள்ளிடவும்",
        "label_income": "வருடாந்திர வருமானம் (₹)", "label_loan_amt": "கடன் தொகை (₹)",
        "label_cibil": "CIBIL மதிப்பெண்", "label_term": "கடன் காலம் (மாதங்கள்)",
        "label_edu": "கல்வி", "label_self": "சுயதொழில்",
        "label_dep": "சார்ந்திருப்பவர்கள்", "label_res": "குடியிருப்பு சொத்துக்கள் (₹)",
        "btn_check_loan": "🔍 தகுதி சரிபார்க்கவும்",
        "opt_graduate": "பட்டதாரி", "opt_notgraduate": "பட்டதாரி இல்லை",
        "opt_yes": "ஆம்", "opt_no": "இல்லை",
        "churn_check": "வாடிக்கையாளர் வெளியேற்ற பகுப்பாய்வு", "churn_form_title": "வாடிக்கையாளர் விவரங்கள்",
        "label_credit": "கிரெடிட் மதிப்பெண்", "label_age": "வயது",
        "label_tenure": "காலம் (ஆண்டுகள்)", "label_balance": "இருப்பு (₹)",
        "label_products": "தயாரிப்புகள்", "label_sat": "திருப்தி (1-5)",
        "label_complaints": "புகார்கள்", "label_active": "செயலில் உள்ளவரா?",
        "btn_check_churn": "🔍 வெளியேற்ற அபாயம் பகுப்பாய்வு",
        "chat": "AI வங்கி உதவியாளர்", "chat_placeholder": "உங்கள் கேள்வியை தட்டச்சு செய்யுங்கள்...",
        "chat_welcome": "👋 வணக்கம்! நான் BankIQ, உங்கள் AI வங்கி உதவியாளர். கடன், CIBIL, EMI பற்றி எதுவும் கேளுங்கள் — உங்கள் மொழியில்!",
        "fq1": "CIBIL என்றால் என்ன?", "fq2": "கடன் வாய்ப்பை மேம்படுத்துவது எப்படி?",
        "fq3": "EMI என்றால் என்ன?", "fq4": "CIBIL வேகமாக அதிகரிக்க",
        "approved": "✅ அனுமதிக்கப்பட்டது", "rejected": "❌ நிராகரிக்கப்பட்டது",
        "why_approved": "✅ ஏன் அனுமதிக்கப்பட்டது", "why_rejected": "❌ ஏன் நிராகரிக்கப்பட்டது",
        "next_steps": "📋 அடுத்த படிகள்", "factor_impact": "📈 காரணி தாக்கம்",
        "risk_signals": "⚠️ அபாய சமிக்ஞைகள்", "loyalty_signals": "✅ விசுவாச சமிக்ஞைகள்",
        "bank_actions": "🎯 பரிந்துரைக்கப்பட்ட நடவடிக்கைகள்",
        "reapply_in": "மீண்டும் விண்ணப்பிக்கலாம்", "improvement_tip": "முக்கிய மேம்பாட்டு குறிப்பு",
        "speak": "🎤 பேசுங்கள்", "stop": "⏹ நிறுத்து", "listen": "🔊 கேளுங்கள்",
        "churn_risk": "வாடிக்கையாளர் இழப்பு அபாயம்",
        "will_stay": "✅ வாடிக்கையாளர் தங்குவார்", "will_leave": "⚠️ அதிக இழப்பு அபாயம்",
        "confidence": "நம்பகத்தன்மை",
        "profile_student": "மாணவர்", "profile_professional": "தொழில்முறையாளர்",
        "profile_elder": "முதியவர்", "profile_business": "வணிகம்",
        "profile_farmer": "விவசாயி", "profile_other": "மற்றவர்",
        "enter_btn": "BankIQ-ல் நுழைக 🚀", "change_lang": "மொழி மாற்றவும்", "btn_cancel": "ரத்து செய்",
    },
    "Hindi": {
        "welcome": "BankIQ में आपका स्वागत है",
        "select_language": "अपनी भाषा चुनें", "select_profile": "अपनी प्रोफ़ाइल चुनें",
        "language_prompt": "जारी रखने के लिए अपनी भाषा चुनें",
        "login": "लॉगिन", "logout": "लॉगआउट", "username": "उपयोगकर्ता नाम",
        "nav_home": "🏠 होम", "nav_loan": "🏦 लोन जांच",
        "nav_churn": "📊 चर्न", "nav_chat": "🤖 AI चैट",
        "hero_title": "AI बैंकिंग\nसरल बनाया गया",
        "hero_sub": "स्पष्ट निर्णय। आवाज़ सहायता। आपकी भाषा में। सभी के लिए।",
        "card_loan_title": "लोन पात्रता", "card_loan_sub": "AI स्पष्टीकरण के साथ अनुमोदन जांचें",
        "card_churn_title": "चर्न विश्लेषण", "card_churn_sub": "ग्राहक रहेगा या जाएगा अनुमान लगाएं",
        "card_chat_title": "वॉयस AI चैट", "card_chat_sub": "अपनी भाषा में बैंकिंग के बारे में पूछें",
        "loan_check": "लोन पात्रता जांच", "loan_form_title": "लोन विवरण दर्ज करें",
        "label_income": "वार्षिक आय (₹)", "label_loan_amt": "लोन राशि (₹)",
        "label_cibil": "CIBIL स्कोर", "label_term": "लोन अवधि (महीने)",
        "label_edu": "शिक्षा", "label_self": "स्व-रोज़गार",
        "label_dep": "आश्रित", "label_res": "आवासीय संपत्ति (₹)",
        "btn_check_loan": "🔍 पात्रता जांचें",
        "opt_graduate": "स्नातक", "opt_notgraduate": "गैर-स्नातक",
        "opt_yes": "हाँ", "opt_no": "नहीं",
        "churn_check": "ग्राहक चर्न विश्लेषण", "churn_form_title": "ग्राहक विवरण",
        "label_credit": "क्रेडिट स्कोर", "label_age": "आयु",
        "label_tenure": "कार्यकाल (वर्ष)", "label_balance": "शेष (₹)",
        "label_products": "उत्पाद संख्या", "label_sat": "संतुष्टि (1-5)",
        "label_complaints": "शिकायतें", "label_active": "सक्रिय सदस्य?",
        "btn_check_churn": "🔍 चर्न जोखिम विश्लेषण",
        "chat": "AI बैंकिंग सहायक", "chat_placeholder": "अपना प्रश्न लिखें...",
        "chat_welcome": "👋 नमस्ते! मैं BankIQ हूं, आपका AI बैंकिंग सहायक। लोन, CIBIL, EMI के बारे में कुछ भी पूछें!",
        "fq1": "CIBIL स्कोर क्या है?", "fq2": "लोन कैसे मिलेगा?",
        "fq3": "EMI क्या है?", "fq4": "CIBIL जल्दी बढ़ाएं",
        "approved": "✅ स्वीकृत", "rejected": "❌ अस्वीकृत",
        "why_approved": "✅ स्वीकृत क्यों", "why_rejected": "❌ अस्वीकृत क्यों",
        "next_steps": "📋 अगले कदम", "factor_impact": "📈 कारक प्रभाव",
        "risk_signals": "⚠️ जोखिम संकेत", "loyalty_signals": "✅ वफादारी संकेत",
        "bank_actions": "🎯 अनुशंसित कार्रवाई",
        "reapply_in": "पुनः आवेदन कर सकते हैं", "improvement_tip": "मुख्य सुधार सुझाव",
        "speak": "🎤 बोलें", "stop": "⏹ रोकें", "listen": "🔊 सुनें",
        "churn_risk": "ग्राहक छोड़ने का जोखिम",
        "will_stay": "✅ ग्राहक रहेगा", "will_leave": "⚠️ अधिक जोखिम",
        "confidence": "विश्वास स्तर",
        "profile_student": "छात्र", "profile_professional": "पेशेवर",
        "profile_elder": "वरिष्ठ", "profile_business": "व्यापार",
        "profile_farmer": "किसान", "profile_other": "अन्य",
        "enter_btn": "BankIQ में प्रवेश करें 🚀", "change_lang": "भाषा बदलें", "btn_cancel": "रद्द करें",
    },
    "Telugu": {
        "welcome": "BankIQ కి స్వాగతం",
        "select_language": "మీ భాషను ఎంచుకోండి", "select_profile": "మీ ప్రొఫైల్ ఎంచుకోండి",
        "language_prompt": "కొనసాగించడానికి మీ భాషను ఎంచుకోండి",
        "login": "లాగిన్", "logout": "లాగ్అవుట్", "username": "వినియోగదారు పేరు",
        "nav_home": "🏠 హోమ్", "nav_loan": "🏦 లోన్ తనిఖీ",
        "nav_churn": "📊 చర్న్", "nav_chat": "🤖 AI చాట్",
        "hero_title": "AI బ్యాంకింగ్\nసరళంగా మార్చబడింది",
        "hero_sub": "స్పష్టమైన నిర్ణయాలు. వాయిస్ సపోర్ట్. మీ భాషలో. అందరికీ.",
        "card_loan_title": "లోన్ అర్హత", "card_loan_sub": "AI వివరణతో అనుమతి అవకాశాలు తనిఖీ చేయండి",
        "card_churn_title": "చర్న్ విశ్లేషణ", "card_churn_sub": "కస్టమర్ ఉంటారా వెళ్తారా అంచనా వేయండి",
        "card_chat_title": "వాయిస్ AI చాట్", "card_chat_sub": "మీ భాషలో బ్యాంకింగ్ గురించి అడగండి",
        "loan_check": "లోన్ అర్హత తనిఖీ", "loan_form_title": "లోన్ వివరాలు నమోదు చేయండి",
        "label_income": "వార్షిక ఆదాయం (₹)", "label_loan_amt": "లోన్ మొత్తం (₹)",
        "label_cibil": "CIBIL స్కోర్", "label_term": "లోన్ కాలం (నెలలు)",
        "label_edu": "విద్య", "label_self": "స్వయం ఉపాధి",
        "label_dep": "ఆధారపడిన వారు", "label_res": "నివాస ఆస్తులు (₹)",
        "btn_check_loan": "🔍 అర్హత తనిఖీ చేయండి",
        "opt_graduate": "గ్రాడ్యుయేట్", "opt_notgraduate": "నాన్-గ్రాడ్యుయేట్",
        "opt_yes": "అవును", "opt_no": "కాదు",
        "churn_check": "కస్టమర్ చర్న్ విశ్లేషణ", "churn_form_title": "కస్టమర్ వివరాలు",
        "label_credit": "క్రెడిట్ స్కోర్", "label_age": "వయస్సు",
        "label_tenure": "కాలం (సంవత్సరాలు)", "label_balance": "బ్యాలెన్స్ (₹)",
        "label_products": "ఉత్పత్తుల సంఖ్య", "label_sat": "సంతృప్తి (1-5)",
        "label_complaints": "ఫిర్యాదులు", "label_active": "యాక్టివ్ మెంబర్?",
        "btn_check_churn": "🔍 చర్న్ రిస్క్ విశ్లేషించండి",
        "chat": "AI బ్యాంకింగ్ అసిస్టెంట్", "chat_placeholder": "మీ ప్రశ్న టైప్ చేయండి...",
        "chat_welcome": "👋 నమస్కారం! నేను BankIQ, మీ AI బ్యాంకింగ్ అసిస్టెంట్. లోన్, CIBIL, EMI గురించి అడగండి — మీ భాషలో!",
        "fq1": "CIBIL స్కోర్ అంటే ఏమిటి?", "fq2": "లోన్ అవకాశాలు పెంచడం ఎలా?",
        "fq3": "EMI అంటే ఏమిటి?", "fq4": "CIBIL వేగంగా పెంచండి",
        "approved": "✅ అనుమతించబడింది", "rejected": "❌ తిరస్కరించబడింది",
        "why_approved": "✅ ఎందుకు అనుమతించబడింది", "why_rejected": "❌ ఎందుకు తిరస్కరించబడింది",
        "next_steps": "📋 తదుపరి దశలు", "factor_impact": "📈 కారకాల ప్రభావం",
        "risk_signals": "⚠️ రిస్క్ సంకేతాలు", "loyalty_signals": "✅ విధేయత సంకేతాలు",
        "bank_actions": "🎯 సిఫార్సు చేయబడిన చర్యలు",
        "reapply_in": "మళ్ళీ దరఖాస్తు చేయవచ్చు", "improvement_tip": "ముఖ్యమైన మెరుగుదల చిట్కా",
        "speak": "🎤 చెప్పండి", "stop": "⏹ ఆపు", "listen": "🔊 వినండి",
        "churn_risk": "కస్టమర్ వెళ్ళిపోయే ప్రమాదం",
        "will_stay": "✅ కస్టమర్ ఉంటారు", "will_leave": "⚠️ అధిక చర్న్ రిస్క్",
        "confidence": "నమ్మకం",
        "profile_student": "విద్యార్థి", "profile_professional": "ప్రొఫెషనల్",
        "profile_elder": "వృద్ధులు", "profile_business": "వ్యాపారం",
        "profile_farmer": "రైతు", "profile_other": "ఇతర",
        "enter_btn": "BankIQ లో ప్రవేశించండి 🚀", "change_lang": "భాష మార్చండి", "btn_cancel": "రద్దు చేయి",
    },
    "Kannada": {
        "welcome": "BankIQ ಗೆ ಸ್ವಾಗತ",
        "select_language": "ನಿಮ್ಮ ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ", "select_profile": "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಆಯ್ಕೆ ಮಾಡಿ",
        "language_prompt": "ಮುಂದುವರಿಯಲು ನಿಮ್ಮ ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ",
        "login": "ಲಾಗಿನ್", "logout": "ಲಾಗ್ಔಟ್", "username": "ಬಳಕೆದಾರ ಹೆಸರು",
        "nav_home": "🏠 ಮುಖಪುಟ", "nav_loan": "🏦 ಸಾಲ ತಪಾಸಣೆ",
        "nav_churn": "📊 ಚರ್ನ್", "nav_chat": "🤖 AI ಚಾಟ್",
        "hero_title": "AI ಬ್ಯಾಂಕಿಂಗ್\nಸರಳಗೊಳಿಸಲಾಗಿದೆ",
        "hero_sub": "ಸ್ಪಷ್ಟ ನಿರ್ಧಾರಗಳು. ಧ್ವನಿ ಬೆಂಬಲ. ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ. ಎಲ್ಲರಿಗೂ.",
        "card_loan_title": "ಸಾಲ ಅರ್ಹತೆ", "card_loan_sub": "AI ವಿವರಣೆಯೊಂದಿಗೆ ಅನುಮೋದನೆ ತಪಾಸಣೆ ಮಾಡಿ",
        "card_churn_title": "ಚರ್ನ್ ವಿಶ್ಲೇಷಣೆ", "card_churn_sub": "ಗ್ರಾಹಕ ಉಳಿಯುತ್ತಾರೆಯೇ ಹೋಗುತ್ತಾರೆಯೇ ಊಹಿಸಿ",
        "card_chat_title": "ಧ್ವನಿ AI ಚಾಟ್", "card_chat_sub": "ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಬ್ಯಾಂಕಿಂಗ್ ಬಗ್ಗೆ ಕೇಳಿ",
        "loan_check": "ಸಾಲ ಅರ್ಹತೆ ತಪಾಸಣೆ", "loan_form_title": "ಸಾಲ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ",
        "label_income": "ವಾರ್ಷಿಕ ಆದಾಯ (₹)", "label_loan_amt": "ಸಾಲದ ಮೊತ್ತ (₹)",
        "label_cibil": "CIBIL ಸ್ಕೋರ್", "label_term": "ಸಾಲದ ಅವಧಿ (ತಿಂಗಳು)",
        "label_edu": "ಶಿಕ್ಷಣ", "label_self": "ಸ್ವಯಂ ಉದ್ಯೋಗ",
        "label_dep": "ಅವಲಂಬಿತರು", "label_res": "ವಸತಿ ಆಸ್ತಿಗಳು (₹)",
        "btn_check_loan": "🔍 ಅರ್ಹತೆ ತಪಾಸಣೆ ಮಾಡಿ",
        "opt_graduate": "ಪದವೀಧರ", "opt_notgraduate": "ಪದವೀಧರರಲ್ಲ",
        "opt_yes": "ಹೌದು", "opt_no": "ಇಲ್ಲ",
        "churn_check": "ಗ್ರಾಹಕ ಚರ್ನ್ ವಿಶ್ಲೇಷಣೆ", "churn_form_title": "ಗ್ರಾಹಕ ವಿವರಗಳು",
        "label_credit": "ಕ್ರೆಡಿಟ್ ಸ್ಕೋರ್", "label_age": "ವಯಸ್ಸು",
        "label_tenure": "ಅವಧಿ (ವರ್ಷಗಳು)", "label_balance": "ಶಿಲ್ಕು (₹)",
        "label_products": "ಉತ್ಪನ್ನ ಸಂಖ್ಯೆ", "label_sat": "ತೃಪ್ತಿ (1-5)",
        "label_complaints": "ದೂರುಗಳು", "label_active": "ಸಕ್ರಿಯ ಸದಸ್ಯರೇ?",
        "btn_check_churn": "🔍 ಚರ್ನ್ ಅಪಾಯ ವಿಶ್ಲೇಷಿಸಿ",
        "chat": "AI ಬ್ಯಾಂಕಿಂಗ್ ಸಹಾಯಕ", "chat_placeholder": "ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಟೈಪ್ ಮಾಡಿ...",
        "chat_welcome": "👋 ನಮಸ್ಕಾರ! ನಾನು BankIQ, ನಿಮ್ಮ AI ಬ್ಯಾಂಕಿಂಗ್ ಸಹಾಯಕ. ಸಾಲ, CIBIL, EMI ಬಗ್ಗೆ ಕೇಳಿ — ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ!",
        "fq1": "CIBIL ಸ್ಕೋರ್ ಎಂದರೇನು?", "fq2": "ಸಾಲ ಅವಕಾಶ ಹೇಗೆ ಸುಧಾರಿಸುವುದು?",
        "fq3": "EMI ಎಂದರೇನು?", "fq4": "CIBIL ವೇಗವಾಗಿ ಹೆಚ್ಚಿಸಿ",
        "approved": "✅ ಅನುಮೋದಿಸಲಾಗಿದೆ", "rejected": "❌ ತಿರಸ್ಕರಿಸಲಾಗಿದೆ",
        "why_approved": "✅ ಏಕೆ ಅನುಮೋದಿಸಲಾಯಿತು", "why_rejected": "❌ ಏಕೆ ತಿರಸ್ಕರಿಸಲಾಯಿತು",
        "next_steps": "📋 ಮುಂದಿನ ಹಂತಗಳು", "factor_impact": "📈 ಅಂಶ ಪ್ರಭಾವ",
        "risk_signals": "⚠️ ಅಪಾಯ ಸಂಕೇತಗಳು", "loyalty_signals": "✅ ನಿಷ್ಠೆ ಸಂಕೇತಗಳು",
        "bank_actions": "🎯 ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮಗಳು",
        "reapply_in": "ಮರು ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು", "improvement_tip": "ಪ್ರಮುಖ ಸುಧಾರಣಾ ಸಲಹೆ",
        "speak": "🎤 ಹೇಳಿ", "stop": "⏹ ನಿಲ್ಲಿಸಿ", "listen": "🔊 ಕೇಳಿ",
        "churn_risk": "ಗ್ರಾಹಕ ತೊರೆಯುವ ಅಪಾಯ",
        "will_stay": "✅ ಗ್ರಾಹಕ ಉಳಿಯುತ್ತಾರೆ", "will_leave": "⚠️ ಹೆಚ್ಚಿನ ಚರ್ನ್ ಅಪಾಯ",
        "confidence": "ವಿಶ್ವಾಸ",
        "profile_student": "ವಿದ್ಯಾರ್ಥಿ", "profile_professional": "ವೃತ್ತಿಪರ",
        "profile_elder": "ಹಿರಿಯರು", "profile_business": "ವ್ಯಾಪಾರ",
        "profile_farmer": "ರೈತ", "profile_other": "ಇತರ",
        "enter_btn": "BankIQ ಗೆ ಪ್ರವೇಶಿಸಿ 🚀", "change_lang": "ಭಾಷೆ ಬದಲಿಸಿ", "btn_cancel": "ರದ್ದು ಮಾಡಿ",
    },
    "Malayalam": {
        "welcome": "BankIQ-ലേക്ക് സ്വാഗതം",
        "select_language": "നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക", "select_profile": "നിങ്ങളുടെ പ്രൊഫൈൽ തിരഞ്ഞെടുക്കുക",
        "language_prompt": "തുടരാൻ നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക",
        "login": "ലോഗിൻ", "logout": "ലോഗൗട്ട്", "username": "ഉപയോക്തൃ നാമം",
        "nav_home": "🏠 ഹോം", "nav_loan": "🏦 ലോൺ",
        "nav_churn": "📊 ചേർൺ", "nav_chat": "🤖 AI ചാറ്റ്",
        "hero_title": "AI ബ്യാങ്കിംഗ്\nലളിതമാക്കി",
        "hero_sub": "വ്യക്തമായ തീരുമാനങ്ങൾ. ശബ്ദ സഹായം. നിങ്ങളുടെ ഭാഷയിൽ. എല്ലാവർക്കും.",
        "card_loan_title": "ലോൺ യോഗ്യത", "card_loan_sub": "AI വിശദീകരണത്തോടെ അംഗീകാര സാധ്യതകൾ പരിശോധിക്കുക",
        "card_churn_title": "ചേർൺ വിശകലനം", "card_churn_sub": "ഉപഭോക്താവ് തുടരുമോ പോകുമോ പ്രവചിക്കുക",
        "card_chat_title": "ശബ്ദ AI ചാറ്റ്", "card_chat_sub": "നിങ്ങളുടെ ഭാഷയിൽ ബ്യാങ്കിംഗ് കാര്യങ്ങൾ ചോദിക്കുക",
        "loan_check": "ലോൺ യോഗ്യതാ പരിശോധന", "loan_form_title": "ലോൺ വിവരങ്ങൾ നൽകുക",
        "label_income": "വാർഷിക വരുമാനം (₹)", "label_loan_amt": "ലോൺ തുക (₹)",
        "label_cibil": "CIBIL സ്കോർ", "label_term": "ലോൺ കാലാവധി (മാസം)",
        "label_edu": "വിദ്യാഭ്യാസം", "label_self": "സ്വയം തൊഴിൽ",
        "label_dep": "ആശ്രിതർ", "label_res": "ആവാസ സ്വത്തുക്കൾ (₹)",
        "btn_check_loan": "🔍 യോഗ്യത പരിശോധിക്കുക",
        "opt_graduate": "ബിരുദധാരി", "opt_notgraduate": "ബിരുദധാരി അല്ല",
        "opt_yes": "അതെ", "opt_no": "ഇല്ല",
        "churn_check": "ഉപഭോക്തൃ ചേർൺ വിശകലനം", "churn_form_title": "ഉപഭോക്തൃ വിവരങ്ങൾ",
        "label_credit": "ക്രെഡിറ്റ് സ്കോർ", "label_age": "പ്രായം",
        "label_tenure": "കാലാവധി (വർഷം)", "label_balance": "ബ്യാലൻസ് (₹)",
        "label_products": "ഉൽപ്പന്ന എണ്ണം", "label_sat": "സംതൃപ്തി (1-5)",
        "label_complaints": "പരാതികൾ", "label_active": "സജീവ അംഗമോ?",
        "btn_check_churn": "🔍 ചേർൺ റിസ്ക് വിശകലനം",
        "chat": "AI ബ്യാങ്കിംഗ് അസിസ്റ്റന്റ്", "chat_placeholder": "നിങ്ങളുടെ ചോദ്യം ടൈപ്പ് ചെയ്യുക...",
        "chat_welcome": "👋 നമസ്കാരം! ഞാൻ BankIQ, നിങ്ങളുടെ AI ബ്യാങ്കിംഗ് അസിസ്റ്റന്റ്. ലോൺ, CIBIL, EMI ചോദിക്കുക — നിങ്ങളുടെ ഭാഷയിൽ!",
        "fq1": "CIBIL സ്കോർ എന്താണ്?", "fq2": "ലോൺ അവസരങ്ങൾ മെച്ചപ്പെടുത്തുക",
        "fq3": "EMI എന്താണ്?", "fq4": "CIBIL വേഗം വർദ്ധിപ്പിക്കുക",
        "approved": "✅ അംഗീകരിച്ചു", "rejected": "❌ നിരസിച്ചു",
        "why_approved": "✅ എന്തുകൊണ്ട് അംഗീകരിച്ചു", "why_rejected": "❌ എന്തുകൊണ്ട് നിരസിച്ചു",
        "next_steps": "📋 അടുത്ത ഘട്ടങ്ങൾ", "factor_impact": "📈 ഘടക സ്വാധീനം",
        "risk_signals": "⚠️ റിസ്ക് സൂചനകൾ", "loyalty_signals": "✅ വിശ്വസ്തത സൂചനകൾ",
        "bank_actions": "🎯 ശുപാർശ ചെയ്ത നടപടികൾ",
        "reapply_in": "വീണ്ടും അപേക്ഷിക്കാം", "improvement_tip": "പ്രധാന മെച്ചപ്പെടുത്തൽ നുറുങ്ങ്",
        "speak": "🎤 സംസാരിക്കുക", "stop": "⏹ നിർത്തുക", "listen": "🔊 കേൾക്കുക",
        "churn_risk": "ഉപഭോക്തൃ നഷ്ട സാധ്യത",
        "will_stay": "✅ ഉപഭോക്താവ് തുടരും", "will_leave": "⚠️ ഉയർന്ന ചേർൺ റിസ്ക്",
        "confidence": "വിശ്വാസ്യത",
        "profile_student": "വിദ്യാർത്ഥി", "profile_professional": "പ്രൊഫഷണൽ",
        "profile_elder": "മുതിർന്നവർ", "profile_business": "ബിസിനസ്",
        "profile_farmer": "കർഷകൻ", "profile_other": "മറ്റുള്ളവ",
        "enter_btn": "BankIQ-ൽ പ്രവേശിക്കുക 🚀", "change_lang": "ഭാഷ മാറ്റുക", "btn_cancel": "റദ്ദാക്കുക",
    }
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
# UI TRANSLATIONS — Full website localization
# ══════════════════════════════════════════════════
def get_ui_labels(language: str) -> dict:
    """Return all UI labels for the selected language."""
    return UI_TRANSLATIONS.get(language, UI_TRANSLATIONS["English"])


# ══════════════════════════════════════════════════
# 1. MAIN CHAT — Personalized Banking Chatbot
# ══════════════════════════════════════════════════
async def ask_claude(question, profile, language, topic, history=[]):
    lang_instr = LANGS.get(language, LANGS["English"])
    prof_instr = PROFILES.get(profile, PROFILES["Student"])

    system = f"""{prof_instr}
{lang_instr}
Topic area: {topic}

You are BankIQ — a friendly, expert AI banking assistant that explains banking decisions simply.
You specialize in: loans, EMI, CIBIL scores, bank accounts, fixed deposits, insurance, and churn analysis.
Always be warm, encouraging, and supportive. Never use harsh or discouraging language.

Reply ONLY as valid JSON with no extra text outside JSON:
{{
  "answer": "2-3 sentence direct answer to the question in the user's language",
  "confidence": "high/medium/low",
  "explanation_points": ["point1", "point2", "point3"],
  "analogy": "simple everyday analogy matching the profile and language",
  "follow_up_questions": ["question1?", "question2?"],
  "voice_answer": "A short 1-sentence version for voice/audio playback (in the user's language)"
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
            max_tokens=900
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
        "follow_up_questions": ["What is EMI?", "How to improve CIBIL score?"],
        "voice_answer": "Sorry, I could not understand. Please try again."
    }


# ══════════════════════════════════════════════════
# 2. VOICE CHATBOT — Twilio-friendly plain text
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


# ══════════════════════════════════════════════════
# 3. LOAN / CHURN EXPLANATION (SHAP → Plain)
#    Returns: reasons + next_steps + reapply_timeline
# ══════════════════════════════════════════════════
async def shap_to_plain(shap_dict, prediction, profile, language, model_type,
                         loan_inputs=None):
    lang_instr = LANGS.get(language, LANGS["English"])
    prof_instr = PROFILES.get(profile, PROFILES["Student"])
    # Profile-specific explanation rules
    profile_rules = ""

    if profile == "Professional":
        profile_rules = """
Explain technically like a financial risk analyst.
Use the SHAP factors and numeric inputs to justify the decision.
Mention feature importance and risk contribution.
Use structured bullet explanations suitable for dashboards.
"""

    elif profile == "Student":
        profile_rules = """
Explain in simple educational language.
Use easy examples and avoid technical financial terms.
"""

    elif profile == "Elder":
        profile_rules = """
Explain very simply using real-life analogies like borrowing money from a neighbor.
Avoid technical words and keep sentences short.
"""

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
Top positive factors that increased approval probability:
{pos_summary}

Top negative factors that reduced approval probability:
{neg_summary}

You MUST explain these factors directly in explanation_points.
Profile: {profile}
{prof_instr}
{lang_instr}
{profile_rules}

{"Since REJECTED — give specific reasons and clear action steps to improve and reapply." if not prediction else "Since APPROVED — explain why and what to do next to maintain this."}

Reply ONLY as valid JSON (no extra text):
{{
  "explanation_points": [
    "Explain the most important factor from SHAP values using the actual numbers provided",
    "Explain the second strongest factor clearly using the input values",
    "Explain the third factor and how it affected the decision"
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
  "reapply_timeline": "{'Specific timeline like: After 6 months when CIBIL improves' if not prediction else 'You are approved — proceed with documentation now'}",
  "improvement_tip": "Single most important thing to {'improve chances next time' if not prediction else 'maintain good standing'}",
  "analogy": "Simple daily life analogy matching {profile} profile",
  "transparency_score": 85,
  "voice_summary": "1 short sentence summarizing the result for voice playback"
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
{profile_rules}

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
    "Bank action 1 to {'retain customer urgently' if prediction else 'keep customer happy'}",
    "Bank action 2",
    "Bank action 3"
  ],
  "reapply_timeline": "{'Timeframe for bank to act — e.g., Act within 2 weeks' if prediction else 'Next review in 3 months'}",
  "improvement_tip": "Single most impactful action {'to retain this customer' if prediction else 'to keep customer happy'}",
  "analogy": "Simple daily life analogy matching {profile} profile",
  "transparency_score": 82,
  "voice_summary": "1 short sentence summarizing churn risk for voice playback"
}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are BankIQ explanation engine. {lang_instr} Reply only in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=700
        )
        text = response.choices[0].message.content
        result = safe_json(text)
        if result:
            return result
    except Exception as e:
        print(f"shap_to_plain error: {e}")

    # ── FALLBACK — fully translated using FALLBACK_MSGS ──
    fb = FALLBACK_MSGS.get(language, FALLBACK_MSGS["English"])

    if model_type == "loan":
        if prediction:
            return {
                "explanation_points": fb["loan_approved_exp"],
                "rejection_reasons": fb["loan_approved_exp"],
                "next_steps": fb["loan_approved_steps"],
                "reapply_timeline": fb["loan_approved_timeline"],
                "improvement_tip": fb["loan_approved_tip"],
                "analogy": fb["analogy_pass"],
                "transparency_score": 82,
                "voice_summary": fb["loan_approved_voice"]
            }
        else:
            return {
                "explanation_points": fb["loan_rejected_exp"],
                "rejection_reasons": fb["loan_rejected_exp"],
                "next_steps": fb["loan_rejected_steps"],
                "reapply_timeline": fb["loan_rejected_timeline"],
                "improvement_tip": fb["loan_rejected_tip"],
                "analogy": fb["analogy_fail"],
                "transparency_score": 80,
                "voice_summary": fb["loan_rejected_voice"]
            }
    else:
        if prediction:
            return {
                "explanation_points": fb["churn_yes_exp"],
                "rejection_reasons": fb["churn_yes_exp"],
                "next_steps": fb["churn_yes_steps"],
                "reapply_timeline": fb["churn_yes_timeline"],
                "improvement_tip": fb["churn_yes_tip"],
                "analogy": fb["analogy_churn"],
                "transparency_score": 78,
                "voice_summary": fb["churn_yes_voice"]
            }
        else:
            return {
                "explanation_points": fb["churn_no_exp"],
                "rejection_reasons": fb["churn_no_exp"],
                "next_steps": fb["churn_no_steps"],
                "reapply_timeline": fb["churn_no_timeline"],
                "improvement_tip": fb["churn_no_tip"],
                "analogy": fb["analogy_loyal"],
                "transparency_score": 85,
                "voice_summary": fb["churn_no_voice"]
            }

# ══════════════════════════════════════════════════
# 4. SIMPLIFY — Make Explanation Even Simpler
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
  "next_steps": ["One simple action they can take right now"],
  "voice_answer": "One very short sentence for voice playback"
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
        "next_steps": ["Ask the AI a specific question for more details"],
        "voice_answer": "The AI reviewed your finances and gave a result."
    }


# ══════════════════════════════════════════════════
# 5. WHAT-IF EXPLANATION
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
  "next_best_action": "What to change next to improve further",
  "voice_summary": "1 short sentence summarizing what-if result for voice"
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
        "next_best_action": "Try improving your CIBIL score above 750 for best results",
        "voice_summary": "The changes you made affected the loan decision."
    }


# ══════════════════════════════════════════════════
# 6. TWILIO VOICE HANDLER — IVR Menu Response
#    Returns TwiML-ready text for phone callers
# ══════════════════════════════════════════════════
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