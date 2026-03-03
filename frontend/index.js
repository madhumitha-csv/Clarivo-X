const API = 'http://localhost:8000';
const S = {page:'splash', hist:[], profile:'Student', language:'English', userName:'User', guest:false, loanResult:null, voiceMode:false};
const STEP_PAGES = ['usecase','inputform','airesult','explanation'];

// ═══════════════════════════════════════════════
// TRANSLATIONS — Full UI labels in 4 languages
// ═══════════════════════════════════════════════
const T = {
  English: {
    nav_home:"Home", nav_chat:"AI Chat", nav_churn:"Churn",
    pp_profile:"Switch Profile", pp_feedback:"Feedback", pp_signout:"Sign Out",
    chat_welcome_short:"Hi! Ask me anything about banking, loans, or your account.",
    login_tagline:"Explainable AI for Loans, Churn & Banking",
    username:"Your Name", enter_btn:"Get Started →", guest_btn:"Continue as Guest",
    step1_badge:"Step 1 of 3", profile_title:"Who are you?",
    profile_sub:"We'll personalise AI explanations to match your level",
    profile_elder:"Elder Mode", profile_elder_desc:"Simple language with real-world analogies. No jargon, just clarity.",
    profile_student:"Student Mode", profile_student_desc:"School analogies and beginner-friendly context.",
    profile_professional:"Professional Mode", profile_professional_desc:"Financial terms, SHAP values, and data-driven insights.",
    select_btn:"Select →",
    hero_title:"Banking AI\nYou Can Trust",
    hero_sub:"ClarivoX explains every AI banking decision in your language — loans, customer churn, credit scores — powered by SHAP and Groq AI.",
    hero_btn1:"🚀 Check Loan AI", hero_btn2:"💬 Ask AI", hero_btn3:"📉 Churn Predictor",
    feat_loan_title:"Loan Approval AI", feat_loan_desc:"Understand why your loan was approved or rejected with full SHAP factor breakdown.",
    feat_churn_title:"Churn Predictor", feat_churn_desc:"Predict if a customer will leave the bank and understand the risk factors clearly.",
    feat_chat_title:"AI Banking Chat", feat_chat_desc:"Ask anything about loans, EMI, credit scores, investments in your language.",
    feat_whatif_title:"What-If Simulator", feat_whatif_desc:"Change your profile values and see how loan approval probability changes live.",
    feat_trans_title:"Transparency Report", feat_trans_desc:"See how open, reliable and fair the AI banking decision was with bias metrics.",
    feat_fb_title:"Rate ClarivoX", feat_fb_desc:"Help us improve by sharing your experience with the AI explanations.",
    analyse_btn:"Analyse →", predict_btn:"Predict →", ask_btn:"Ask now →", simulate_btn:"Simulate →", report_btn:"View report →", feedback_btn:"Give feedback →",
    step2_badge:"Step 2 of 3", usecase_title:"What do you want to check?", usecase_sub:"Select a use case and get a personalised AI explanation",
    uc_loan:"Loan & EMI", uc_loan_desc:"Ask about loans, interest rates, EMI calculations.",
    uc_credit:"Credit Score", uc_credit_desc:"Understand how to improve your CIBIL score.",
    uc_savings:"Savings & Investment", uc_savings_desc:"Learn about FD, RD, mutual funds and savings.",
    uc_insurance:"Insurance", uc_insurance_desc:"Understand life, health, and vehicle insurance.",
    step3_badge:"Step 3 of 3", loan_form_title:"Enter Loan Details", loan_form_sub:"Fill in your details for an accurate AI loan assessment",
    label_income:"Annual Income (₹)", label_loan_amt:"Loan Amount (₹)", label_cibil:"CIBIL Score",
    label_term:"Loan Term (months)", label_edu:"Education", label_self:"Self Employed?",
    label_dep:"Dependents", label_res:"Residential Assets (₹)",
    opt_graduate:"Graduate", opt_notgraduate:"Not Graduate", opt_yes:"Yes", opt_no:"No",
    btn_check_loan:"🚀 Run AI Assessment", privacy_note:"🔒 Your data is processed locally and never stored",
    confidence:"Model Confidence", risk_level:"Risk Level", listen_result:"Listen to Result",
    view_explanation:"🔍 View Full Explanation →", whatif_btn:"🔧 What-If Simulator", trans_btn:"🛡️ Transparency Report",
    expl_title:"Why was this decision made?", expl_sub:"Top SHAP factors that influenced the AI's outcome, personalised for your profile",
    simplify_btn:"🧓 Simplify", ask_ai_btn:"💬 Ask AI",
    whatif_btn2:"🔧 What-If Simulator →", trans_btn2:"🛡️ Transparency Report →",
    shap_weights:"SHAP FACTOR WEIGHTS", analogy_label:"💡 ANALOGY",
    whatif_title:"What-If Simulator", whatif_sub:"Adjust sliders to see how changes affect loan approval probability in real time",
    sim_income:"💰 Annual Income (₹)", sim_cibil:"📊 CIBIL Score", sim_loan:"🏠 Loan Amount (₹)",
    approval_prob:"APPROVAL PROBABILITY", run_assessment:"🚀 Run Real Assessment →",
    churn_check:"Customer Churn Predictor", churn_sub:"Predict if a customer will leave the bank — powered by Random Forest + SHAP",
    label_tenure:"Tenure (years)", label_balance:"Account Balance (₹)", label_products:"No. of Products",
    label_sat:"Satisfaction Score (1-5)", label_complaints:"Number of Complaints", label_credit:"Credit Score",
    label_age:"Age", label_active:"Is Active Member?", btn_check_churn:"📉 Predict Churn Risk",
    churn_risk:"Risk Score",
    chat_title:"Ask ClarivoX AI", chat_sub:"Get plain-language answers about banking in your language",
    chat_placeholder:"Ask a banking question…", chat_welcome:"Hello! I'm here to explain banking decisions in simple terms. Ask me anything!",
    send_btn:"Send",
    fq1:"What is EMI?", fq2:"Improve CIBIL score", fq3:"Should I take a loan?",
    topic_loan:"🏦 Loans & EMI", topic_credit:"📊 Credit Score", topic_savings:"💰 Savings", topic_insurance:"🛡️ Insurance",
    trans_title:"Transparency & Bias Report", trans_sub:"How open, reliable, and fair was this AI decision?",
    trans_score_label:"TRANSPARENCY SCORE", trans_good:"✓ Good Transparency",
    score_breakdown:"SCORE BREAKDOWN", model_conf:"Model Confidence", shap_stability:"SHAP Stability",
    bias_check:"Bias Check", explainability:"Explainability",
    bias_detection:"⚖️ Bias Detection", potential_bias:"⚠️ Potential Bias",
    bias_desc:"A disparity was found in urban vs rural approval rates in the training data.",
    urban_approval:"Urban Approval", rural_approval:"Rural Approval", model_info:"MODEL INFO",
    rate_badge:"⭐ Rate ClarivoX", fb_title:"How helpful was the AI?",
    fb_sub:"Your feedback helps us improve for everyone",
    fb_placeholder:"Tell us what you liked or what we can improve…",
    submit_fb:"Submit Feedback →", fb_thanks:"Thank you!", fb_submitted:"Your feedback has been submitted to our team.",
    back_home:"← Back to Home",
    approved:"✅ Approved", rejected:"❌ Rejected",
    why_approved:"Great news! Your application meets the approval criteria.",
    why_rejected:"Your application did not meet the minimum criteria.",
    emode_label:"Personalised Explanation", emode_elder:"Elder Mode", emode_student:"Student Mode", emode_professional:"Professional Mode",
    rejection_reasons_title:"❌ Why Was It Rejected?",
    next_steps_title:"✅ What To Do Next",
    reapply_label:"📅 When To Reapply",
    improvement_tip_label:"💡 Top Improvement Tip",
    no_rejection_data:"No specific rejection reasons available.",
    likely_approved:"Likely Approved", borderline:"Borderline", likely_rejected:"Likely Rejected",
    tip_cibil:"Raise CIBIL score above 750 for the biggest boost.",
    tip_income:"Income above ₹6L significantly improves chances.",
    tip_loan:"Lower the loan amount to improve approval odds.",
    tip_good:"Good profile! You'd likely be approved with these values.",
    ai_decision:"AI Decision Complete", model_sub:"Loan Approval Assessment · LightGBM + SHAP", shap_score_label:"SHAP Score", risk_low:"Low Risk", risk_medium:"Medium", risk_high:"High"
  },
  Tamil: {
    nav_home:"முகப்பு", nav_chat:"AI உரை", nav_churn:"வாடிக்கையாளர்",
    pp_profile:"சுயவிவரம் மாற்று", pp_feedback:"கருத்து", pp_signout:"வெளியேறு",
    chat_welcome_short:"வணக்கம்! வங்கி, கடன் பற்றி கேளுங்கள்.",
    login_tagline:"கடன், வாடிக்கையாளர் & வங்கிக்கான விளக்க AI",
    username:"உங்கள் பெயர்", enter_btn:"தொடங்கவும் →", guest_btn:"விருந்தினராக தொடரவும்",
    step1_badge:"படி 1 / 3", profile_title:"நீங்கள் யார்?",
    profile_sub:"உங்கள் நிலைக்கு ஏற்ப AI விளக்கங்களை தனிப்பயனாக்குவோம்",
    profile_elder:"முதியோர் பயன்முறை", profile_elder_desc:"எளிய மொழி, வாழ்க்கை உதாரணங்கள். சொல்லாட்சி இல்லை.",
    profile_student:"மாணவர் பயன்முறை", profile_student_desc:"பள்ளி உதாரணங்கள் மற்றும் தொடக்கநிலை விளக்கங்கள்.",
    profile_professional:"தொழில்முறை பயன்முறை", profile_professional_desc:"நிதி சொற்கள், SHAP மதிப்புகள் மற்றும் தரவு பகுப்பாய்வு.",
    select_btn:"தேர்ந்தெடு →",
    hero_title:"நம்பகமான\nவங்கி AI",
    hero_sub:"ClarivoX ஒவ்வொரு AI வங்கி முடிவையும் உங்கள் மொழியில் விளக்குகிறது — கடன், வாடிக்கையாளர் இழப்பு, கிரெடிட் ஸ்கோர் — SHAP மற்றும் Groq AI மூலம்.",
    hero_btn1:"🚀 கடன் AI சரிபார்", hero_btn2:"💬 AI கேளு", hero_btn3:"📉 வாடிக்கையாளர் பகுப்பு",
    feat_loan_title:"கடன் அனுமதி AI", feat_loan_desc:"உங்கள் கடன் ஏன் அனுமதிக்கப்பட்டது அல்லது நிராகரிக்கப்பட்டது என்று புரிந்துகொள்ளுங்கள்.",
    feat_churn_title:"வாடிக்கையாளர் இழப்பு", feat_churn_desc:"வாடிக்கையாளர் வங்கியை விடுவாரா என்று கணிக்கவும்.",
    feat_chat_title:"AI வங்கி உரை", feat_chat_desc:"கடன், EMI, கிரெடிட் ஸ்கோர் பற்றி உங்கள் மொழியில் கேளுங்கள்.",
    feat_whatif_title:"என்னவாகும் சிமுலேட்டர்", feat_whatif_desc:"மதிப்புகளை மாற்றி கடன் அனுமதி வாய்ப்பை நேரடியாக பாருங்கள்.",
    feat_trans_title:"வெளிப்படைத்தன்மை அறிக்கை", feat_trans_desc:"AI முடிவு எவ்வளவு நேர்மையானது என்று பாருங்கள்.",
    feat_fb_title:"ClarivoX மதிப்பிடு", feat_fb_desc:"உங்கள் அனுபவத்தை பகிர்ந்து மேம்பட உதவுங்கள்.",
    analyse_btn:"பகுப்பாய்வு →", predict_btn:"கணிக்கவும் →", ask_btn:"இப்போது கேளு →", simulate_btn:"சிமுலேட் →", report_btn:"அறிக்கை பார்க்க →", feedback_btn:"கருத்து தர →",
    step2_badge:"படி 2 / 3", usecase_title:"என்ன சரிபார்க்கணும்?", usecase_sub:"ஒரு பயன்பாட்டை தேர்ந்தெடுத்து தனிப்பயன் AI விளக்கம் பெறுங்கள்",
    uc_loan:"கடன் & EMI", uc_loan_desc:"கடன், வட்டி வீதம், EMI கணக்கீடு பற்றி கேளுங்கள்.",
    uc_credit:"கிரெடிட் ஸ்கோர்", uc_credit_desc:"CIBIL ஸ்கோரை எப்படி மேம்படுத்துவது என்று புரிந்துகொள்ளுங்கள்.",
    uc_savings:"சேமிப்பு & முதலீடு", uc_savings_desc:"FD, RD, மியூச்சுவல் ஃபண்ட் பற்றி அறிந்துகொள்ளுங்கள்.",
    uc_insurance:"காப்பீடு", uc_insurance_desc:"உயிர், சுகாதார, வாகன காப்பீடு பற்றி புரிந்துகொள்ளுங்கள்.",
    step3_badge:"படி 3 / 3", loan_form_title:"கடன் விவரங்களை உள்ளிடவும்", loan_form_sub:"சரியான AI கடன் மதிப்பீட்டிற்கு விவரங்களை நிரப்பவும்",
    label_income:"வருடாந்திர வருமானம் (₹)", label_loan_amt:"கடன் தொகை (₹)", label_cibil:"CIBIL மதிப்பெண்",
    label_term:"கடன் காலம் (மாதங்கள்)", label_edu:"கல்வி", label_self:"சுயதொழில்?",
    label_dep:"சார்ந்திருப்பவர்கள்", label_res:"குடியிருப்பு சொத்துக்கள் (₹)",
    opt_graduate:"பட்டதாரி", opt_notgraduate:"பட்டதாரி இல்லை", opt_yes:"ஆம்", opt_no:"இல்லை",
    btn_check_loan:"🚀 AI மதிப்பீடு இயக்கு", privacy_note:"🔒 உங்கள் தரவு உள்ளூரில் செயலாக்கப்படுகிறது",
    confidence:"மாடல் நம்பகம்", risk_level:"ஆபத்து நிலை", listen_result:"🔊 முடிவை கேளு",
    view_explanation:"🔍 முழு விளக்கம் பார்க்க →", whatif_btn:"🔧 என்னவாகும் சிமுலேட்டர்", trans_btn:"🛡️ வெளிப்படைத்தன்மை அறிக்கை",
    expl_title:"இந்த முடிவு ஏன் எடுக்கப்பட்டது?", expl_sub:"AI முடிவை பாதித்த முக்கிய SHAP காரணிகள்",
    simplify_btn:"🧓 எளிமைப்படுத்து", ask_ai_btn:"💬 AI கேளு",
    whatif_btn2:"🔧 என்னவாகும் சிமுலேட்டர் →", trans_btn2:"🛡️ வெளிப்படைத்தன்மை அறிக்கை →",
    shap_weights:"SHAP காரணி எடைகள்", analogy_label:"💡 உதாரணம்",
    whatif_title:"என்னவாகும் சிமுலேட்டர்", whatif_sub:"ஸ்லைடர்களை சரிசெய்து கடன் அனுமதி வாய்ப்பை நேரடியாக பாருங்கள்",
    sim_income:"💰 வருடாந்திர வருமானம் (₹)", sim_cibil:"📊 CIBIL மதிப்பெண்", sim_loan:"🏠 கடன் தொகை (₹)",
    approval_prob:"அனுமதி வாய்ப்பு", run_assessment:"🚀 உண்மையான மதிப்பீடு இயக்கு →",
    churn_check:"வாடிக்கையாளர் இழப்பு கணிப்பான்", churn_sub:"வாடிக்கையாளர் வங்கியை விடுவாரா — Random Forest + SHAP மூலம்",
    label_tenure:"காலம் (ஆண்டுகள்)", label_balance:"கணக்கு இருப்பு (₹)", label_products:"தயாரிப்புகளின் எண்ணிக்கை",
    label_sat:"திருப்தி மதிப்பெண் (1-5)", label_complaints:"புகார்களின் எண்ணிக்கை", label_credit:"கிரெடிட் மதிப்பெண்",
    label_age:"வயது", label_active:"செயலில் உள்ள உறுப்பினரா?", btn_check_churn:"📉 இழப்பு ஆபத்து கணி",
    churn_risk:"ஆபத்து மதிப்பெண்",
    chat_title:"ClarivoX AI கேளு", chat_sub:"உங்கள் மொழியில் வங்கி பற்றி எளிய விடைகள் பெறுங்கள்",
    chat_placeholder:"வங்கி கேள்வி கேளுங்கள்…", chat_welcome:"வணக்கம்! நான் வங்கி முடிவுகளை எளிய மொழியில் விளக்குகிறேன். எதுவும் கேளுங்கள்!",
    send_btn:"அனுப்பு",
    fq1:"EMI என்றால் என்ன?", fq2:"CIBIL மேம்படுத்து", fq3:"கடன் வாங்கணுமா?",
    topic_loan:"🏦 கடன் & EMI", topic_credit:"📊 கிரெடிட் ஸ்கோர்", topic_savings:"💰 சேமிப்பு", topic_insurance:"🛡️ காப்பீடு",
    trans_title:"வெளிப்படைத்தன்மை & சார்பு அறிக்கை", trans_sub:"இந்த AI முடிவு எவ்வளவு நேர்மையானது?",
    trans_score_label:"வெளிப்படைத்தன்மை மதிப்பெண்", trans_good:"✓ நல்ல வெளிப்படைத்தன்மை",
    score_breakdown:"மதிப்பெண் விவரம்", model_conf:"மாடல் நம்பகம்", shap_stability:"SHAP நிலைத்தன்மை",
    bias_check:"சார்பு சரிபார்ப்பு", explainability:"விளக்கத்திறன்",
    bias_detection:"⚖️ சார்பு கண்டறிதல்", potential_bias:"⚠️ சாத்தியமான சார்பு",
    bias_desc:"பயிற்சி தரவில் நகர்ப்புற மற்றும் கிராமப்புற அனுமதி வீதங்களில் வேறுபாடு கண்டறியப்பட்டது.",
    urban_approval:"நகர்ப்புற அனுமதி", rural_approval:"கிராமப்புற அனுமதி", model_info:"மாடல் தகவல்",
    rate_badge:"⭐ ClarivoX மதிப்பிடு", fb_title:"AI எவ்வளவு உதவியாக இருந்தது?",
    fb_sub:"உங்கள் கருத்து அனைவருக்கும் மேம்படுத்த உதவுகிறது",
    fb_placeholder:"என்ன பிடித்தது அல்லது மேம்படுத்தணும் என்று சொல்லுங்கள்…",
    submit_fb:"கருத்து சமர்ப்பி →", fb_thanks:"நன்றி!", fb_submitted:"உங்கள் கருத்து எங்கள் குழுவிற்கு சமர்ப்பிக்கப்பட்டது.",
    back_home:"← முகப்பிற்கு திரும்பு",
    approved:"✅ அனுமதிக்கப்பட்டது", rejected:"❌ நிராகரிக்கப்பட்டது",
    why_approved:"நல்ல செய்தி! உங்கள் விண்ணப்பம் அனுமதி நிலைகளை பூர்த்தி செய்கிறது.",
    why_rejected:"உங்கள் விண்ணப்பம் குறைந்தபட்ச தேவைகளை பூர்த்தி செய்யவில்லை.",
    emode_label:"தனிப்பயன் விளக்கம்", emode_elder:"முதியோர் பயன்முறை", emode_student:"மாணவர் பயன்முறை", emode_professional:"தொழில்முறை பயன்முறை",
    rejection_reasons_title:"❌ ஏன் நிராகரிக்கப்பட்டது?",
    next_steps_title:"✅ அடுத்து என்ன செய்யணும்",
    reapply_label:"📅 எப்போது மீண்டும் விண்ணப்பிக்கலாம்",
    improvement_tip_label:"💡 முக்கிய மேம்பாட்டு குறிப்பு",
    no_rejection_data:"குறிப்பிட்ட நிராகரிப்பு காரணங்கள் இல்லை.",
    likely_approved:"அனுமதிக்கப்படும்", borderline:"எல்லையில் உள்ளது", likely_rejected:"நிராகரிக்கப்படும்",
    tip_cibil:"அதிகபட்ச மேம்பாட்டிற்கு CIBIL மதிப்பெண்ணை 750-க்கு மேல் உயர்த்துங்கள்.",
    tip_income:"₹6 லட்சத்திற்கு மேல் வருமானம் அனுமதி வாய்ப்பை கணிசமாக அதிகரிக்கும்.",
    tip_loan:"அனுமதி வாய்ப்பை மேம்படுத்த கடன் தொகையை குறைக்கவும்.",
    tip_good:"நல்ல சுயவிவரம்! இந்த மதிப்புகளுடன் நீங்கள் அனுமதிக்கப்படுவீர்கள்.",
    ai_decision:"AI முடிவு முடிந்தது", model_sub:"கடன் அனுமதி மதிப்பீடு · LightGBM + SHAP", shap_score_label:"SHAP மதிப்பு", risk_low:"குறைந்த ஆபத்து", risk_medium:"நடுத்தரம்", risk_high:"அதிக ஆபத்து"
  },
  Hindi: {
    nav_home:"होम", nav_chat:"AI चैट", nav_churn:"चर्न",
    pp_profile:"प्रोफ़ाइल बदलें", pp_feedback:"फ़ीडबैक", pp_signout:"साइन आउट",
    chat_welcome_short:"नमस्ते! बैंकिंग, लोन के बारे में पूछें।",
    login_tagline:"लोन, चर्न और बैंकिंग के लिए व्याख्यात्मक AI",
    username:"आपका नाम", enter_btn:"शुरू करें →", guest_btn:"अतिथि के रूप में जारी रखें",
    step1_badge:"चरण 1 / 3", profile_title:"आप कौन हैं?",
    profile_sub:"हम AI स्पष्टीकरण को आपके स्तर के अनुसार व्यक्तिगत बनाएंगे",
    profile_elder:"वरिष्ठ मोड", profile_elder_desc:"सरल भाषा, रोजमर्रा के उदाहरण। कोई जटिल शब्द नहीं।",
    profile_student:"छात्र मोड", profile_student_desc:"स्कूल उदाहरण और शुरुआती अनुकूल संदर्भ।",
    profile_professional:"पेशेवर मोड", profile_professional_desc:"वित्तीय शब्द, SHAP मान और डेटा-संचालित अंतर्दृष्टि।",
    select_btn:"चुनें →",
    hero_title:"विश्वसनीय\nबैंकिंग AI",
    hero_sub:"ClarivoX हर AI बैंकिंग निर्णय को आपकी भाषा में समझाता है — लोन, ग्राहक चर्न, क्रेडिट स्कोर — SHAP और Groq AI द्वारा संचालित।",
    hero_btn1:"🚀 लोन AI जांचें", hero_btn2:"💬 AI से पूछें", hero_btn3:"📉 चर्न प्रेडिक्टर",
    feat_loan_title:"लोन अनुमोदन AI", feat_loan_desc:"जानें आपका लोन क्यों स्वीकृत या अस्वीकृत हुआ।",
    feat_churn_title:"चर्न प्रेडिक्टर", feat_churn_desc:"अनुमान लगाएं कि ग्राहक बैंक छोड़ेगा या नहीं।",
    feat_chat_title:"AI बैंकिंग चैट", feat_chat_desc:"लोन, EMI, क्रेडिट स्कोर के बारे में अपनी भाषा में पूछें।",
    feat_whatif_title:"क्या-अगर सिमुलेटर", feat_whatif_desc:"मान बदलें और लोन अनुमोदन संभावना सीधे देखें।",
    feat_trans_title:"पारदर्शिता रिपोर्ट", feat_trans_desc:"देखें AI निर्णय कितना खुला और निष्पक्ष था।",
    feat_fb_title:"ClarivoX रेट करें", feat_fb_desc:"अपना अनुभव साझा करें और सुधार में मदद करें।",
    analyse_btn:"विश्लेषण →", predict_btn:"अनुमान →", ask_btn:"अभी पूछें →", simulate_btn:"सिमुलेट →", report_btn:"रिपोर्ट देखें →", feedback_btn:"फ़ीडबैक दें →",
    step2_badge:"चरण 2 / 3", usecase_title:"आप क्या जांचना चाहते हैं?", usecase_sub:"एक उपयोग मामला चुनें और व्यक्तिगत AI स्पष्टीकरण पाएं",
    uc_loan:"लोन & EMI", uc_loan_desc:"लोन, ब्याज दरें, EMI गणना के बारे में पूछें।",
    uc_credit:"क्रेडिट स्कोर", uc_credit_desc:"CIBIL स्कोर कैसे सुधारें समझें।",
    uc_savings:"बचत & निवेश", uc_savings_desc:"FD, RD, म्यूचुअल फंड के बारे में जानें।",
    uc_insurance:"बीमा", uc_insurance_desc:"जीवन, स्वास्थ्य, वाहन बीमा समझें।",
    step3_badge:"चरण 3 / 3", loan_form_title:"लोन विवरण दर्ज करें", loan_form_sub:"सटीक AI लोन मूल्यांकन के लिए विवरण भरें",
    label_income:"वार्षिक आय (₹)", label_loan_amt:"लोन राशि (₹)", label_cibil:"CIBIL स्कोर",
    label_term:"लोन अवधि (महीने)", label_edu:"शिक्षा", label_self:"स्व-रोज़गार?",
    label_dep:"आश्रित", label_res:"आवासीय संपत्ति (₹)",
    opt_graduate:"स्नातक", opt_notgraduate:"गैर-स्नातक", opt_yes:"हाँ", opt_no:"नहीं",
    btn_check_loan:"🚀 AI मूल्यांकन चलाएं", privacy_note:"🔒 आपका डेटा स्थानीय रूप से संसाधित होता है",
    confidence:"मॉडल विश्वास", risk_level:"जोखिम स्तर", listen_result:"🔊 परिणाम सुनें",
    view_explanation:"🔍 पूरी व्याख्या देखें →", whatif_btn:"🔧 क्या-अगर सिमुलेटर", trans_btn:"🛡️ पारदर्शिता रिपोर्ट",
    expl_title:"यह निर्णय क्यों लिया गया?", expl_sub:"AI परिणाम को प्रभावित करने वाले शीर्ष SHAP कारक",
    simplify_btn:"🧓 सरल बनाएं", ask_ai_btn:"💬 AI से पूछें",
    whatif_btn2:"🔧 क्या-अगर सिमुलेटर →", trans_btn2:"🛡️ पारदर्शिता रिपोर्ट →",
    shap_weights:"SHAP कारक वजन", analogy_label:"💡 उपमा",
    whatif_title:"क्या-अगर सिमुलेटर", whatif_sub:"स्लाइडर समायोजित करें और लोन अनुमोदन संभावना सीधे देखें",
    sim_income:"💰 वार्षिक आय (₹)", sim_cibil:"📊 CIBIL स्कोर", sim_loan:"🏠 लोन राशि (₹)",
    approval_prob:"अनुमोदन संभावना", run_assessment:"🚀 वास्तविक मूल्यांकन चलाएं →",
    churn_check:"ग्राहक चर्न प्रेडिक्टर", churn_sub:"अनुमान लगाएं ग्राहक बैंक छोड़ेगा — Random Forest + SHAP",
    label_tenure:"कार्यकाल (वर्ष)", label_balance:"खाता शेष (₹)", label_products:"उत्पादों की संख्या",
    label_sat:"संतुष्टि स्कोर (1-5)", label_complaints:"शिकायतों की संख्या", label_credit:"क्रेडिट स्कोर",
    label_age:"आयु", label_active:"सक्रिय सदस्य?", btn_check_churn:"📉 चर्न जोखिम अनुमानित करें",
    churn_risk:"जोखिम स्कोर",
    chat_title:"ClarivoX AI से पूछें", chat_sub:"अपनी भाषा में बैंकिंग पर सरल उत्तर पाएं",
    chat_placeholder:"बैंकिंग प्रश्न पूछें…", chat_welcome:"नमस्ते! मैं बैंकिंग निर्णयों को सरल भाषा में समझाता हूं। कुछ भी पूछें!",
    send_btn:"भेजें",
    fq1:"EMI क्या है?", fq2:"CIBIL सुधारें", fq3:"लोन लेना चाहिए?",
    topic_loan:"🏦 लोन & EMI", topic_credit:"📊 क्रेडिट स्कोर", topic_savings:"💰 बचत", topic_insurance:"🛡️ बीमा",
    trans_title:"पारदर्शिता और पूर्वाग्रह रिपोर्ट", trans_sub:"यह AI निर्णय कितना खुला, विश्वसनीय और निष्पक्ष था?",
    trans_score_label:"पारदर्शिता स्कोर", trans_good:"✓ अच्छी पारदर्शिता",
    score_breakdown:"स्कोर विवरण", model_conf:"मॉडल विश्वास", shap_stability:"SHAP स्थिरता",
    bias_check:"पूर्वाग्रह जांच", explainability:"व्याख्यात्मकता",
    bias_detection:"⚖️ पूर्वाग्रह का पता लगाना", potential_bias:"⚠️ संभावित पूर्वाग्रह",
    bias_desc:"प्रशिक्षण डेटा में शहरी और ग्रामीण अनुमोदन दरों में असमानता पाई गई।",
    urban_approval:"शहरी अनुमोदन", rural_approval:"ग्रामीण अनुमोदन", model_info:"मॉडल जानकारी",
    rate_badge:"⭐ ClarivoX रेट करें", fb_title:"AI कितना उपयोगी था?",
    fb_sub:"आपकी प्रतिक्रिया सभी के लिए सुधार में मदद करती है",
    fb_placeholder:"बताएं क्या पसंद आया या क्या सुधार सकते हैं…",
    submit_fb:"फ़ीडबैक सबमिट करें →", fb_thanks:"धन्यवाद!", fb_submitted:"आपका फ़ीडबैक हमारी टीम को सबमिट किया गया।",
    back_home:"← होम वापस",
    approved:"✅ स्वीकृत", rejected:"❌ अस्वीकृत",
    why_approved:"बधाई! आपका आवेदन अनुमोदन मानदंड पूरे करता है।",
    why_rejected:"आपका आवेदन न्यूनतम मानदंड पूरे नहीं करता।",
    emode_label:"व्यक्तिगत स्पष्टीकरण", emode_elder:"वरिष्ठ मोड", emode_student:"छात्र मोड", emode_professional:"पेशेवर मोड",
    rejection_reasons_title:"❌ अस्वीकरण के कारण",
    next_steps_title:"✅ आगे क्या करें",
    reapply_label:"📅 दोबारा आवेदन कब करें",
    improvement_tip_label:"💡 शीर्ष सुधार सुझाव",
    no_rejection_data:"कोई विशेष अस्वीकरण कारण उपलब्ध नहीं।",
    likely_approved:"संभवतः स्वीकृत", borderline:"सीमारेखा", likely_rejected:"संभवतः अस्वीकृत",
    tip_cibil:"सबसे बड़े सुधार के लिए CIBIL स्कोर 750 से ऊपर बढ़ाएं।",
    tip_income:"₹6L से अधिक आय स्वीकृति की संभावना बढ़ाती है।",
    tip_loan:"स्वीकृति की संभावना सुधारने के लिए लोन राशि कम करें।",
    tip_good:"अच्छा प्रोफाइल! इन मानों के साथ आप स्वीकृत होंगे।"
  },
  Telugu: {
    nav_home:"హోమ్", nav_chat:"AI చాట్", nav_churn:"చర్న్",
    pp_profile:"ప్రొఫైల్ మార్చు", pp_feedback:"అభిప్రాయం", pp_signout:"సైన్ అవుట్",
    chat_welcome_short:"నమస్కారం! బ్యాంకింగ్, లోన్ గురించి అడగండి.",
    login_tagline:"లోన్, చర్న్ & బ్యాంకింగ్ కోసం వివరణ AI",
    username:"మీ పేరు", enter_btn:"ప్రారంభించండి →", guest_btn:"అతిథిగా కొనసాగించండి",
    step1_badge:"దశ 1 / 3", profile_title:"మీరు ఎవరు?",
    profile_sub:"మీ స్థాయికి అనుగుణంగా AI వివరణలను వ్యక్తిగతీకరిస్తాము",
    profile_elder:"వృద్ధుల మోడ్", profile_elder_desc:"సరళ భాష, రోజువారీ ఉదాహరణలు. సంక్లిష్ట పదాలు లేవు.",
    profile_student:"విద్యార్థి మోడ్", profile_student_desc:"పాఠశాల ఉదాహరణలు మరియు మొదటి స్థాయి వివరణలు.",
    profile_professional:"ప్రొఫెషనల్ మోడ్", profile_professional_desc:"ఆర్థిక పదాలు, SHAP విలువలు మరియు డేటా విశ్లేషణ.",
    select_btn:"ఎంచుకోండి →",
    hero_title:"నమ్మకమైన\nబ్యాంకింగ్ AI",
    hero_sub:"ClarivoX ప్రతి AI బ్యాంకింగ్ నిర్ణయాన్ని మీ భాషలో వివరిస్తుంది — లోన్, కస్టమర్ చర్న్, క్రెడిట్ స్కోర్ — SHAP మరియు Groq AI ద్వారా.",
    hero_btn1:"🚀 లోన్ AI తనిఖీ", hero_btn2:"💬 AI అడగండి", hero_btn3:"📉 చర్న్ ప్రిడిక్టర్",
    feat_loan_title:"లోన్ అనుమతి AI", feat_loan_desc:"మీ లోన్ ఎందుకు ఆమోదించబడింది లేదా తిరస్కరించబడిందో అర్థం చేసుకోండి.",
    feat_churn_title:"చర్న్ ప్రిడిక్టర్", feat_churn_desc:"కస్టమర్ బ్యాంక్ వదిలిపోతారా అని అంచనా వేయండి.",
    feat_chat_title:"AI బ్యాంకింగ్ చాట్", feat_chat_desc:"లోన్, EMI, క్రెడిట్ స్కోర్ గురించి మీ భాషలో అడగండి.",
    feat_whatif_title:"ఏమి జరిగితే సిమ్యులేటర్", feat_whatif_desc:"విలువలు మార్చి లోన్ అనుమతి అవకాశాన్ని నేరుగా చూడండి.",
    feat_trans_title:"పారదర్శకత నివేదిక", feat_trans_desc:"AI నిర్ణయం ఎంత నిజాయితీగా ఉందో చూడండి.",
    feat_fb_title:"ClarivoX రేట్ చేయండి", feat_fb_desc:"మీ అనుభవాన్ని పంచుకుని మెరుగుపరచడానికి సహాయపడండి.",
    analyse_btn:"విశ్లేషించు →", predict_btn:"అంచనా వేయు →", ask_btn:"ఇప్పుడు అడగు →", simulate_btn:"సిమ్యులేట్ →", report_btn:"నివేదిక చూడు →", feedback_btn:"అభిప్రాయం ఇవ్వు →",
    step2_badge:"దశ 2 / 3", usecase_title:"మీరు ఏమి తనిఖీ చేయాలనుకుంటున్నారు?", usecase_sub:"ఒక ఉపయోగ కేసు ఎంచుకుని వ్యక్తిగత AI వివరణ పొందండి",
    uc_loan:"లోన్ & EMI", uc_loan_desc:"లోన్, వడ్డీ రేట్లు, EMI లెక్కింపు గురించి అడగండి.",
    uc_credit:"క్రెడిట్ స్కోర్", uc_credit_desc:"CIBIL స్కోర్ ఎలా మెరుగుపరచాలో అర్థం చేసుకోండి.",
    uc_savings:"పొదుపు & పెట్టుబడి", uc_savings_desc:"FD, RD, మ్యూచువల్ ఫండ్ల గురించి తెలుసుకోండి.",
    uc_insurance:"బీమా", uc_insurance_desc:"జీవితం, ఆరోగ్యం, వాహన బీమా అర్థం చేసుకోండి.",
    step3_badge:"దశ 3 / 3", loan_form_title:"లోన్ వివరాలు నమోదు చేయండి", loan_form_sub:"ఖచ్చితమైన AI లోన్ మూల్యాంకనానికి వివరాలు నమోదు చేయండి",
    label_income:"వార్షిక ఆదాయం (₹)", label_loan_amt:"లోన్ మొత్తం (₹)", label_cibil:"CIBIL స్కోర్",
    label_term:"లోన్ కాలం (నెలలు)", label_edu:"విద్య", label_self:"స్వయం ఉపాధి?",
    label_dep:"ఆధారపడిన వారు", label_res:"నివాస ఆస్తులు (₹)",
    opt_graduate:"గ్రాడ్యుయేట్", opt_notgraduate:"నాన్-గ్రాడ్యుయేట్", opt_yes:"అవును", opt_no:"కాదు",
    btn_check_loan:"🚀 AI మూల్యాంకనం అమలు చేయండి", privacy_note:"🔒 మీ డేటా స్థానికంగా ప్రాసెస్ చేయబడుతుంది",
    confidence:"మోడల్ నమ్మకం", risk_level:"రిస్క్ స్థాయి", listen_result:"🔊 ఫలితం వినండి",
    view_explanation:"🔍 పూర్తి వివరణ చూడండి →", whatif_btn:"🔧 ఏమి జరిగితే సిమ్యులేటర్", trans_btn:"🛡️ పారదర్శకత నివేదిక",
    expl_title:"ఈ నిర్ణయం ఎందుకు తీసుకోబడింది?", expl_sub:"AI ఫలితాన్ని ప్రభావితం చేసిన టాప్ SHAP కారకాలు",
    simplify_btn:"🧓 సరళీకరించు", ask_ai_btn:"💬 AI అడగు",
    whatif_btn2:"🔧 ఏమి జరిగితే సిమ్యులేటర్ →", trans_btn2:"🛡️ పారదర్శకత నివేదిక →",
    shap_weights:"SHAP కారక బరువులు", analogy_label:"💡 ఉపమానం",
    whatif_title:"ఏమి జరిగితే సిమ్యులేటర్", whatif_sub:"స్లైడర్లు సర్దుబాటు చేసి లోన్ అనుమతి సంభావ్యత నేరుగా చూడండి",
    sim_income:"💰 వార్షిక ఆదాయం (₹)", sim_cibil:"📊 CIBIL స్కోర్", sim_loan:"🏠 లోన్ మొత్తం (₹)",
    approval_prob:"అనుమతి సంభావ్యత", run_assessment:"🚀 అసలు మూల్యాంకనం అమలు చేయండి →",
    churn_check:"కస్టమర్ చర్న్ ప్రిడిక్టర్", churn_sub:"కస్టమర్ బ్యాంక్ వదిలిపోతారా — Random Forest + SHAP",
    label_tenure:"కాలం (సంవత్సరాలు)", label_balance:"ఖాతా బ్యాలెన్స్ (₹)", label_products:"ఉత్పత్తుల సంఖ్య",
    label_sat:"సంతృప్తి స్కోర్ (1-5)", label_complaints:"ఫిర్యాదుల సంఖ్య", label_credit:"క్రెడిట్ స్కోర్",
    label_age:"వయస్సు", label_active:"యాక్టివ్ సభ్యుడా?", btn_check_churn:"📉 చర్న్ రిస్క్ అంచనా వేయండి",
    churn_risk:"రిస్క్ స్కోర్",
    chat_title:"ClarivoX AI అడగండి", chat_sub:"మీ భాషలో బ్యాంకింగ్ పై సరళ సమాధానాలు పొందండి",
    chat_placeholder:"బ్యాంకింగ్ ప్రశ్న అడగండి…", chat_welcome:"నమస్కారం! నేను బ్యాంకింగ్ నిర్ణయాలను సరళ భాషలో వివరిస్తాను. ఏదైనా అడగండి!",
    send_btn:"పంపు",
    fq1:"EMI అంటే ఏమిటి?", fq2:"CIBIL మెరుగుపరచు", fq3:"లోన్ తీసుకోవాలా?",
    topic_loan:"🏦 లోన్ & EMI", topic_credit:"📊 క్రెడిట్ స్కోర్", topic_savings:"💰 పొదుపు", topic_insurance:"🛡️ బీమా",
    trans_title:"పారదర్శకత & పక్షపాత నివేదిక", trans_sub:"ఈ AI నిర్ణయం ఎంత నిజాయితీగా ఉంది?",
    trans_score_label:"పారదర్శకత స్కోర్", trans_good:"✓ మంచి పారదర్శకత",
    score_breakdown:"స్కోర్ వివరాలు", model_conf:"మోడల్ నమ్మకం", shap_stability:"SHAP స్థిరత్వం",
    bias_check:"పక్షపాత తనిఖీ", explainability:"వివరణాత్మకత",
    bias_detection:"⚖️ పక్షపాత గుర్తింపు", potential_bias:"⚠️ సంభావ్య పక్షపాతం",
    bias_desc:"శిక్షణ డేటాలో పట్టణ మరియు గ్రామీణ అనుమతి రేట్లలో వ్యత్యాసం కనుగొనబడింది.",
    urban_approval:"పట్టణ అనుమతి", rural_approval:"గ్రామీణ అనుమతి", model_info:"మోడల్ సమాచారం",
    rate_badge:"⭐ ClarivoX రేట్ చేయండి", fb_title:"AI ఎంత ఉపయోగకరంగా ఉంది?",
    fb_sub:"మీ అభిప్రాయం అందరికీ మెరుగుపరచడంలో సహాయపడుతుంది",
    fb_placeholder:"మీకు ఏమి నచ్చింది లేదా మెరుగుపరచాలో చెప్పండి…",
    submit_fb:"అభిప్రాయం సమర్పించండి →", fb_thanks:"ధన్యవాదాలు!", fb_submitted:"మీ అభిప్రాయం మా టీమ్‌కు సమర్పించబడింది.",
    back_home:"← హోమ్‌కి తిరిగి"
  },
  Malayalam: {
    nav_home:"ഹോം", nav_chat:"AI ചാറ്റ്", nav_churn:"ചേർൺ",
    pp_profile:"പ്രൊഫൈൽ മാറ്റുക", pp_feedback:"ഫീഡ്ബാക്ക്", pp_signout:"സൈൻ ഔട്ട്",
    chat_welcome_short:"നമസ്കാരം! ബ്യാങ്കിംഗ്, ലോൺ കാര്യങ്ങൾ ചോദിക്കൂ.",
    login_tagline:"ലോൺ, ചേർൺ & ബ്യാങ്കിംഗിനുള്ള വ്യക്തമായ AI",
    username:"നിങ്ങളുടെ പേര്", enter_btn:"ആരംഭിക്കുക →", guest_btn:"അതിഥിയായി തുടരുക",
    step1_badge:"ഘട്ടം 1 / 3", profile_title:"നിങ്ങൾ ആരാണ്?",
    profile_sub:"AI വിശദീകരണം നിങ്ങളുടെ നിലവാരത്തിനനുസരിച്ച് ക്രമീകരിക്കും",
    profile_elder:"മുതിർന്നവർ മോഡ്", profile_elder_desc:"ലളിതഭാഷ, ജീവിത ഉദാഹരണങ്ങൾ. ബ്യാങ്കിംഗ് സാങ്കേതിക പദങ്ങളില്ല.",
    profile_student:"വിദ്യാർത്ഥി മോഡ്", profile_student_desc:"സ്കൂൾ ഉദാഹരണങ്ങളും തുടക്കക്കാർക്ക് അനുയോജ്യമായ വിശദീകരണങ്ങളും.",
    profile_professional:"പ്രൊഫഷണൽ മോഡ്", profile_professional_desc:"ധനകാര്യ പദങ്ങൾ, SHAP മൂല്യങ്ങൾ, ഡേറ്റ അടിസ്ഥാനമാക്കിയ ഉൾക്കാഴ്ചകൾ.",
    select_btn:"തിരഞ്ഞെടുക്കുക →",
    hero_title:"വിശ്വാസ്യയോഗ്യമായ\nബ്യാങ്കിംഗ് AI",
    hero_sub:"ClarivoX ഓരോ AI ബ്യാങ്കിംഗ് തീരുമാനവും നിങ്ങളുടെ ഭാഷയിൽ വിശദീകരിക്കുന്നു.",
    hero_btn1:"🚀 ലോൺ AI പരിശോധന", hero_btn2:"💬 AI ചോദിക്കുക", hero_btn3:"📉 ചേർൺ പ്രവചനം",
    feat_loan_title:"ലോൺ അംഗീകാര AI", feat_loan_desc:"ലോൺ അംഗീകരിച്ചതിന്റെ അല്ലെങ്കിൽ നിരസിച്ചതിന്റെ കാരണം മനസ്സിലാക്കുക.",
    feat_churn_title:"ചേർൺ പ്രവചകൻ", feat_churn_desc:"ഉപഭോക്താവ് ബ്യാങ്ക് വിടുമോ എന്ന് പ്രവചിക്കുക.",
    feat_chat_title:"AI ബ്യാങ്കിംഗ് ചാറ്റ്", feat_chat_desc:"ലോൺ, EMI, ക്രെഡിറ്റ് സ്കോറിനെ കുറിച്ച് മലയാളത്തിൽ ചോദിക്കൂ.",
    feat_whatif_title:"എന്ത്-ആണ് സിമുലേറ്റർ", feat_whatif_desc:"മൂല്യങ്ങൾ മാറ്റി ലോൺ അംഗീകാര സാധ്യത നേരിട്ട് കാണുക.",
    feat_trans_title:"സുതാര്യതാ റിപ്പോർട്ട്", feat_trans_desc:"AI തീരുമാനം എത്ര തുറന്നതും നീതിയുക്തവും ആണ് കാണുക.",
    feat_fb_title:"ClarivoX റേറ്റ് ചെയ്യുക", feat_fb_desc:"നിങ്ങളുടെ അനുഭവം പങ്കിടൂ.",
    analyse_btn:"വിശകലനം →", predict_btn:"പ്രവചിക്കൂ →", ask_btn:"ഇപ്പോൾ ചോദിക്കൂ →",
    simulate_btn:"സിമുലേറ്റ് →", report_btn:"റിപ്പോർട്ട് കാണുക →", feedback_btn:"ഫീഡ്ബാക്ക് നൽകൂ →",
    step2_badge:"ഘട്ടം 2 / 3", usecase_title:"എന്ത് പരിശോധിക്കണം?",
    usecase_sub:"ഒരു ഉദ്ദേശ്യം തിരഞ്ഞെടുത്ത് വ്യക്തിഗത AI വിശദീകരണം നേടുക",
    uc_loan:"ലോൺ & EMI", uc_loan_desc:"ലോൺ, പലിശ, EMI കണക്കുകൂട്ടൽ ചോദിക്കൂ.",
    uc_credit:"ക്രെഡിറ്റ് സ്കോർ", uc_credit_desc:"CIBIL സ്കോർ എങ്ങനെ മെച്ചപ്പെടുത്താം.",
    uc_savings:"സമ്പാദ്യം & നിക്ഷേപം", uc_savings_desc:"FD, RD, മ്യൂച്ചൽ ഫണ്ടിനെ കുറിച്ച് അറിയൂ.",
    uc_insurance:"ഇൻഷുറൻസ്", uc_insurance_desc:"ജീവൻ, ആരോഗ്യ, വാഹന ഇൻഷുറൻസ് മനസ്സിലാക്കൂ.",
    step3_badge:"ഘട്ടം 3 / 3", loan_form_title:"ലോൺ വിവരങ്ങൾ നൽകുക",
    loan_form_sub:"കൃത്യമായ AI ലോൺ മൂല്യനിർണ്ണയത്തിന് വിവരങ്ങൾ പൂരിപ്പിക്കൂ",
    label_income:"വാർഷിക വരുമാനം (₹)", label_loan_amt:"ലോൺ തുക (₹)", label_cibil:"CIBIL സ്കോർ",
    label_term:"ലോൺ കാലാവധി (മാസം)", label_edu:"വിദ്യാഭ്യാസം", label_self:"സ്വയം തൊഴിൽ?",
    label_dep:"ആശ്രിതർ", label_res:"ആവാസ സ്വത്തുക്കൾ (₹)",
    opt_graduate:"ബിരുദധാരി", opt_notgraduate:"ബിരുദധാരിയല്ല", opt_yes:"അതെ", opt_no:"ഇല്ല",
    btn_check_loan:"🚀 AI മൂല്യനിർണ്ണയം", privacy_note:"🔒 നിങ്ങളുടെ ഡേറ്റ ഒരിക്കലും സൂക്ഷിക്കില്ല",
    confidence:"മോഡൽ വിശ്വാസ്യത", risk_level:"റിസ്ക് നില", listen_result:"🔊 ഫലം കേൾക്കൂ",
    view_explanation:"🔍 പൂർണ്ണ വിശദീകരണം →", whatif_btn:"🔧 എന്ത്-ആണ് സിമുലേറ്റർ",
    trans_btn:"🛡️ സുതാര്യതാ റിപ്പോർട്ട്",
    expl_title:"ഈ തീരുമാനം എടുക്കാൻ കാരണം?",
    expl_sub:"AI ഫലത്തെ സ്വാധീനിച്ച പ്രധാന SHAP ഘടകങ്ങൾ",
    simplify_btn:"🧓 ലളിതമാക്കുക", ask_ai_btn:"💬 AI ചോദിക്കൂ",
    whatif_btn2:"🔧 എന്ത്-ആണ് സിമുലേറ്റർ →", trans_btn2:"🛡️ സുതാര്യതാ റിപ്പോർട്ട് →",
    shap_weights:"SHAP ഘടക ഭാരം", analogy_label:"💡 ഉദാഹരണം",
    whatif_title:"എന്ത്-ആണ് സിമുലേറ്റർ",
    whatif_sub:"ലോൺ അംഗീകാര സാധ്യത നേരിട്ട് കാണാൻ സ്ലൈഡറുകൾ ക്രമീകരിക്കൂ",
    sim_income:"💰 വാർഷിക വരുമാനം (₹)", sim_cibil:"📊 CIBIL സ്കോർ", sim_loan:"🏠 ലോൺ തുക (₹)",
    approval_prob:"അംഗീകാര സാധ്യത", run_assessment:"🚀 യഥാർത്ഥ മൂല്യനിർണ്ണയം →",
    churn_check:"ഉപഭോക്തൃ ചേർൺ പ്രവചകൻ",
    churn_sub:"ഉപഭോക്താവ് ബ്യാങ്ക് വിടുമോ — Random Forest + SHAP",
    label_tenure:"കാലാവധി (വർഷം)", label_balance:"അക്കൗണ്ട് ബാലൻസ് (₹)",
    label_products:"ഉൽപ്പന്നങ്ങളുടെ എണ്ണം", label_sat:"സംതൃപ്തി (1-5)",
    label_complaints:"പരാതികൾ", label_credit:"ക്രെഡിറ്റ് സ്കോർ",
    label_age:"പ്രായം", label_active:"സജീവ അംഗമാണോ?", btn_check_churn:"📉 ചേർൺ റിസ്ക് പ്രവചിക്കൂ",
    churn_risk:"റിസ്ക് സ്കോർ",
    chat_title:"ClarivoX AI ചോദിക്കൂ",
    chat_sub:"നിങ്ങളുടെ ഭാഷയിൽ ബ്യാങ്കിംഗ് ഉത്തരങ്ങൾ നേടൂ",
    chat_placeholder:"ബ്യാങ്കിംഗ് ചോദ്യം ചോദിക്കൂ…",
    chat_welcome:"നമസ്കാരം! ഞാൻ ബ്യാങ്കിംഗ് തീരുമാനങ്ങൾ ലളിതഭാഷയിൽ വിശദീകരിക്കാം.",
    send_btn:"അയക്കുക",
    fq1:"EMI എന്നാൽ എന്ത്?", fq2:"CIBIL മെച്ചപ്പെടുത്തുക", fq3:"ലോൺ എടുക്കണോ?",
    topic_loan:"🏦 ലോൺ & EMI", topic_credit:"📊 ക്രെഡിറ്റ് സ്കോർ",
    topic_savings:"💰 സമ്പാദ്യം", topic_insurance:"🛡️ ഇൻഷുറൻസ്",
    trans_title:"സുതാര്യത & പക്ഷപാത റിപ്പോർട്ട്",
    trans_sub:"ഈ AI തീരുമാനം എത്ര തുറന്നതും നീതിയുക്തവും?",
    trans_score_label:"സുതാര്യതാ സ്കോർ", trans_good:"✓ നല്ല സുതാര്യത",
    score_breakdown:"സ്കോർ വിവരം", model_conf:"മോഡൽ വിശ്വാസ്യത",
    shap_stability:"SHAP സ്ഥിരത", bias_check:"പക്ഷപാത പരിശോധന", explainability:"വ്യക്തത",
    bias_detection:"⚖️ പക്ഷപാത കണ്ടെത്തൽ", potential_bias:"⚠️ സംഭാവ്യ പക്ഷപാതം",
    bias_desc:"പരിശീലന ഡേറ്റയിൽ നഗര-ഗ്രാമ അംഗീകാര നിരക്കുകളിൽ വ്യത്യാസം കണ്ടെത്തി.",
    urban_approval:"നഗര അംഗീകാരം", rural_approval:"ഗ്രാമ അംഗീകാരം", model_info:"മോഡൽ വിവരം",
    rate_badge:"⭐ ClarivoX റേറ്റ് ചെയ്യുക", fb_title:"AI എത്ര ഉപകാരപ്രദമായിരുന്നു?",
    fb_sub:"നിങ്ങളുടെ ഫീഡ്ബാക്ക് എല്ലാവർക്കും മെച്ചപ്പെടുത്താൻ സഹായിക്കുന്നു",
    fb_placeholder:"ഇഷ്ടമായത് അല്ലെങ്കിൽ മെച്ചപ്പെടുത്തേണ്ടത് പറയൂ…",
    submit_fb:"ഫീഡ്ബാക്ക് സമർപ്പിക്കൂ →", fb_thanks:"നന്ദി!",
    fb_submitted:"നിങ്ങളുടെ ഫീഡ്ബാക്ക് ഞങ്ങളുടെ ടീമിന് ലഭിച്ചു.",
    back_home:"← ഹോമിലേക്ക് മടങ്ങൂ",
    likely_approved:"അംഗീകൃതമാകും", borderline:"അതിർത്തി", likely_rejected:"നിരസിക്കപ്പെടും",
    tip_cibil:"💡 ഏറ്റവും വലിയ ബൂസ്റ്റിന് CIBIL 750-ൽ കൂടുതൽ ആക്കൂ.",
    tip_income:"💡 ₹6L-ൽ കൂടുതൽ വരുമാനം അംഗീകാര സാധ്യത ഗണ്യമായി വർദ്ധിപ്പിക്കുന്നു.",
    tip_loan:"💡 അംഗീകാര സാധ്യത മെച്ചപ്പെടുത്താൻ ലോൺ തുക കുറയ്ക്കൂ.",
    tip_good:"🎉 നല്ല പ്രൊഫൈൽ! ഈ മൂല്യങ്ങൾ ഉള്ളപ്പോൾ അംഗീകൃതമാകും.",
    positive:"പോസിറ്റീവ്", negative:"നെഗറ്റീവ്",
    approved:"✅ അംഗീകരിച്ചു", rejected:"❌ നിരസിച്ചു",
    why_approved:"അഭിനന്ദനങ്ങൾ! നിങ്ങളുടെ അപേക്ഷ അംഗീകാര മാനദണ്ഡങ്ങൾ പൂർത്തിയാക്കി.",
    why_rejected:"നിങ്ങളുടെ അപേക്ഷ ഏറ്റവും കുറഞ്ഞ മാനദണ്ഡങ്ങൾ പൂർത്തിയാക്കിയില്ല.",
    emode_label:"വ്യക്തിഗത വിശദീകരണം", emode_elder:"മുതിർന്നവർ മോഡ്", emode_student:"വിദ്യാർത്ഥി മോഡ്", emode_professional:"പ്രൊഫഷണൽ മോഡ്",
    rejection_reasons_title:"❌ നിരസിക്കാനുള്ള കാരണങ്ങൾ",
    next_steps_title:"✅ അടുത്ത ഘട്ടങ്ങൾ",
    reapply_label:"📅 വീണ്ടും അപേക്ഷിക്കാൻ എപ്പോൾ",
    improvement_tip_label:"💡 പ്രധാന മെച്ചപ്പെടുത്തൽ നുറുങ്ങ്",
    no_rejection_data:"പ്രത്യേക നിരസിക്കൽ കാരണങ്ങൾ ലഭ്യമല്ല.",
    likely_approved:"അംഗീകരിക്കപ്പെടും", borderline:"അതിർത്തിയിൽ", likely_rejected:"നിരസിക്കപ്പെടും",
    tip_cibil:"ഏറ്റവും വലിയ ബൂസ്റ്റിന് CIBIL 750-ൽ കൂടുതൽ ആക്കൂ.",
    tip_income:"₹6L-ൽ കൂടുതൽ വരുമാനം അംഗീകാര സാധ്യത ഗണ്യമായി വർദ്ധിപ്പിക്കുന്നു.",
    tip_loan:"അംഗീകാര സാധ്യത മെച്ചപ്പെടുത്താൻ ലോൺ തുക കുറയ്ക്കൂ.",
    tip_good:"നല്ല പ്രൊഫൈൽ! ഈ മൂല്യങ്ങൾ ഉള്ളപ്പോൾ അംഗീകൃതമാകും.",
    ai_decision:"AI തീരുമാനം പൂർത്തിയായി", model_sub:"ലോൺ അംഗീകാര മൂല്യനിർണ്ണയം · LightGBM + SHAP", shap_score_label:"SHAP സ്കോർ", risk_low:"കുറഞ്ഞ റിസ്ക്", risk_medium:"ഇടത്തരം", risk_high:"ഉയർന്ന റിസ്ക്"
  }
};

// ═══════════════════════════════════════════════
// LANGUAGE SWITCHING — Apply translations to DOM
// ═══════════════════════════════════════════════
function applyTranslations(lang){
  const labels = T[lang] || T.English;
  // Update all data-label elements
  document.querySelectorAll('[data-label]').forEach(el=>{
    const key = el.getAttribute('data-label');
    if(!labels[key]) return;
    const tag = el.tagName.toLowerCase();
    if(tag==='input'||tag==='textarea') el.placeholder = labels[key];
    else if(tag==='option') el.textContent = labels[key];
    else el.textContent = labels[key];
  });
  // Update placeholder-only elements
  document.querySelectorAll('[data-placeholder-label]').forEach(el=>{
    const key = el.getAttribute('data-placeholder-label');
    if(labels[key]) el.placeholder = labels[key];
  });
  // Update topbar lang buttons
  const codeMap={English:'EN',Tamil:'TA',Hindi:'HI',Malayalam:'ML'};
  document.querySelectorAll('.tb-lang-btn').forEach(btn=>{
    btn.classList.remove('active');
    if(btn.textContent.trim()===(codeMap[lang]||'')) btn.classList.add('active');
  });
  // Update chatLang selector
  const cl=document.getElementById('chatLang');
  if(cl) cl.value=lang;
  // Update document lang
  const htmlLangMap={English:'en',Tamil:'ta',Hindi:'hi',Malayalam:'ml'};
  document.documentElement.lang=htmlLangMap[lang]||'en';
}

function switchLang(lang, btn){
  S.language = lang;
  applyTranslations(lang);
  // Update topbar active state
  document.querySelectorAll('.tb-lang-btn').forEach(b=>b.classList.remove('active'));
  if(btn) btn.classList.add('active');
  // Update login lang buttons too if on login page
  document.querySelectorAll('.lang-btn').forEach(b=>{
    b.classList.remove('active');
    const bl = b.getAttribute('onclick')||'';
    if(bl.includes(`'${lang}'`)) b.classList.add('active');
  });
}

function setLang(b, lang){
  document.querySelectorAll('.lang-btn').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');
  S.language=lang;
  applyTranslations(lang);
}

function updateChatLang(){
  const cl=document.getElementById('chatLang');
  if(cl){ S.language=cl.value; applyTranslations(cl.value); }
}

// ═══════════════════════════════════════════════
// VOICE AI — Multilingual TTS + STT
// ═══════════════════════════════════════════════
const LANG_CODES = {
  English:'en-IN', Tamil:'ta-IN', Hindi:'hi-IN', Malayalam:'ml-IN',
  Telugu:'te-IN', Kannada:'kn-IN', Marathi:'mr-IN', Bengali:'bn-IN'
};

// Voice fallback priority order per language
const VOICE_FALLBACKS = {
  Tamil:     ['ta','ta-IN','ta-LK'],
  Hindi:     ['hi','hi-IN'],
  Malayalam: ['ml','ml-IN'],
  Telugu:    ['te','te-IN'],
  Kannada:   ['kn','kn-IN'],
  English:   ['en-IN','en-GB','en-US']
};

// Text-to-Speech — speaks text in current language with robust fallback
function speak(text, lang){
  if(!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = LANG_CODES[lang||S.language] || 'en-IN';
  utter.rate = (lang==='Tamil'||lang==='Malayalam') ? 0.85 : 0.9;
  utter.pitch = 1;

  // Try each fallback code until a matching voice is found
  const voices = window.speechSynthesis.getVoices();
  const fallbacks = VOICE_FALLBACKS[lang] || VOICE_FALLBACKS['English'];
  let matched = null;
  for(const code of fallbacks){
    matched = voices.find(v=>v.lang===code) ||
              voices.find(v=>v.lang.startsWith(code.split('-')[0]));
    if(matched) break;
  }
  if(!matched) matched = voices.find(v=>v.lang.startsWith('en'));
  if(matched) utter.voice = matched;

  const btn = document.getElementById('voiceResultBtn');
  if(btn){
    btn.innerHTML = '⏹ Stop';
    btn.onclick = ()=>{ window.speechSynthesis.cancel(); resetVoiceBtn(); };
  }
  utter.onend = ()=>resetVoiceBtn();
  utter.onerror = ()=>resetVoiceBtn();
  window.speechSynthesis.speak(utter);
}

function resetVoiceBtn(){
  const btn=document.getElementById('voiceResultBtn');
  if(btn){ btn.innerHTML='🔊 <span data-label="listen_result">'+((T[S.language]||T.English).listen_result||'Listen to Result')+'</span>'; btn.onclick=speakResult; }
}

function speakResult(){
  if(!S.loanResult) return;
  const la = (T[S.language]||T.English);
  const approved = S.loanResult.prediction==='Approved';
  const voice_txt = S.loanResult.voice_summary || (approved ? la.approved||'Approved' : la.rejected||'Rejected');
  speak(voice_txt, S.language);
}

function speakChurnResult(){
  if(!window._lastChurnData) return;
  const d=window._lastChurnData;
  const txt = d.voice_summary || (d.will_churn ? (T[S.language]||T.English).will_leave||'High churn risk' : (T[S.language]||T.English).will_stay||'Customer will stay');
  speak(txt, S.language);
}

// Speak any AI bubble text
function speakBubble(text){
  speak(text, S.language);
}

// Add speak button to AI bubbles
function addSpeakBtn(bubbleEl, text){
  const btn = document.createElement('button');
  btn.className='bubble-speak';
  btn.innerHTML='🔊';
  btn.title='Listen';
  btn.onclick=()=>speakBubble(text);
  bubbleEl.appendChild(btn);
}

// Speech-to-Text (Voice Input)
let recognition = null;
let isRecording = false;

function initSpeechRecognition(){
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR){ console.warn('Speech recognition not supported'); return null; }
  const r = new SR();
  r.continuous = false;
  r.interimResults = true;
  r.maxAlternatives = 1;
  return r;
}

function toggleVoiceInput(){
  if(isRecording){ stopRecording(); return; }
  startRecording();
}

function startRecording(){
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR){ alert('Voice input not supported in this browser. Use Chrome.'); return; }
  recognition = new SR();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = LANG_CODES[S.language] || 'en-IN';

  const micBtn = document.getElementById('micBtn');
  const indicator = document.getElementById('voiceIndicator');
  const voiceStatus = document.getElementById('voiceStatus');
  const inp = document.getElementById('chatInp');

  micBtn.className='voice-btn recording';
  micBtn.innerHTML='⏹';
  indicator.className='voice-indicator show';
  voiceStatus.textContent = {English:'Listening…',Tamil:'கேட்கிறேன்…',Hindi:'सुन रहा हूं…',Malayalam:'കേൾക്കുന്നു…'}[S.language]||'Listening…';
  isRecording=true;

  recognition.onresult=(e)=>{
    let interim='',final='';
    for(let i=e.resultIndex;i<e.results.length;i++){
      if(e.results[i].isFinal) final+=e.results[i][0].transcript;
      else interim+=e.results[i][0].transcript;
    }
    inp.value=final||interim;
  };

  recognition.onend=()=>{
    stopRecording();
    if(inp.value.trim()) sendChat();
  };

  recognition.onerror=(e)=>{
    console.warn('Speech error:',e.error);
    stopRecording();
  };

  recognition.start();
}

function stopRecording(){
  isRecording=false;
  if(recognition){ try{recognition.stop();}catch(e){} recognition=null; }
  const micBtn=document.getElementById('micBtn');
  const indicator=document.getElementById('voiceIndicator');
  if(micBtn){ micBtn.className='voice-btn'; micBtn.innerHTML='🎤'; }
  if(indicator) indicator.className='voice-indicator';
}

// Load voices (needed for some browsers)
if(window.speechSynthesis){
  window.speechSynthesis.onvoiceschanged=()=>{ window.speechSynthesis.getVoices(); };
}

// ─────────────────────────────────────────
// VOICE CONVERSATION MODE — Toggle auto-speak on AI responses
// ─────────────────────────────────────────
function toggleVoiceMode(){
  S.voiceMode = !S.voiceMode;
  const btn = document.getElementById('voiceModeBtn');
  const lbl = document.getElementById('voiceModeLbl');
  if(!btn||!lbl) return;
  if(S.voiceMode){
    btn.style.background='rgba(124,110,250,0.25)';
    btn.style.borderColor='rgba(124,110,250,0.7)';
    lbl.textContent='Voice Mode: ON';
    btn.classList.add('voice-mode-on');
    // Greet user in voice
    const greet = {English:'Voice mode enabled. I will speak every response aloud.',
      Tamil:'குரல் முறை இயக்கப்பட்டது.',
      Hindi:'आवाज़ मोड चालू है।',
      Malayalam:'ശബ്ദ മോഡ് ഓണാണ്.'};
    speak(greet[S.language]||greet.English, S.language);
  } else {
    btn.style.background='rgba(124,110,250,0.08)';
    btn.style.borderColor='rgba(124,110,250,0.4)';
    lbl.textContent='Voice Mode: Off';
    btn.classList.remove('voice-mode-on');
    window.speechSynthesis.cancel();
  }
}

// ══════════════════════════════════════
// NAVIGATION
// ══════════════════════════════════════
function goTo(id){
  if(S.page!==id) S.hist.push(S.page);
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  const el=document.getElementById(id);
  if(!el){console.warn('Missing page:',id);return;}
  el.classList.add('active');
  S.page=id;
  updateTopbar();
  onEnter(id);
  window.scrollTo(0,0);
}
function goBack(){
  if(!S.hist.length) return;
  const prev=S.hist.pop();
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  const el=document.getElementById(prev);
  if(!el) return;
  el.classList.add('active');
  S.page=prev;
  updateTopbar();
  onEnter(prev);
  window.scrollTo(0,0);
}

function updateTopbar(){
  const hide=['splash','login'].includes(S.page);
  document.getElementById('topbar').style.display=hide?'none':'flex';
  document.getElementById('floatChat').classList.toggle('show',!hide && S.page!=='chat');
  const bb=document.getElementById('backBtn');
  const noBack=['home','profile','splash','login'].includes(S.page);
  bb.classList.toggle('show',!noBack && S.hist.length>0);
  const bar=document.getElementById('stepBar');
  bar.innerHTML='';
  const ci=STEP_PAGES.indexOf(S.page);
  STEP_PAGES.forEach((_,i)=>{
    const d=document.createElement('div');
    d.className='sdot'+(i<ci?' done':i===ci?' cur':'');
    bar.appendChild(d);
  });
  if(S.profile){
    const initials=(S.guest?'G':S.userName[0]||'U').toUpperCase();
    ['tav','ppav'].forEach(id=>{const e=document.getElementById(id);if(e)e.textContent=initials;});
    document.getElementById('tpname').textContent=S.guest?'Guest':S.userName;
    const la_tp=T[S.language]||T.English;
    const pmodeMap={Elder:la_tp.emode_elder||'Elder Mode',Student:la_tp.emode_student||'Student Mode',Professional:la_tp.emode_professional||'Professional Mode'};
    document.getElementById('tpmode').textContent=pmodeMap[S.profile]||(S.profile+' Mode');
    document.getElementById('ppname').textContent=S.guest?'Guest User':S.userName;
  }
}

function onEnter(id){
  // Re-apply all data-label translations every time a page is entered
  applyTranslations(S.language);
  if(id==='airesult'&&S.loanResult) showLoanResult(S.loanResult);
  if(id==='explanation'&&S.loanResult) showExplanation(S.loanResult);
  if(id==='whatif') updateSim();
  if(id==='home'){
    const n=S.guest?'Explorer':S.userName.split(' ')[0];
    document.getElementById('hbadge').textContent=`👋 Welcome, ${n}`;
    const la=T[S.language]||T.English;
    if(S.profile==='Elder') document.getElementById('htext').textContent=la.hero_sub||"We'll explain every AI banking decision in clear, simple language.";
    else if(S.profile==='Professional') document.getElementById('htext').textContent=la.hero_sub||"Access SHAP-powered AI explanations, bias audits, and full transparency reports.";
    else { const p=document.getElementById('htext'); if(p) p.textContent=la.hero_sub||p.textContent; }
  }
}

// SPLASH
setTimeout(()=>goTo('login'),3100);

// LOGIN
async function checkServer(){
  try{
    const r=await fetch(API+'/health');
    const d=await r.json();
    const online=d.status==='healthy';
    document.getElementById('loginDot').className='status-dot'+(online?' online':'');
    document.getElementById('loginStatus').textContent=online?'Backend connected ✓':'Backend offline — check server';
  }catch{
    document.getElementById('loginDot').className='status-dot';
    document.getElementById('loginStatus').textContent='Cannot reach backend';
  }
}
checkServer();

function doLogin(){
  const nm=document.getElementById('lname').value.trim();
  S.userName=nm||'User';
  S.guest=false;
  goTo('profile');
}
function doLoginGuest(){S.guest=true;goTo('profile');}

function selProfile(mode,card){
  document.querySelectorAll('.pcard').forEach(c=>c.classList.remove('sel'));
  card.classList.add('sel');
  S.profile=mode;
  setTimeout(()=>goTo('home'),350);
}

function selUC(uc,card){
  document.querySelectorAll('.uccard').forEach(c=>c.style.borderColor='');
  card.style.borderColor='rgba(124,110,250,.6)';
  S.useCase=uc;
  setTimeout(()=>goTo('inputform'),280);
}

// LOAN SUBMIT
async function submitLoan(){
  const income=+document.getElementById('fIncome').value;
  const loan=+document.getElementById('fLoan').value;
  const cibil=+document.getElementById('fCibil').value;
  const term=+document.getElementById('fTerm').value||12;
  const edu=document.getElementById('fEdu').value;
  const selfEmp=document.getElementById('fSelf').value;
  const dep=+document.getElementById('fDep').value||0;
  const res=+document.getElementById('fRes').value||0;
  if(!income||!loan||!cibil){alert('Please fill in Income, Loan Amount, and CIBIL Score!');return;}
  const btn=document.getElementById('loanBtn');
  btn.innerHTML='<div class="spinner"></div> Analysing…';
  btn.disabled=true;
  try{
    const r=await fetch(API+'/api/loan/predict',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({income,loan_amount:loan,cibil_score:cibil,loan_term:term,education:edu,self_employed:selfEmp,dependents:dep,residential_assets:res,profile:S.profile,language:S.language})
    });
    const data=await r.json();
    S.loanResult=data;
    goTo('airesult');
  }catch(e){alert('Error connecting to backend! Make sure python main.py is running.');}finally{
    const la=T[S.language]||T.English;
    btn.innerHTML=la.btn_check_loan||'🚀 Run AI Assessment';
    btn.disabled=false;
  }
}

function showLoanResult(data){
  const la=T[S.language]||T.English;
  const approved=data.prediction==='Approved';
  const msub=document.getElementById('rModelSub');
  if(msub) msub.textContent=la.model_sub||'Loan Approval Assessment · LightGBM + SHAP';
  document.getElementById('rVerdict').textContent=approved?(la.approved||'✅ Approved'):(la.rejected||'❌ Rejected');
  document.getElementById('rVerdict').style.color=approved?'var(--success)':'var(--danger)';
  document.getElementById('rBadge').className='badge '+(approved?'bs':'bd');
  document.getElementById('rBadge').textContent='⚡ '+(la.ai_decision||'AI Decision Complete');
  const conf=data.confidence||0;
  document.getElementById('rConf').textContent=conf+'%';
  document.getElementById('rScore').textContent=conf>80?(la.risk_low||'Low Risk'):conf>60?(la.risk_medium||'Medium'):(la.risk_high||'High');
  document.getElementById('rRisk').textContent=approved?(la.risk_low||'Low'):(la.risk_high||'High');
  document.getElementById('rRisk').style.color=approved?'var(--success)':'var(--danger)';
  setTimeout(()=>document.getElementById('rBar').style.width=conf+'%',200);
  const alertEl=document.getElementById('rAlert');
  if(approved){
    alertEl.style.cssText='background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.2);border-radius:10px;padding:12px 16px;display:flex;align-items:center;gap:9px;margin-bottom:22px';
    alertEl.innerHTML='<span style="font-size:18px">✅</span><span style="font-size:12px;color:#34D399">'+(la.why_approved||'Great news! Your application meets the approval criteria.')+'</span>';
  }else{
    alertEl.style.cssText='background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:10px;padding:12px 16px;display:flex;align-items:center;gap:9px;margin-bottom:22px';
    alertEl.innerHTML='<span style="font-size:18px">⚠️</span><span style="font-size:12px;color:#F87171">'+(la.why_rejected||'Your application did not meet the minimum criteria.')+'</span>';
  }
}

function showExplanation(data){
  const shap=data.shap||{};
  const expl=data.explanation||{};
  const la=T[S.language]||T.English;
  // Translate the profile mode label
  const emodeMap={Elder:la.emode_elder||'Elder Mode',Student:la.emode_student||'Student Mode',Professional:la.emode_professional||'Professional Mode'};
  document.getElementById('emode').textContent='👤 '+(emodeMap[S.profile]||S.profile+' Mode');
  const pts=expl.explanation_points||[];
  document.getElementById('etxt').textContent=pts.join(' ');
  document.getElementById('analogyTxt').textContent=expl.analogy||'—';
  const sorted=Object.entries(shap).sort((a,b)=>Math.abs(b[1])-Math.abs(a[1])).slice(0,5);
  const factorsEl=document.getElementById('shapFactors');
  factorsEl.innerHTML=sorted.map(([k,v],i)=>`
    <div class="frow">
      <div class="fnum">${i+1}</div>
      <div style="flex:1">
        <div class="fname">${k.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase())}</div>
        <div class="fsub">SHAP: ${v>0?'+':''}${v.toFixed(3)}</div>
      </div>
      <span class="badge ${v>0?'bs':'bd'}">${v>0?(la.positive||'Positive'):(la.negative||'Negative')}</span>
    </div>`).join('');
  const max=Math.max(...Object.values(shap).map(Math.abs));
  const barsEl=document.getElementById('shapBars');
  barsEl.innerHTML=sorted.map(([k,v])=>`
    <div class="mrow">
      <div class="mname" style="font-size:11px">${k.replace(/_/g,' ')}</div>
      <div class="mtrack"><div class="mfill" style="width:${Math.abs(v)/max*100}%;background:${v>0?'linear-gradient(90deg,var(--success),#34D399)':'linear-gradient(90deg,var(--danger),#F87171)'}"></div></div>
      <div class="mval" style="color:${v>0?'var(--success)':'var(--danger)'};">${(Math.abs(v)/max*100).toFixed(0)}%</div>
    </div>`).join('');
  const ts=expl.transparency_score||82;
  const trScoreEl=document.getElementById('trScore');
  if(trScoreEl) trScoreEl.textContent=ts;
  const trCircleEl=document.getElementById('trCircle');
  if(trCircleEl){ const dashoffset=301-(301*(ts/100)); trCircleEl.setAttribute('stroke-dashoffset',dashoffset); }

  // ── Rejection reasons + next steps panel ──
  const panel=document.getElementById('rejectionPanel');
  const approved=(data.prediction==='Approved');
  if(panel){
    if(!approved){
      panel.style.display='block';
      // Translate panel headings
      const rTitle=document.getElementById('rejTitleEl');
      const nTitle=document.getElementById('nextStepsTitleEl');
      const reapplyLbl=document.getElementById('reapplyLabelEl');
      const improveLbl=document.getElementById('improveTipLabelEl');
      if(rTitle) rTitle.textContent=la.rejection_reasons_title||'❌ Why Was It Rejected?';
      if(nTitle) nTitle.textContent=la.next_steps_title||'✅ What To Do Next';
      if(reapplyLbl) reapplyLbl.textContent=la.reapply_label||'📅 When To Reapply';
      if(improveLbl) improveLbl.textContent=la.improvement_tip_label||'💡 Top Improvement Tip';
      // Rejection reasons list
      const reasons=data.rejection_reasons||expl.rejection_reasons||[];
      const rList=document.getElementById('rejReasonsList');
      if(rList) rList.innerHTML=reasons.length
        ? reasons.map(r=>`<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px"><span style="color:#F87171;font-size:14px;flex-shrink:0">✗</span><span style="font-size:12px;color:var(--text2);line-height:1.6">${r}</span></div>`).join('')
        : `<p style="font-size:12px;color:var(--text3)">${la.no_rejection_data||'No specific rejection reasons available.'}</p>`;
      // Next steps list
      const steps=data.next_steps||expl.next_steps||[];
      const sList=document.getElementById('nextStepsList');
      if(sList) sList.innerHTML=steps.length
        ? steps.map((s,i)=>`<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px"><span style="background:linear-gradient(135deg,var(--success),#34D399);color:#fff;border-radius:50%;width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0">${i+1}</span><span style="font-size:12px;color:var(--text2);line-height:1.6">${s}</span></div>`).join('')
        : '';
      // Reapply timeline
      const reapplyTxt=document.getElementById('reapplyTxt');
      const reapplyCard=document.getElementById('reapplyCard');
      const rt=data.reapply_timeline||expl.reapply_timeline||'';
      if(reapplyCard) reapplyCard.style.display=rt?'block':'none';
      if(reapplyTxt) reapplyTxt.textContent=rt;
      // Improvement tip
      const improveTxt=document.getElementById('improveTipTxt');
      const it=data.improvement_tip||expl.improvement_tip||'';
      if(improveTxt) improveTxt.textContent=it;
    } else {
      panel.style.display='none';
    }
  }
}

async function simplifyExpl(){
  const curr=document.getElementById('etxt').textContent;
  document.getElementById('etxt').textContent='Simplifying…';
  try{
    const r=await fetch(API+'/api/simplify',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({previous_answer:curr,profile:S.profile,language:S.language})
    });
    const d=await r.json();
    if(d.success){
      document.getElementById('etxt').textContent=(d.data.explanation_points||[]).join(' ');
      document.getElementById('analogyTxt').textContent=d.data.analogy||'—';
      document.getElementById('emode').textContent='🧓 Simplified';
    }
  }catch{document.getElementById('etxt').textContent=curr;}
}

function updateSim(){
  const income=+(document.getElementById('is')?.value||500000);
  const credit=+(document.getElementById('cs')?.value||700);
  const loan=+(document.getElementById('ls')?.value||1000000);
  const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
  set('iv','₹'+income.toLocaleString('en-IN'));
  set('cv',credit);
  set('lv','₹'+loan.toLocaleString('en-IN'));
  let prob=0;
  prob+=Math.max(0,(income-100000)/(2000000-100000))*35;
  prob+=Math.max(0,(credit-300)/(900-300))*50;
  prob+=Math.max(0,(1-(loan-100000)/(10000000-100000)))*15;
  prob=Math.min(97,Math.round(prob));
  set('pd',prob+'%');
  const la=T[S.language]||T.English;
  const pl=document.getElementById('pl');
  if(pl){
    if(prob>=60){pl.style.color='var(--success)';pl.textContent='✅ '+(la.likely_approved||'Likely Approved');}
    else if(prob>=40){pl.style.color='var(--warning)';pl.textContent='⚠️ '+(la.borderline||'Borderline');}
    else{pl.style.color='var(--danger)';pl.textContent='❌ '+(la.likely_rejected||'Likely Rejected');}
  }
  const tip=document.getElementById('simtip');
  if(tip){
    if(credit<750) tip.textContent='💡 '+(la.tip_cibil||'Raise CIBIL score above 750 for the biggest boost.');
    else if(income<600000) tip.textContent='💡 '+(la.tip_income||'Income above ₹6L significantly improves chances.');
    else if(loan>5000000) tip.textContent='💡 '+(la.tip_loan||'Lower the loan amount to improve approval odds.');
    else tip.textContent='🎉 '+(la.tip_good||"Good profile! You'd likely be approved with these values.");
  }
}

async function submitChurn(){
  const tenure=+document.getElementById('cTenure').value;
  const balance=+document.getElementById('cBalance').value;
  const products=+document.getElementById('cProducts').value||1;
  const satisfaction=+document.getElementById('cSatis').value||3;
  const complaints=+document.getElementById('cComplaints').value||0;
  const credit=+document.getElementById('cCredit').value||650;
  const age=+document.getElementById('cAge').value||35;
  const active=document.getElementById('cActive').value==='true';
  if(!tenure&&!balance){alert('Please fill in Tenure and Balance!');return;}
  const btn=document.getElementById('churnBtn');
  btn.innerHTML='<div class="spinner"></div> Predicting…';
  btn.disabled=true;
  try{
    const r=await fetch(API+'/api/churn/predict',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({tenure,balance,products,is_active:active,complaints,credit_score:credit,age,salary:50000,satisfaction,points:400,profile:S.profile,language:S.language})
    });
    const data=await r.json();
    window._lastChurnData=data;
    showChurnResult(data);
  }catch(e){alert('Error connecting to backend!');}finally{
    const la=T[S.language]||T.English;
    btn.innerHTML=la.btn_check_churn||'📉 Predict Churn Risk';
    btn.disabled=false;
  }
}

function showChurnResult(data){
  const la=T[S.language]||T.English;
  const el=document.getElementById('churnResult');
  el.style.display='block';
  const risk=data.risk_score||0;
  const churn=data.will_churn;
  document.getElementById('churnVerdict').textContent=churn?(la.will_leave||'⚠️ High Churn Risk'):(la.will_stay||'✅ Customer Will Stay');
  document.getElementById('churnVerdict').style.color=churn?'var(--danger)':'var(--success)';
  document.getElementById('churnScore').textContent=risk+'%';
  setTimeout(()=>document.getElementById('churnBar').style.width=risk+'%',200);
  const pts=data.explanation?.explanation_points||[];
  document.getElementById('churnExpPoints').innerHTML=pts.map(p=>`
    <div class="frow"><div class="fnum">→</div><div style="flex:1"><div class="fsub">${p}</div></div></div>`).join('');
  document.getElementById('churnAnalogy').textContent=data.explanation?.analogy||'—';
  el.scrollIntoView({behavior:'smooth'});
}

// ── CHAT ──
const chatHistory=[];
async function sendChat(){
  const inp=document.getElementById('chatInp');
  const q=inp.value.trim();
  if(!q)return;
  appendMsg('chatMsgs',q,'user');
  chatHistory.push({role:'user',content:q});
  inp.value='';
  const btn=document.getElementById('chatSendBtn');
  btn.disabled=true;
  const t=appendTyping('chatMsgs');
  try{
    const topic=document.getElementById('chatTopic')?.value||'Loans & EMI';
    const lang=document.getElementById('chatLang')?.value||S.language;
    const r=await fetch(API+'/api/ask',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({question:q,profile:S.profile,language:lang,topic,history:chatHistory.slice(-6)})
    });
    const data=await r.json();
    t.remove();
    if(data.success){
      const ans=data.data.answer||'Sorry, I could not answer that.';
      const bubble=appendMsg('chatMsgs',ans,'ai');
      if(bubble) addSpeakBtn(bubble, ans);
      chatHistory.push({role:'assistant',content:ans});
      // ── Voice Mode: auto-speak AI response + restart mic ──
      if(S.voiceMode){
        const micBtn=document.getElementById('micBtn');
        if(micBtn){ micBtn.className='voice-btn speaking'; micBtn.innerHTML='🔊'; }
        speakBubble(ans);
        const waitAndRestart=()=>{
          if(window.speechSynthesis && window.speechSynthesis.speaking){
            setTimeout(waitAndRestart,300);
          } else {
            const btn2=document.getElementById('micBtn');
            if(btn2){ btn2.className='voice-btn'; btn2.innerHTML='🎤'; }
            if(S.voiceMode) startRecording();
          }
        };
        setTimeout(waitAndRestart,600);
      }
      const fqs=data.data.follow_up_questions||[];
      if(fqs.length){
        const chips=document.createElement('div');
        chips.className='qchips';
        chips.style.marginTop='4px';
        fqs.forEach(fq=>{
          const c=document.createElement('div');
          c.className='qchip';
          c.textContent=fq;
          c.onclick=()=>{document.getElementById('chatInp').value=fq;sendChat();};
          chips.appendChild(c);
        });
        document.getElementById('chatMsgs').appendChild(chips);
      }
    } else {
      appendMsg('chatMsgs','Sorry, something went wrong. Please try again.','ai');
    }
  }catch(e){
    t.remove();
    appendMsg('chatMsgs','Cannot reach backend. Make sure python main.py is running.','ai');
  }
  btn.disabled=false;
}

function qAsk(q){document.getElementById('chatInp').value=q;sendChat();}

function appendMsg(cid,txt,role){
  const c=document.getElementById(cid);if(!c)return;
  const b=document.createElement('div');
  b.className='bubble '+role;
  if(role==='ai') b.innerHTML=`<div class="aitag">✨ CLARIVOX AI</div>${txt}`;
  else b.textContent=txt;
  c.appendChild(b);c.scrollTop=c.scrollHeight;return b;
}
function appendTyping(cid){
  const c=document.getElementById(cid);if(!c)return document.createElement('div');
  const b=document.createElement('div');
  b.className='bubble ai';
  b.innerHTML='<div class="aitag">✨ CLARIVOX AI</div><div class="typing"><div class="tdot"></div><div class="tdot"></div><div class="tdot"></div></div>';
  c.appendChild(b);c.scrollTop=c.scrollHeight;return b;
}

// FLOATING CHAT
let cpOpen=false;
function toggleCP(){
  cpOpen=!cpOpen;
  document.getElementById('cpanel').classList.toggle('open',cpOpen);
  if(cpOpen){const b=document.querySelector('#floatChat .fcbadge');if(b)b.style.display='none';}
}
async function cpSend(){
  const inp=document.getElementById('cpinp');
  if(!inp||!inp.value.trim())return;
  const q=inp.value.trim();
  cpAppend(q,'user');
  inp.value='';
  const t=cpTyping();
  try{
    const r=await fetch(API+'/api/ask',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({question:q,profile:S.profile,language:S.language,topic:'Loans & EMI',history:[]})
    });
    const data=await r.json();
    t.remove();
    const ans=data.success?data.data.answer:'Sorry, try again.';
    cpAppend(ans,'ai');
    if(S.language!=='English') speak(ans, S.language);
  }catch{t.remove();cpAppend('Backend offline. Run python main.py first.','ai');}
}
function cpAppend(txt,role){
  const c=document.getElementById('cpmsgs');if(!c)return;
  const b=document.createElement('div');
  b.className='bubble '+role;b.style.maxWidth='92%';
  if(role==='ai')b.innerHTML=`<div class="aitag">CLARIVOX AI</div>${txt}`;else b.textContent=txt;
  c.appendChild(b);c.scrollTop=c.scrollHeight;return b;
}
function cpTyping(){
  const c=document.getElementById('cpmsgs');
  const b=document.createElement('div');b.className='bubble ai';b.style.maxWidth='92%';
  b.innerHTML='<div class="aitag">CLARIVOX AI</div><div class="typing"><div class="tdot"></div><div class="tdot"></div><div class="tdot"></div></div>';
  c.appendChild(b);c.scrollTop=c.scrollHeight;return b;
}

// PROFILE POPUP
let ppOpen=false;
function togglePP(){ppOpen=!ppOpen;document.getElementById('ppopup').classList.toggle('open',ppOpen);}
document.addEventListener('click',e=>{
  if(!e.target.closest('.profile-pill')&&!e.target.closest('#ppopup')&&ppOpen){
    ppOpen=false;document.getElementById('ppopup').classList.remove('open');
  }
});

// FEEDBACK
let sr=0;
function rateStar(n){sr=n;document.querySelectorAll('.star').forEach((s,i)=>s.classList.toggle('on',i<n));}
async function submitFB(){
  const comment=document.getElementById('fbComment').value;
  try{
    await fetch(API+'/api/feedback',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({question:'UI Feedback',answer:'N/A',rating:sr,profile:S.profile,language:S.language,comment})
    });
  }catch(e){}
  document.getElementById('fbForm').style.display='none';
  const ok=document.getElementById('fbOk');
  ok.style.display='block';
  document.getElementById('fbPct').textContent=Math.round((sr/5)*100)+'%';
}

// RESPONSIVE
function resp(){
  const m=window.innerWidth<768;
  ['explGrid','wiGrid','trGrid'].forEach(id=>{const e=document.getElementById(id);if(e)e.style.gridTemplateColumns=m?'1fr':'1fr 1fr';});
  const fg=document.getElementById('featGrid');
  if(fg)fg.style.gridTemplateColumns=m?'1fr':window.innerWidth<1024?'1fr 1fr':'1fr 1fr 1fr';
}
window.addEventListener('resize',resp);
resp();
