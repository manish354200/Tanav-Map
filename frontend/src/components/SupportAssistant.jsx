import React, { useEffect, useMemo, useRef, useState } from 'react';
import { assistantAPI } from '../services/api';
import { useLanguage } from '../i18n';

const languageOptions = [
  { value: 'english', label: 'English', title: 'Support Assistant', stress: 'Stress Level', labels: { critical: 'Critical', high: 'High', medium: 'Medium', low: 'Low' }, greeting: 'Hey, I’m here for you. You can share anything, even the little things, and I’ll listen without judging.', placeholder: 'Share how you feel...', send: 'Send', thinking: 'Thinking...' },
  { value: 'hindi', label: 'हिंदी', title: 'सहायता सहायक', stress: 'तनाव का स्तर', labels: { critical: 'गंभीर', high: 'उच्च', medium: 'मध्यम', low: 'कम' }, greeting: 'Namaste, main aapke liye yahan hoon. Aap bina kisi jhijhak ke apni baat share kar sakte hain.', placeholder: 'Aap kaisa mehsoos kar rahe hain?', send: 'भेजें', thinking: 'सोच रहा हूँ...' },
  { value: 'tamil', label: 'தமிழ்', title: 'ஆதரவு உதவியாளர்', stress: 'மன அழுத்த நிலை', labels: { critical: 'மிகவும் தீவிரம்', high: 'அதிகம்', medium: 'நடுத்தரம்', low: 'குறைவு' }, greeting: 'வணக்கம், உங்களுக்காக நான் இங்கே இருக்கிறேன். தயக்கமின்றி உங்கள் உணர்வுகளைப் பகிரலாம்.', placeholder: 'நீங்கள் எப்படி உணர்கிறீர்கள்?', send: 'அனுப்பு', thinking: 'சிந்திக்கிறேன்...' },
  { value: 'telugu', label: 'తెలుగు', title: 'మద్దతు సహాయకుడు', stress: 'ఒత్తిడి స్థాయి', labels: { critical: 'తీవ్రమైన', high: 'ఎక్కువ', medium: 'మధ్యస్థ', low: 'తక్కువ' }, greeting: 'నమస్తే, మీ కోసం నేను ఇక్కడ ఉన్నాను. ఎలాంటి సంకోచం లేకుండా మీ భావాలను పంచుకోవచ్చు.', placeholder: 'మీకు ఎలా అనిపిస్తోంది?', send: 'పంపండి', thinking: 'ఆలోచిస్తున్నాను...' },
  { value: 'bengali', label: 'বাংলা', title: 'সহায়তা সহকারী', stress: 'মানসিক চাপের মাত্রা', labels: { critical: 'গুরুতর', high: 'উচ্চ', medium: 'মাঝারি', low: 'কম' }, greeting: 'নমস্কার, আমি আপনার পাশে আছি। নির্দ্বিধায় আপনার অনুভূতিগুলো শেয়ার করতে পারেন।', placeholder: 'আপনার কেমন লাগছে?', send: 'পাঠান', thinking: 'ভাবছি...' },
  { value: 'marathi', label: 'मराठी', title: 'सहाय्यक', stress: 'तणावाची पातळी', labels: { critical: 'गंभीर', high: 'उच्च', medium: 'मध्यम', low: 'कमी' }, greeting: 'नमस्कार, मी तुमच्यासाठी इथे आहे. तुम्ही निःसंकोचपणे तुमच्या भावना सांगू शकता.', placeholder: 'तुम्हाला कसे वाटत आहे?', send: 'पाठवा', thinking: 'विचार करत आहे...' },
  { value: 'punjabi', label: 'ਪੰਜਾਬੀ', title: 'ਸਹਾਇਤਾ ਸਹਾਇਕ', stress: 'ਤਣਾਅ ਦਾ ਪੱਧਰ', labels: { critical: 'ਗੰਭੀਰ', high: 'ਉੱਚਾ', medium: 'ਦਰਮਿਆਨਾ', low: 'ਘੱਟ' }, greeting: 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਇੱਥੇ ਹਾਂ। ਤੁਸੀਂ ਬੇਝਿਜਕ ਆਪਣੀਆਂ ਭਾਵਨਾਵਾਂ ਸਾਂਝੀਆਂ ਕਰ ਸਕਦੇ ਹੋ।', placeholder: 'ਤੁਸੀਂ ਕਿਵੇਂ ਮਹਿਸੂਸ ਕਰ ਰਹੇ ਹੋ?', send: 'ਭੇਜੋ', thinking: 'ਸੋਚ ਰਿਹਾ ਹਾਂ...' },
];

const getInitialMessages = () => {
  const savedLanguage = localStorage.getItem('assistant-language') || 'english';
  const option = languageOptions.find((item) => item.value === savedLanguage) || languageOptions[0];
  return [{ sender: 'assistant', text: option.greeting }];
};

const stressKeywords = {
  critical: [
    'suicide',
    'kill myself',
    'end my life',
    'self harm',
    'hurt myself',
    'cannot go on',
    "can't go on",
    'panic',
    'unsafe',
  ],
  high: [
    'terrified',
    'scared',
    'afraid',
    'threat',
    'threatened',
    'harassed',
    'stalking',
    'nightmare',
    'crying',
    'hopeless',
    'helpless',
    'anxious',
    'anxiety',
    'trauma',
  ],
  medium: [
    'stress',
    'stressed',
    'worried',
    'sad',
    'angry',
    'tired',
    'alone',
    'confused',
    'upset',
    'fear',
    'nervous',
    'sleep',
  ],
};

const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

const estimateStressScore = (text) => {
  const normalizedText = text.toLowerCase();
  const words = normalizedText.match(/[a-z']+/g) || [];
  const exclamations = (normalizedText.match(/!/g) || []).length;
  let score = Math.min(words.length * 1.6, 24) + Math.min(exclamations * 4, 12);

  stressKeywords.critical.forEach((keyword) => {
    if (normalizedText.includes(keyword)) score += 28;
  });
  stressKeywords.high.forEach((keyword) => {
    if (normalizedText.includes(keyword)) score += 14;
  });
  stressKeywords.medium.forEach((keyword) => {
    if (normalizedText.includes(keyword)) score += 8;
  });

  if (/\b(no one|nobody|never|always|please help|help me)\b/.test(normalizedText)) {
    score += 10;
  }

  return clamp(Math.round(score), 8, 100);
};

const getStressLevel = (score) => {
  if (score >= 76) return { label: 'Critical', className: 'critical' };
  if (score >= 56) return { label: 'High', className: 'high' };
  if (score >= 31) return { label: 'Medium', className: 'medium' };
  return { label: 'Low', className: 'low' };
};

const SupportAssistant = () => {
  const { language, setLanguage } = useLanguage();
  const [messages, setMessages] = useState(getInitialMessages);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiStressScore, setApiStressScore] = useState(null);
  const scrollRef = useRef(null);

  const stressScore = useMemo(() => {
    const recentUserText = messages
      .filter((message) => message.sender === 'user')
      .slice(-3)
      .map((message) => message.text)
      .join(' ');
    const textForAnalysis = [recentUserText, input].filter(Boolean).join(' ');

    if (input.trim()) return estimateStressScore(textForAnalysis);
    return apiStressScore ?? (textForAnalysis.trim() ? estimateStressScore(textForAnalysis) : 8);
  }, [apiStressScore, input, messages]);

  const stressLevel = getStressLevel(stressScore);
  const selectedLanguage = languageOptions.find((option) => option.value === language) || languageOptions[0];

  useEffect(() => {
    setMessages([{ sender: 'assistant', text: selectedLanguage.greeting }]);
    setApiStressScore(null);
  }, [language]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || loading) return;

    const userMessage = { sender: 'user', text };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const history = messages.slice(-8).map((message) => ({
        role: message.sender === 'assistant' ? 'assistant' : 'user',
        content: message.text,
      }));
      const response = await assistantAPI.respond(text, 1, history, language);
      const assistantReply = {
        sender: 'assistant',
        text: response?.data?.reply || 'I’m here with you. We can take this one step at a time.',
      };
      const nextStressScore = Number(response?.data?.stress_percentage);
      if (Number.isFinite(nextStressScore)) {
        setApiStressScore(nextStressScore);
      }
      setMessages((prev) => [...prev, assistantReply]);
    } catch (error) {
      console.error('Assistant failed:', error);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: 'I’m here with you. You can tell me anything, and we can take this one step at a time.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageChange = (event) => {
    const nextLanguage = event.target.value;
    setLanguage(nextLanguage);
    setMessages([{ sender: 'assistant', text: languageOptions.find((option) => option.value === nextLanguage).greeting }]);
    setApiStressScore(null);
  };

  return (
    <aside className="assistant-panel">
      <div className="assistant-header">
        <span className="assistant-icon">💬</span>
        <span>{selectedLanguage.title}</span>
        <label className="assistant-language">
          <span className="sr-only">{selectedLanguage.title}</span>
          <select value={language} onChange={handleLanguageChange} aria-label={selectedLanguage.title}>
            {languageOptions.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
          </select>
        </label>
      </div>

      <div className={`stress-meter ${stressLevel.className}`}>
        <div className="stress-meter-top">
          <span>{selectedLanguage.stress}</span>
          <strong>{selectedLanguage.labels[stressLevel.className]}</strong>
        </div>
        <div
          className="stress-meter-track"
          role="meter"
          aria-label={selectedLanguage.stress}
          aria-valuemin="0"
          aria-valuemax="100"
          aria-valuenow={stressScore}
        >
          <div className="stress-meter-fill" style={{ width: `${stressScore}%` }} />
        </div>
        <span className="stress-meter-score">{stressScore}/100</span>
      </div>

      <div className="assistant-chat" ref={scrollRef}>
        {messages.map((msg, index) => (
          <div key={`${msg.sender}-${index}`} className={`message-row ${msg.sender}`}>
            <div className="message-bubble">
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-row assistant">
            <div className="message-bubble typing">{selectedLanguage.thinking}</div>
          </div>
        )}
      </div>

      <div className="assistant-input-wrap">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={selectedLanguage.placeholder}
          rows={2}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <button onClick={handleSend} disabled={loading || !input.trim()}>
          {selectedLanguage.send}
        </button>
      </div>
    </aside>
  );
};

export default SupportAssistant;
