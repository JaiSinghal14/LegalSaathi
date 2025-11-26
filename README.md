# 📘 LegalSaathi — AI-Powered Legal Support Assistant

**LegalSaathi** is an AI-driven legal-support tool designed to help users quickly generate complaint drafts, identify relevant IPC sections, and fetch precedent case suggestions.  
Built using **CrewAI**, it provides fast, structured, and reliable legal assistance tailored for Indian legal scenarios.

---

## 🚀 Features

- **Complaint Drafting**  
  Generate clear and structured legal complaint drafts from a user’s description.

- **IPC Section Identification**  
  Automatically detect relevant **Indian Penal Code (IPC)** sections.

- **Precedent Case Suggestions**  
  Get case references aligned with the incident details.

- **Multi-Agent Workflow (CrewAI)**  
  A coordinated agent system for analysis, drafting, and refinement.

- **User-Friendly Interface**  
  Simple input → complete legal output.

---
## 📸 Screenshots

### 🖼️ Home Interface
![Home Interface](screenshots/home.png)

---

### 🧠 AI Output (Part 1)
![Output Part 1](screenshots/output_1.png)

### 🧠 AI Output (Part 2)
![Output Part 2](screenshots/output_2.png)

---

## 🧠 How It Works

1. User enters a legal situation or scenario.  
2. **Complaint Agent** drafts a structured legal complaint.  
3. **IPC Agent** identifies applicable Indian Penal Code sections.  
4. **Precedent Agent** fetches similar case references.  
5. **Supervisor Agent** organizes the final output.

---

## 🛠️ Tech Stack

- Python 3  
- CrewAI  
- Groq / OpenAI LLMs  
- dotenv  
- (Optional) Streamlit / FastAPI UI  

---

```md
## 📁 Project Structure

.
├── main.py
├── agents/
│   ├── complaint_agent.py
│   ├── ipc_agent.py
│   ├── precedent_agent.py
│   └── supervisor.py
├── tools/
├── prompts/
├── env_template.txt
├── home.png
├── output_1.png
├── output_2.png
├── output_3.png
└── README.md
```

## 🤝 Contributing

Contributions, improvements, and suggestions are welcome!
Feel free to submit issues or pull requests.
