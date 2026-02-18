
# 🛡️ AI Travel Insurance Agent

A full-stack, multi-agent Retrieval-Augmented Generation (RAG) application that acts as a Travel Insurance Advisor. 

This project uses **LangGraph** to route user queries intelligently: 
1. A **Customer Support Agent** handles general greetings and chats.
2. A **Policy Expert Agent** uses RAG (via FAISS) to retrieve specific coverage details, exclusions, and limits from customized travel insurance policy documents.

The backend is powered by **FastAPI** and the frontend is a modern **React (Vite)** application. It supports both cloud LLMs (OpenAI) and local, privacy-first LLMs (Ollama).

---

## 🚀 Features
* **Multi-Agent Routing:** Automatically routes intent between general support and strict policy retrieval.
* **RAG Architecture:** Embeds and searches actual `.txt` policy documents using FAISS.
* **Provider Agnostic:** Easily switch between OpenAI and local Ollama models.
* **Modern UI:** A clean, responsive chat interface built with React.

---

## 📋 Prerequisites
Before you begin, ensure you have the following installed:
* **Python 3.9+**
* **Node.js (v16+)** & npm
* *(Optional)* **Ollama** installed locally if you want to run the models locally without OpenAI API costs. **Note:** You must pull a model that supports tool-calling (e.g., `ollama pull llama3.1`).

---

## 🛠️ Backend Setup (FastAPI + LangGraph)

1. **Navigate to the backend directory:**
   ```bash
   cd backend

```

2. **Create and activate a virtual environment:**
* **Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate

```


* **Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate

```




3. **Install the required Python packages:**
```bash
pip install -r requirements.txt

```


4. **Configure Environment Variables:**
Create a `.env` file in the `backend` directory and add your configurations.
*Example for Local Ollama:*
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

```


*Example for OpenAI:*
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here

```


5. **Run the Backend Server:**
```bash
uvicorn app.main:app --reload

```


*The API will be available at `http://127.0.0.1:8000`.*
*You can view the interactive API docs at `http://127.0.0.1:8000/docs`.*

---

## 💻 Frontend Setup (React + Vite)

1. **Open a new terminal** and navigate to the frontend directory (keep the backend running in your first terminal):
```bash
cd frontend

```


2. **Install Node dependencies:**
```bash
npm install

```


3. **Start the development server:**
```bash
npm run dev

```


4. **Open your browser:**
Navigate to the local URL provided by Vite (usually `http://localhost:5173`) to interact with the AI agent!

---

## 📁 Project Structure

```text
├── backend/
│   ├── app/
│   │   ├── agent/         # LangGraph multi-agent logic & tools
│   │   ├── policies/      # .txt files containing insurance policies
│   │   ├── rag/           # Document loaders, embeddings, FAISS vectorstore
│   │   ├── config.py      # Environment variable configurations
│   │   └── main.py        # FastAPI application & endpoints
│   ├── requirements.txt   # Python dependencies
│   └── .env               # (You create this) LLM API Keys & settings
│
└── frontend/
    ├── src/
    │   ├── App.jsx        # Main React chat interface
    │   ├── App.css        # UI styling and animations
    │   └── main.jsx       # React entry point
    ├── package.json       # Node dependencies
    └── vite.config.js     # Vite configuration

```

---

## 🧪 Testing the Agent

Try asking the agent different types of questions to see the multi-agent routing in action!

* **Support Agent Intent:** *"Hi, how are you today?"* or *"Who are you?"*
* **Policy Expert Intent:** *"What does the Premium Elite plan cover?"* or *"Does the Adventure Pro plan cover scuba diving?"*

---

## 🧰 Tech Stack

* **Framework:** FastAPI, React (Vite)
* **AI & Orchestration:** LangChain, LangGraph
* **Vector Database:** FAISS
* **Embeddings & LLMs:** OpenAI, Ollama

```

```
