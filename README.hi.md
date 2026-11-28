<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="PageSpeed Audit का आइकन">
</p>
<h1 align="center">PageSpeed Audit</h1>
<p align="center"><a href="README.md">Español</a> · <a href="README.en.md">English</a> · <a href="README.pt.md">Português</a> · <a href="README.fr.md">Français</a> · <a href="README.zh-CN.md">简体中文</a> · <strong>हिन्दी</strong></p>

**PageSpeed रिपोर्ट से तीन ऐसे सुधार पाएँ जिन्हें आप अपनी साइट पर लागू कर सकते हैं।**

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)
[![Lighthouse](https://img.shields.io/badge/Lighthouse-B3371D?style=for-the-badge&logo=lighthouse&logoColor=white)](#यह-कैसे-काम-करती-है)
[![MIT](https://img.shields.io/badge/MIT-5B3CC4?style=for-the-badge)](LICENSE)

[![ChatGPT](https://img.shields.io/badge/ChatGPT-176B56?style=for-the-badge)](#chatgpt)
[![Codex](https://img.shields.io/badge/Codex-343541?style=for-the-badge)](#codex)
[![Claude](https://img.shields.io/badge/Claude-984425?style=for-the-badge&logo=claude&logoColor=white)](#claudeai)

[![Python 3](https://img.shields.io/badge/Python%203-306998?style=for-the-badge&logo=python&logoColor=white)](#स्क्रिप्ट-सीधे-चलाएँ)
[![macOS](https://img.shields.io/badge/macOS-24292F?style=for-the-badge&logo=apple&logoColor=white)](#macos-और-linux-के-साथ-संगतता)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#macos-और-linux-के-साथ-संगतता)

[इंस्टॉलेशन](#इंस्टॉलेशन) · [इस्तेमाल के उदाहरण](#इस्तेमाल-कैसे-करें) · [यह कैसे काम करती है](#यह-कैसे-काम-करती-है) · [टेस्ट](#टेस्ट)

`pagespeed-audit` **ChatGPT**, **Codex** और **Claude** के लिए एक स्किल है। यह Google PageSpeed Insights (PSI) के नतीजों से अधिकतम तीन प्राथमिक सुधारों की संक्षिप्त रिपोर्ट बनाती है। इससे धीमे पेजों का कारण पता कर सकते हैं, टेम्पलेट या सेटिंग में बदलाव चुन सकते हैं और डिप्लॉयमेंट के पहले और बाद की गति की तुलना कर सकते हैं।

यह सार्वजनिक HTTP(S) साइटों पर काम करती है, जिनमें WordPress, WooCommerce, Shopify, स्टैटिक साइटें और क्लाइंट या सर्वर पर रेंडर होने वाले ऐप शामिल हैं। आप सार्वजनिक URL, साझा रिपोर्ट, स्क्रीनशॉट या PSI JSON दे सकते हैं।

चारों परिवेश एक ही निर्देश फ़ोल्डर इस्तेमाल करते हैं। Codex इसे `.agents/skills/` से लोड करता है और Claude Code `.claude/skills/` में मौजूद सिम्बॉलिक लिंक इस्तेमाल करता है। खाते में सुविधा उपलब्ध होने पर वेब इंटरफ़ेस में स्किल अपलोड कर सकते हैं।

## प्रोजेक्ट में क्या है

| घटक | उपयोग |
| --- | --- |
| `SKILL.md` | सबूत जुटाने, समस्याओं की पहचान करने और रिपोर्ट देने के निर्देश। |
| `scripts/psi.py` | आधिकारिक API से मापता है, JSON को सामान्य रूप में लाता है और संस्करणों की तुलना करता है। केवल Python 3 की मानक लाइब्रेरी इस्तेमाल करता है। |
| `references/` | माप के नियम, सीमाएँ, प्लेटफ़ॉर्म के अनुसार निदान (WordPress और WooCommerce सहित), एजेंट की भूमिकाएँ और रिपोर्ट का प्रारूप। |
| चार सबएजेंट | `psi-field`, `psi-lab`, `psi-implementation` और `psi-review`। ये केवल पढ़ने के लिए हैं और Codex में `.codex/agents/` तथा Claude Code में `.claude/agents/` में हैं। |

## macOS और Linux के साथ संगतता

| इस्तेमाल का तरीका | macOS और Linux पर ज़रूरतें |
| --- | --- |
| ब्राउज़र में ChatGPT या Claude.ai | स्किल अपलोड की अनुमति वाला खाता और तैयार ZIP। ZIP पहले से हो तो स्थानीय Git या Python के बिना अपलोड कर सकते हैं। |
| Codex CLI या Claude Code | प्रोजेक्ट क्लोन करने के लिए Git और अपनी पसंद का टर्मिनल क्लाइंट। |
| ZIP बनाना, `psi.py` चलाना या टेस्ट चलाना | Python 3 और उसकी मानक लाइब्रेरी। `pip` से पैकेज इंस्टॉल करने की ज़रूरत नहीं है। `psi.py fetch` से नया URL मापने के लिए PageSpeed Insights API तक पहुँच चाहिए। |

कमांड macOS के Terminal या Linux के Bash या Zsh टर्मिनल में चलाएँ। नीचे अपनी ज़रूरत के टूल का संस्करण जाँचें।

```bash
git --version
python3 --version
codex --version
claude --version
```

टर्मिनल क्लाइंट के लिए [आधिकारिक Codex CLI निर्देश](https://learn.chatgpt.com/docs/codex/cli) या [Claude Code इंस्टॉलेशन गाइड](https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code) देखें।

macOS और Linux में फ़ाइल सिस्टम के समर्थन पर Git Claude Code का सिम्बॉलिक लिंक बनाए रखता है। लिंक न मिले तो Claude Code अनुभाग के अनुसार साझा फ़ोल्डर की कॉपी इस्तेमाल करें।

टेस्ट Linux पर चलाए गए हैं। macOS पर स्थानीय वर्कफ़्लो की पुष्टि बाकी है।

## इंस्टॉलेशन

| परिवेश | इंस्टॉल करने का तरीका | इस्तेमाल करने का तरीका |
| --- | --- | --- |
| ChatGPT | खाते में अनुमति हो तो **Plugins → Skills** में स्किल अपलोड करें। | “pagespeed-audit स्किल इस्तेमाल करें…” |
| Codex | रिपॉज़िटरी को प्रोजेक्ट की तरह खोलें। | `$pagespeed-audit` |
| Claude.ai | **Customize → Skills** में ZIP अपलोड करें। | “pagespeed-audit स्किल इस्तेमाल करें…” |
| Claude Code | रिपॉज़िटरी को प्रोजेक्ट की तरह खोलें। | `/pagespeed-audit` |

### वेब इंटरफ़ेस के लिए ZIP बनाएँ

रिपॉज़िटरी क्लोन करें और Python 3 से पैकेज बनाएँ। Windows में `python3` उपलब्ध न हो तो `py -3 tools/build_claude_zip.py` चलाएँ।

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

`dist/pagespeed-audit.zip` अपलोड करें। इसमें `SKILL.md`, संदर्भ और स्क्रिप्ट शामिल हैं। रिपॉज़िटरी के चार सबएजेंट इस्तेमाल करने के लिए प्रोजेक्ट Codex या Claude Code में खोलें। वेब इंटरफ़ेस में यही काम क्रम से हो सकता है।

### ChatGPT

1. साइडबार में **Plugins → Skills → Create → Upload from your computer** खोलें।
2. `dist/pagespeed-audit.zip` चुनें और अपलोड की समीक्षा पूरी होने दें।
3. नए चैट में लिखें “pagespeed-audit से मेरी साइट को मोबाइल और डेस्कटॉप पर जाँचें” और सार्वजनिक URL दें या PSI रिपोर्ट संलग्न करें।

अपलोड की सुविधा Skills और वर्कस्पेस की अनुमतियों पर निर्भर है। मेनू न मिले तो Codex इस्तेमाल करें या PSI रिपोर्ट संलग्न करके चैट में सीधे विश्लेषण माँगें। [आधिकारिक ChatGPT Skills गाइड](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) देखें।

### Codex

Git और [स्किल](https://learn.chatgpt.com/docs/build-skills) का समर्थन करने वाला Codex परिवेश चाहिए। चार विशेषज्ञों के लिए [प्रोजेक्ट सबएजेंट](https://learn.chatgpt.com/docs/agent-configuration/subagents) का समर्थन भी चाहिए।

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
codex
```

`$pagespeed-audit` इस्तेमाल करें। स्किल `.agents/skills/pagespeed-audit/` और एजेंट `.codex/agents/` से लोड होते हैं।

### Claude Code

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
claude
```

स्किल `.claude/skills/pagespeed-audit/` और सबएजेंट `.claude/agents/` से लोड होते हैं। “https://example.com/ की गति मोबाइल और डेस्कटॉप पर जाँचें” जैसे शब्दों में अनुरोध करें या `/pagespeed-audit` इस्तेमाल करें।

> सिम्बॉलिक लिंक न हो तो `.agents/skills/pagespeed-audit/` की पूरी कॉपी `.claude/skills/pagespeed-audit/` में रखें। Windows में Git लिंक न बनाए तो भी यही तरीका अपनाएँ।

### Claude.ai

1. खाते में विकल्प दिखे तो **Settings → Capabilities** में कोड चलाने और फ़ाइल बनाने की सुविधा चालू करें। प्रबंधित वर्कस्पेस में जाँचें कि संगठन की नीति स्किल की अनुमति देती है।
2. **Customize → Skills → + → Create skill → Upload a skill** खोलें।
3. `dist/pagespeed-audit.zip` चुनें, स्किल चालू करें और बातचीत में उसका नाम लेकर अनुरोध करें।

[आधिकारिक Claude Skills गाइड](https://support.claude.com/en/articles/12512180-use-skills-in-claude) देखें।

### जब चैट URL को माप न सके

ChatGPT और Claude.ai में अपने आप मापना Google PageSpeed Insights तक पहुँच पर निर्भर है। अनुरोध विफल हो तो [PageSpeed Insights](https://pagespeed.web.dev/) में टेस्ट चलाएँ और लिंक, मोबाइल व डेस्कटॉप के स्क्रीनशॉट या JSON साझा करें। `summarize` JSON फ़ाइलें पढ़ता है। लिंक और स्क्रीनशॉट का विश्लेषण उनमें दिख रहे सबूत के आधार पर होता है।

### किसी अन्य प्रोजेक्ट में जोड़ें

1. पूरी `.agents/skills/pagespeed-audit/` डायरेक्टरी को अपने प्रोजेक्ट में उसी पथ पर कॉपी करें। Claude Code के लिए `.claude/skills/pagespeed-audit` पर कॉपी या सिम्बॉलिक लिंक भी बनाएँ।
2. काम बाँटने के लिए चार `psi-*.toml` फ़ाइलें `.codex/agents/` में या चार `psi-*.md` फ़ाइलें `.claude/agents/` में कॉपी करें। मौजूदा कॉन्फ़िगरेशन सुरक्षित रखें और समान नाम वाली फ़ाइल बदलने से पहले उसे देखें।
3. प्रोजेक्ट की मूल डायरेक्टरी से एजेंट शुरू करें।

स्किल की अतिरिक्त निर्भरताएँ नहीं हैं। स्क्रिप्ट से नया URL मापने के लिए PSI API तक पहुँच चाहिए। बिना कुंजी का कोटा सीमित है। कुंजी चाहिए तो उसे एनवायरनमेंट वैरिएबल के रूप में एक्सपोर्ट करें और रिपॉज़िटरी से बाहर रखें।

```bash
export PAGESPEED_API_KEY="..."
```

स्क्रिप्ट `X-Goog-Api-Key` हेडर में कुंजी Google को भेजती है। इसे चैट या साझा रिपोर्ट में न डालें।

## इस्तेमाल कैसे करें

**URL का ऑडिट करें**

> pagespeed-audit से https://example.com/ को मोबाइल और डेस्कटॉप पर जाँचें। प्राथमिक सुधारों, बदलाव की जगह और सत्यापन के तरीके की संक्षिप्त रिपोर्ट दें।

**मौजूदा रिपोर्ट का विश्लेषण करें**

> इस PageSpeed JSON के साथ pagespeed-audit इस्तेमाल करें। साइट WordPress पर है। वापस लिए जा सकने वाले बदलाव सुझाएँ और किसी कारण की पुष्टि न हो सके तो बताएँ कि कौन-सा सबूत चाहिए।

**डिप्लॉयमेंट की तुलना करें**

> एक ही पेज और डिवाइस की पहले और बाद की रिपोर्ट की तुलना करें। दिखे हुए बदलाव, माप में अंतर और बाकी जाँच बताएँ।

(Codex में स्किल के नाम से पहले `$` लगाएँ: `$pagespeed-audit`।)

पूरी साइट के ऑडिट के लिए अलग-अलग टेम्पलेट के प्रतिनिधि सार्वजनिक URL दें, जैसे होम पेज, लेख और उत्पाद पेज।

### स्क्रिप्ट सीधे चलाएँ

```bash
cd .agents/skills/pagespeed-audit
python3 scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 scripts/psi.py summarize psi-reports/*.json
python3 scripts/psi.py compare antes.json despues.json
```

`fetch` क्रेडेंशियल और आंतरिक पतों के आम पैटर्न पहचानता है। मापने से पहले URL सार्वजनिक हो और उसमें टोकन, निजी डेटा या निजी पहचानकर्ता न हों। `summarize` और `compare` संरचित आउटपुट के लिए `--json` स्वीकार करते हैं।

## यह कैसे काम करती है

1. **सबूत जुटाती है।** दिए हुए PSI नतीजे इस्तेमाल करती है या माँगे गए URL मापती है। रीडायरेक्ट और ब्लॉक पेज पहचानने के लिए डिवाइस, तारीख और अंतिम URL दर्ज करती है।
2. **प्रदर्शन का विश्लेषण करती है।** उपलब्ध होने पर Chrome UX Report (CrUX) के वास्तविक विज़िट डेटा को Lighthouse की लैब माप से अलग करती है। पेज और ओरिजिन का डेटा अलग दिखाती है और तय सीमाओं के आधार पर मेट्रिक वर्गीकृत करती है।
3. **काम बाँटती है।** सुविधा उपलब्ध होने पर फ़ील्ड और लैब एजेंट साथ काम करते हैं। कार्यान्वयन एजेंट नतीजों से सुझाव बनाता है और समीक्षा एजेंट रिपोर्ट को सबूत से मिलाता है। अन्य परिवेश में वही चरण क्रम से चलते हैं।
4. **रिपोर्ट देती है।** उपलब्ध मेट्रिक का सार देती है और असर, भरोसे और जोखिम के आधार पर अधिकतम तीन सुझाव चुनती है। बताती है कि बदलाव कहाँ करें, कैसे जाँचें और ज़रूरत हो तो कैसे वापस लें।

| सबएजेंट | ज़िम्मेदारी |
| --- | --- |
| `psi-field` | डिवाइस और दायरे के अनुसार CrUX की LCP, INP और CLS मेट्रिक समझता है। |
| `psi-lab` | Lighthouse विश्लेषण करता है और समस्या को संसाधन, एलिमेंट या ऑडिट से जोड़ता है। |
| `psi-implementation` | प्लेटफ़ॉर्म के मुताबिक ठोस बदलाव और उनकी जाँच के तरीके सुझाता है। |
| `psi-review` | बिना सबूत वाले दावे, दो बार गिनी गई बचत और अमान्य तुलनाएँ पहचानता है। |

## टेस्ट

```bash
python3 -m unittest discover -s tests -v
```

टेस्ट मेट्रिक सामान्यीकरण, URL सत्यापन, ब्लॉक पेज और Codex व Claude के सबएजेंट की समानता की जाँच करते हैं। `tests/fixtures/` की फ़ाइलें **कृत्रिम** हैं। वे API v5 की संरचना दिखाती हैं, वास्तविक माप नहीं। किसी सबएजेंट को बदलते समय उसकी `.md` और `.toml` साथ अपडेट करें। समानता टेस्ट अंतर बताता है।

## दायरा

PageSpeed को सार्वजनिक पेज तक पहुँच चाहिए। लॉगिन, ब्लॉक या अनपेक्षित रीडायरेक्ट मिलने पर रिपोर्ट दिखाती है कि क्या नहीं मापा जा सका। CrUX डेटा कम हो तो अनुपलब्ध मेट्रिक बताई जाती हैं। ऑडिट सामान्यतः सुझाव देता है। साइट में बदलाव अलग से माँगना होगा।

[PageSpeed Insights की कार्यप्रणाली](https://developers.google.com/speed/docs/insights/v5/about) · [आधिकारिक API](https://developers.google.com/speed/docs/insights/v5/get-started)

## लाइसेंस

यह प्रोजेक्ट [MIT लाइसेंस](LICENSE) के तहत उपलब्ध है। आप इसे व्यावसायिक काम सहित इस्तेमाल, संशोधित और दोबारा वितरित कर सकते हैं। कॉपी या उसके महत्वपूर्ण हिस्से में कॉपीराइट नोटिस और लाइसेंस का पाठ रखें।

निर्माता [Lulu (@lulubumps)](https://github.com/lulubumps)।
