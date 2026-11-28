🌐 [Español](README.md) · [English](README.en.md) · [Português](README.pt.md) · [Français](README.fr.md) · [简体中文](README.zh-CN.md) · [हिन्दी](README.hi.md)

<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="Ícono de PageSpeed Audit">
</p>

# Google PageSpeed Insights से वेबसाइट की गति का ऑडिट

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)

PageSpeed Audit, ChatGPT, Codex और Claude के लिए एक स्किल है। यह PageSpeed रिपोर्ट के आधार पर अधिकतम तीन प्राथमिक सुझाव देती है। हर सुझाव में बताया जाता है कि बदलाव कहाँ करें, उसका असर कैसे जाँचें और ज़रूरत पड़ने पर उसे कैसे वापस लें। यह WordPress, WooCommerce, Shopify और स्टैटिक साइटों सहित सार्वजनिक HTTP(S) साइटों पर काम करती है।

## macOS और Linux पर इंस्टॉल करना

रिपॉज़िटरी क्लोन करने के लिए Git चाहिए। टर्मिनल में काम करने के लिए Codex CLI या Claude Code इंस्टॉल करें। ZIP बनाने, स्क्रिप्ट चलाने या टेस्ट चलाने के लिए Python 3 चाहिए। प्रोजेक्ट Python की मानक लाइब्रेरी इस्तेमाल करता है। टेस्ट Linux पर चलाए गए हैं। macOS पर स्थानीय वर्कफ़्लो की पुष्टि बाकी है।

- **ChatGPT:** नीचे दिए गए कमांड से ZIP बनाएँ। **Plugins → Skills → Create → Upload from your computer** में `dist/pagespeed-audit.zip` चुनें। यह विकल्प खाते और वर्कस्पेस की अनुमतियों पर निर्भर है।
- **Claude.ai:** ज़रूरत होने पर कोड चलाने और फ़ाइल बनाने की सुविधा चालू करें। **Customize → Skills → + → Create skill → Upload a skill** में वही ZIP अपलोड करके स्किल चालू करें।
- **Codex CLI:** क्लोन की गई रिपॉज़िटरी में `codex` चलाएँ और `$pagespeed-audit` इस्तेमाल करें।
- **Claude Code:** रिपॉज़िटरी में `claude` चलाएँ और `/pagespeed-audit` इस्तेमाल करें। सिम्बॉलिक लिंक उपलब्ध न हो तो `.agents/skills/pagespeed-audit/` को `.claude/skills/pagespeed-audit/` में कॉपी करें।

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

## उपयोग और कार्यप्रवाह

> pagespeed-audit से https://example.com/ का मोबाइल और डेस्कटॉप पर ऑडिट करें। तीन प्राथमिक बदलाव, उन्हें करने की जगह और उनकी जाँच का तरीका बताएँ।

आप सार्वजनिक URL, PSI रिपोर्ट का लिंक, स्क्रीनशॉट या निर्यात किया गया JSON दे सकते हैं। किसी डिप्लॉयमेंट की तुलना के लिए उसी URL और डिवाइस की पहले और बाद की रिपोर्ट दें। अगर चैट Google तक नहीं पहुँच पाती, तो ब्राउज़र में PSI चलाकर परिणाम साझा करें।

स्किल CrUX के वास्तविक उपयोगकर्ता डेटा और Lighthouse की लैब माप को अलग रखती है। यह जाँचे गए URL और डिवाइस को दर्ज करती है और बताती है कि कौन-सा डेटा नहीं मिला या कौन-सी माप अवरुद्ध हुई। Codex और Claude Code में चार विशेषज्ञ एजेंट फ़ील्ड डेटा, लैब विश्लेषण, बदलाव के सुझाव और रिपोर्ट की समीक्षा सँभाल सकते हैं। यही काम क्रम से भी किया जा सकता है। साइट में बदलाव करने के लिए अलग से अनुरोध करें।

## कमांड लाइन और लाइसेंस

नीचे दिए गए कमांड रिपॉज़िटरी की मूल डायरेक्टरी से चलाएँ। नई माप के लिए PSI API तक पहुँच चाहिए। API कुंजी की ज़रूरत हो तो `PAGESPEED_API_KEY` एनवायरनमेंट वैरिएबल सेट करें। सार्वजनिक URL इस्तेमाल करें और उनमें पासवर्ड या निजी डेटा शामिल न करें। प्रोजेक्ट [MIT लाइसेंस](LICENSE) के तहत उपलब्ध है।

```bash
python3 .agents/skills/pagespeed-audit/scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 .agents/skills/pagespeed-audit/scripts/psi.py summarize psi-reports/*.json
python3 .agents/skills/pagespeed-audit/scripts/psi.py compare before.json after.json
python3 -m unittest discover -s tests -v
```

[Lulu (@lulubumps)](https://github.com/lulubumps) · [PageSpeed Insights documentation](https://developers.google.com/speed/docs/insights/v5/about)
