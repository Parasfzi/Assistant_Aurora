# 🌌 Assistant Aurora  

> A futuristic AI assistant powered by **voice recognition, GPT intelligence, real-time web search, and a customizable modular system** — designed to feel like your own digital companion.  

---

## 🏷️ Badges  

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)  
![License](https://img.shields.io/badge/License-MIT-green)  
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)  
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)  

---

## ✨ Features  

- 🎙️ **Voice Recognition** — Powered by [Whisper](https://github.com/openai/whisper).  
- 🧠 **Smart AI** — Natural replies via [OpenRouter](https://openrouter.ai/) & GPT models.  
- 🌍 **Web Search** — Summarizes internet search results in real-time.  
- 🔔 **Utilities** — Timers, reminders, emails, translation, news updates.  
- 🛠️ **Custom Commands** — Easily extend functionality with `custom_commands.json`.  
- 💡 **Modular Design** — Each feature lives in its own module.  
- 🖥️ **GUI (WIP)** — Futuristic hologram-style GUI with live waveforms (coming soon).  

---

## 🛠️ Tech Stack  

- **Language**: Python 3.10+  
- **AI/ML**: Whisper, GPT via OpenRouter API  
- **Conversation Engine**: RiveScript  
- **GUI**: Tkinter / PyQt (future: WebGL / Three.js)  
- **APIs**: News API, Translation API, Email Service  

---

## 📂 Project Structure  

```
Assistant_Aurora/
│── main.py                     # Entry point
│── aurora_gui.py                # GUI (WIP)
│── command_handler.py           # Command router
│── modules/
│    ├── speech_recognition_module.py
│    ├── text_to_speech_module.py
│    ├── web_search_module.py
│    ├── news_module.py
│    ├── email_module.py
│    ├── translation_module.py
│    ├── timer_reminder_module.py
│    ├── smart_ai_module.py
│    └── custom_command_module.py
│── config.py
│── aurora_knowledge.json
│── custom_commands.json
│── requirements.txt
│── README.md
```

---

## 🚀 Installation  

1. **Clone repository**  
```bash
git clone https://github.com/Parasfzi/Assistant_Aurora.git
cd Assistant_Aurora
```

2. **Setup virtual environment**  
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

3. **Install requirements**  
```bash
pip install -r requirements.txt
```

4. **Configure API keys**  
Create `.env` file in root and add your API keys:  
```env
OPENROUTER_API_KEY=your_api_key_here
NEWS_API_KEY=your_api_key_here
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_password
```

---

## ▶️ Usage  

Run Aurora:  
```bash
python main.py
```

Example commands:  
- "Aurora, search latest AI news"  
- "Set a reminder for 6 PM"  
- "Translate Hello to French"  
- "Send an email to John"  

---

## 🔮 Roadmap  

- [ ] Advanced **3D GUI** with hologram effects  
- [ ] Real-time **voice waveform animations**  
- [ ] **Contextual memory** for longer conversations  
- [ ] Cross-platform installer (Windows/Mac/Linux)  
- [ ] Mobile app integration  

---

## 🤝 Contributing  

Contributions are welcome!  

1. Fork the repo  
2. Create a branch (`feature/my-feature`)  
3. Commit changes  
4. Open a pull request  

---

## 📜 License  

This project is licensed under the **MIT License**.  

---

## 💡 Inspiration  

Aurora aims to be more than a simple assistant — it’s a **personal AI companion** blending productivity, web intelligence, and futuristic design.  
