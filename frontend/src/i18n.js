import React, { createContext, useContext, useMemo, useState } from 'react';

export const languageOptions = [
  { value: 'english', label: 'English' },
  { value: 'hindi', label: 'हिंदी' },
  { value: 'tamil', label: 'தமிழ்' },
  { value: 'telugu', label: 'తెలుగు' },
  { value: 'bengali', label: 'বাংলা' },
  { value: 'marathi', label: 'मराठी' },
  { value: 'punjabi', label: 'ਪੰਜਾਬੀ' },
];

const translations = {
  english: {
    appName: 'Mental Health Monitoring System', home: 'Home', dashboard: 'Dashboard', alerts: 'Alerts', help: 'Help',
    victims: 'Victims', interventions: 'Interventions', analytics: 'Analytics', logout: 'Logout', language: 'Language',
    dashboardTitle: 'Mental Health Monitoring Dashboard', totalVictims: 'Total Victims', highRiskCases: 'High Risk Cases',
    activeAlerts: 'Active Alerts', interventionsToday: 'Interventions Today', recentAlerts: 'Recent Alerts', distressTrend: 'Distress Trend',
    loadingAlerts: 'Loading alerts...', noAlerts: 'No alerts currently reported.', dashboardError: 'Unable to load dashboard data right now.',
    login: 'Log in', createAccount: 'Create account', welcomeBack: 'Welcome back', accessWorkspace: 'Access your monitoring workspace',
    fullName: 'Full name', workEmail: 'Work email', role: 'Role', password: 'Password', yourName: 'Your name',
    counselor: 'Counselor', caseOfficer: 'Case officer', specialist: 'Mental health specialist', pleaseWait: 'Please wait...',
    enterWorkspace: 'Enter workspace', createWorkspace: 'Create workspace', secureWorkspace: 'Secure case workspace',
    unableRequest: 'Unable to complete that request.', languageLabel: 'Page language',
  },
  hindi: {
    appName: 'मानसिक स्वास्थ्य निगरानी प्रणाली', home: 'होम', dashboard: 'डैशबोर्ड', alerts: 'अलर्ट', help: 'सहायता', victims: 'लाभार्थी', interventions: 'हस्तक्षेप', analytics: 'विश्लेषण', logout: 'लॉग आउट', language: 'भाषा',
    dashboardTitle: 'मानसिक स्वास्थ्य निगरानी डैशबोर्ड', totalVictims: 'कुल लाभार्थी', highRiskCases: 'उच्च जोखिम मामले', activeAlerts: 'सक्रिय अलर्ट', interventionsToday: 'आज के हस्तक्षेप', recentAlerts: 'हाल के अलर्ट', distressTrend: 'तनाव का रुझान', loadingAlerts: 'अलर्ट लोड हो रहे हैं...', noAlerts: 'अभी कोई अलर्ट नहीं है।', dashboardError: 'डैशबोर्ड डेटा अभी लोड नहीं हो सका।',
    login: 'लॉग इन', createAccount: 'खाता बनाएं', welcomeBack: 'वापसी पर स्वागत है', accessWorkspace: 'अपने निगरानी कार्यक्षेत्र में जाएं', fullName: 'पूरा नाम', workEmail: 'कार्य ईमेल', role: 'भूमिका', password: 'पासवर्ड', yourName: 'आपका नाम', counselor: 'काउंसलर', caseOfficer: 'केस अधिकारी', specialist: 'मानसिक स्वास्थ्य विशेषज्ञ', pleaseWait: 'कृपया प्रतीक्षा करें...', enterWorkspace: 'कार्य क्षेत्र में जाएं', createWorkspace: 'कार्य क्षेत्र बनाएं', secureWorkspace: 'सुरक्षित केस कार्यक्षेत्र', unableRequest: 'अनुरोध पूरा नहीं हो सका।', languageLabel: 'पृष्ठ की भाषा',
  },
  tamil: { appName: 'மனநல கண்காணிப்பு அமைப்பு', home: 'முகப்பு', dashboard: 'டாஷ்போர்டு', alerts: 'எச்சரிக்கைகள்', help: 'உதவி', victims: 'பயனாளிகள்', interventions: 'தலையீடுகள்', analytics: 'பகுப்பாய்வு', logout: 'வெளியேறு', language: 'மொழி', dashboardTitle: 'மனநல கண்காணிப்பு டாஷ்போர்டு', totalVictims: 'மொத்த பயனாளிகள்', highRiskCases: 'அதிக ஆபத்து வழக்குகள்', activeAlerts: 'செயலில் உள்ள எச்சரிக்கைகள்', interventionsToday: 'இன்றைய தலையீடுகள்', recentAlerts: 'சமீபத்திய எச்சரிக்கைகள்', distressTrend: 'மன அழுத்த போக்கு', loadingAlerts: 'எச்சரிக்கைகள் ஏற்றப்படுகின்றன...', noAlerts: 'தற்போது எச்சரிக்கைகள் இல்லை.', dashboardError: 'டாஷ்போர்டு தரவை ஏற்ற முடியவில்லை.', login: 'உள்நுழை', createAccount: 'கணக்கை உருவாக்கு', welcomeBack: 'மீண்டும் வருக', accessWorkspace: 'கண்காணிப்பு பணியிடத்தை அணுகவும்', fullName: 'முழுப் பெயர்', workEmail: 'பணி மின்னஞ்சல்', role: 'பங்கு', password: 'கடவுச்சொல்', yourName: 'உங்கள் பெயர்', counselor: 'ஆலோசகர்', caseOfficer: 'வழக்கு அதிகாரி', specialist: 'மனநல நிபுணர்', pleaseWait: 'காத்திருக்கவும்...', enterWorkspace: 'பணியிடத்திற்குச் செல்லவும்', createWorkspace: 'பணியிடத்தை உருவாக்கு', secureWorkspace: 'பாதுகாப்பான வழக்கு பணியிடம்', unableRequest: 'கோரிக்கையை முடிக்க முடியவில்லை.', languageLabel: 'பக்க மொழி' },
  telugu: { appName: 'మానసిక ఆరోగ్య పర్యవేక్షణ వ్యవస్థ', home: 'హోమ్', dashboard: 'డ్యాష్‌బోర్డ్', alerts: 'హెచ్చరికలు', help: 'సహాయం', victims: 'లబ్ధిదారులు', interventions: 'చర్యలు', analytics: 'విశ్లేషణ', logout: 'లాగ్ అవుట్', language: 'భాష', dashboardTitle: 'మానసిక ఆరోగ్య పర్యవేక్షణ డ్యాష్‌బోర్డ్', totalVictims: 'మొత్తం లబ్ధిదారులు', highRiskCases: 'అధిక ప్రమాద కేసులు', activeAlerts: 'క్రియాశీల హెచ్చరికలు', interventionsToday: 'నేటి చర్యలు', recentAlerts: 'ఇటీవలి హెచ్చరికలు', distressTrend: 'ఒత్తిడి ధోరణి', loadingAlerts: 'హెచ్చరికలు లోడ్ అవుతున్నాయి...', noAlerts: 'ప్రస్తుతం హెచ్చరికలు లేవు.', dashboardError: 'డ్యాష్‌బోర్డ్ డేటాను లోడ్ చేయలేకపోయాం.', login: 'లాగిన్', createAccount: 'ఖాతా సృష్టించండి', welcomeBack: 'మళ్లీ స్వాగతం', accessWorkspace: 'పర్యవేక్షణ కార్యస్థలాన్ని తెరవండి', fullName: 'పూర్తి పేరు', workEmail: 'పని ఇమెయిల్', role: 'పాత్ర', password: 'పాస్‌వర్డ్', yourName: 'మీ పేరు', counselor: 'కౌన్సిలర్', caseOfficer: 'కేసు అధికారి', specialist: 'మానసిక ఆరోగ్య నిపుణుడు', pleaseWait: 'దయచేసి వేచి ఉండండి...', enterWorkspace: 'కార్యస్థలంలోకి వెళ్లండి', createWorkspace: 'కార్యస్థలాన్ని సృష్టించండి', secureWorkspace: 'సురక్షిత కేసు కార్యస్థలం', unableRequest: 'అభ్యర్థనను పూర్తి చేయలేకపోయాం.', languageLabel: 'పేజీ భాష' },
  bengali: { appName: 'মানসিক স্বাস্থ্য পর্যবেক্ষণ ব্যবস্থা', home: 'হোম', dashboard: 'ড্যাশবোর্ড', alerts: 'সতর্কতা', help: 'সহায়তা', victims: 'উপকারভোগী', interventions: 'হস্তক্ষেপ', analytics: 'বিশ্লেষণ', logout: 'লগ আউট', language: 'ভাষা', dashboardTitle: 'মানসিক স্বাস্থ্য পর্যবেক্ষণ ড্যাশবোর্ড', totalVictims: 'মোট উপকারভোগী', highRiskCases: 'উচ্চ ঝুঁকির মামলা', activeAlerts: 'সক্রিয় সতর্কতা', interventionsToday: 'আজকের হস্তক্ষেপ', recentAlerts: 'সাম্প্রতিক সতর্কতা', distressTrend: 'মানসিক চাপের প্রবণতা', loadingAlerts: 'সতর্কতা লোড হচ্ছে...', noAlerts: 'বর্তমানে কোনো সতর্কতা নেই।', dashboardError: 'ড্যাশবোর্ড ডেটা লোড করা যায়নি।', login: 'লগ ইন', createAccount: 'অ্যাকাউন্ট তৈরি করুন', welcomeBack: 'আবার স্বাগতম', accessWorkspace: 'আপনার পর্যবেক্ষণ কর্মক্ষেত্রে প্রবেশ করুন', fullName: 'পুরো নাম', workEmail: 'কাজের ইমেল', role: 'ভূমিকা', password: 'পাসওয়ার্ড', yourName: 'আপনার নাম', counselor: 'কাউন্সেলর', caseOfficer: 'কেস অফিসার', specialist: 'মানসিক স্বাস্থ্য বিশেষজ্ঞ', pleaseWait: 'অনুগ্রহ করে অপেক্ষা করুন...', enterWorkspace: 'কর্মক্ষেত্রে প্রবেশ করুন', createWorkspace: 'কর্মক্ষেত্র তৈরি করুন', secureWorkspace: 'নিরাপদ কেস কর্মক্ষেত্র', unableRequest: 'অনুরোধটি সম্পন্ন করা যায়নি।', languageLabel: 'পৃষ্ঠার ভাষা' },
  marathi: { appName: 'मानसिक आरोग्य निरीक्षण प्रणाली', home: 'मुख्यपृष्ठ', dashboard: 'डॅशबोर्ड', alerts: 'सूचना', help: 'मदत', victims: 'लाभार्थी', interventions: 'हस्तक्षेप', analytics: 'विश्लेषण', logout: 'लॉग आउट', language: 'भाषा', dashboardTitle: 'मानसिक आरोग्य निरीक्षण डॅशबोर्ड', totalVictims: 'एकूण लाभार्थी', highRiskCases: 'उच्च जोखीम प्रकरणे', activeAlerts: 'सक्रिय सूचना', interventionsToday: 'आजचे हस्तक्षेप', recentAlerts: 'अलीकडील सूचना', distressTrend: 'तणावाचा कल', loadingAlerts: 'सूचना लोड होत आहेत...', noAlerts: 'सध्या कोणत्याही सूचना नाहीत.', dashboardError: 'डॅशबोर्ड डेटा लोड करता आला नाही.', login: 'लॉग इन', createAccount: 'खाते तयार करा', welcomeBack: 'पुन्हा स्वागत आहे', accessWorkspace: 'तुमच्या निरीक्षण कार्यक्षेत्रात प्रवेश करा', fullName: 'पूर्ण नाव', workEmail: 'कामाचा ईमेल', role: 'भूमिका', password: 'पासवर्ड', yourName: 'तुमचे नाव', counselor: 'समुपदेशक', caseOfficer: 'केस अधिकारी', specialist: 'मानसिक आरोग्य तज्ज्ञ', pleaseWait: 'कृपया प्रतीक्षा करा...', enterWorkspace: 'कार्य क्षेत्रात प्रवेश करा', createWorkspace: 'कार्य क्षेत्र तयार करा', secureWorkspace: 'सुरक्षित केस कार्यक्षेत्र', unableRequest: 'विनंती पूर्ण करता आली नाही.', languageLabel: 'पृष्ठाची भाषा' },
  punjabi: { appName: 'ਮਾਨਸਿਕ ਸਿਹਤ ਨਿਗਰਾਨੀ ਪ੍ਰਣਾਲੀ', home: 'ਹੋਮ', dashboard: 'ਡੈਸ਼ਬੋਰਡ', alerts: 'ਚੇਤਾਵਨੀਆਂ', help: 'ਮਦਦ', victims: 'ਲਾਭਪਾਤਰੀ', interventions: 'ਦਖਲ', analytics: 'ਵਿਸ਼ਲੇਸ਼ਣ', logout: 'ਲੌਗ ਆਊਟ', language: 'ਭਾਸ਼ਾ', dashboardTitle: 'ਮਾਨਸਿਕ ਸਿਹਤ ਨਿਗਰਾਨੀ ਡੈਸ਼ਬੋਰਡ', totalVictims: 'ਕੁੱਲ ਲਾਭਪਾਤਰੀ', highRiskCases: 'ਉੱਚ ਜੋਖਮ ਮਾਮਲੇ', activeAlerts: 'ਸਰਗਰਮ ਚੇਤਾਵਨੀਆਂ', interventionsToday: 'ਅੱਜ ਦੇ ਦਖਲ', recentAlerts: 'ਹਾਲੀਆ ਚੇਤਾਵਨੀਆਂ', distressTrend: 'ਤਣਾਅ ਦਾ ਰੁਝਾਨ', loadingAlerts: 'ਚੇਤਾਵਨੀਆਂ ਲੋਡ ਹੋ ਰਹੀਆਂ ਹਨ...', noAlerts: 'ਇਸ ਵੇਲੇ ਕੋਈ ਚੇਤਾਵਨੀ ਨਹੀਂ।', dashboardError: 'ਡੈਸ਼ਬੋਰਡ ਡੇਟਾ ਲੋਡ ਨਹੀਂ ਹੋ ਸਕਿਆ।', login: 'ਲੌਗ ਇਨ', createAccount: 'ਖਾਤਾ ਬਣਾਓ', welcomeBack: 'ਜੀ ਆਇਆਂ ਨੂੰ', accessWorkspace: 'ਆਪਣੇ ਨਿਗਰਾਨੀ ਕਾਰਜਸਥਾਨ ਵਿੱਚ ਜਾਓ', fullName: 'ਪੂਰਾ ਨਾਮ', workEmail: 'ਕੰਮ ਦੀ ਈਮੇਲ', role: 'ਭੂਮਿਕਾ', password: 'ਪਾਸਵਰਡ', yourName: 'ਤੁਹਾਡਾ ਨਾਮ', counselor: 'ਕਾਊਂਸਲਰ', caseOfficer: 'ਕੇਸ ਅਧਿਕਾਰੀ', specialist: 'ਮਾਨਸਿਕ ਸਿਹਤ ਮਾਹਿਰ', pleaseWait: 'ਕਿਰਪਾ ਕਰਕੇ ਉਡੀਕ ਕਰੋ...', enterWorkspace: 'ਕਾਰਜਸਥਾਨ ਵਿੱਚ ਜਾਓ', createWorkspace: 'ਕਾਰਜਸਥਾਨ ਬਣਾਓ', secureWorkspace: 'ਸੁਰੱਖਿਅਤ ਕੇਸ ਕਾਰਜਸਥਾਨ', unableRequest: 'ਬੇਨਤੀ ਪੂਰੀ ਨਹੀਂ ਹੋ ਸਕੀ।', languageLabel: 'ਪੰਨੇ ਦੀ ਭਾਸ਼ਾ' },
};

const LanguageContext = createContext(null);

export const LanguageProvider = ({ children }) => {
  const [language, setLanguageState] = useState(() => localStorage.getItem('assistant-language') || 'english');
  const setLanguage = (nextLanguage) => {
    const validLanguage = translations[nextLanguage] ? nextLanguage : 'english';
    localStorage.setItem('assistant-language', validLanguage);
    setLanguageState(validLanguage);
  };
  const value = useMemo(() => ({ language, setLanguage, t: (key) => translations[language]?.[key] || translations.english[key] || key, languageOptions }), [language]);
  return React.createElement(LanguageContext.Provider, { value }, children);
};

export const useLanguage = () => useContext(LanguageContext);
