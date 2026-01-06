# 🚀 Action-RAG | Enterprise Knowledge Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-RAG-orange)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-green)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Groq](https://img.shields.io/badge/Inference-Groq-purple)

> **A production-style Retrieval-Augmented Generation (RAG) system with zero-hallucination guardrails and agentic workflow automation.**

> ⚠️ **Important Note (Fresher-Friendly):**  
> This is a **personal learning project** designed to simulate **real-world enterprise AI systems**.  
> It is **not deployed in a company**, but follows **industry-relevant design principles**.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [Real-World Usefulness](#-real-world-usefulness)
- [Tech Stack](#-tech-stack)
- [How to Run This Project](#-how-to-run-this-project-local-setup)
- [Anti-Hallucination Strategy](#-anti-hallucination-strategy)
- [Security & Privacy](#-security--privacy)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

---

## 📖 Overview

**Action-RAG** is an AI-powered knowledge assistant that allows users to query internal documents such as **PDF, DOCX, and TXT files** and receive **accurate, traceable, and context-based answers**.

Unlike generic AI chatbots, Action-RAG is designed with **reliability and safety** in mind:

- Answers are generated **only from uploaded documents**
- Every response includes **source citations**
- The system **refuses to answer** if information is not present
- Retrieved knowledge can be converted into **actionable outputs** like professional emails

This project focuses on **enterprise-style thinking**, not just model usage.

---

## ❓ Problem Statement

In real organizations:

- Knowledge is scattered across large documents
- Employees waste time manually searching PDFs
- AI chatbots often hallucinate answers
- Responses lack source traceability
- Information retrieval does not lead to action

These problems reduce productivity and trust in AI systems.

---

## ✅ Solution

Action-RAG solves these issues by combining:

- **Semantic search using FAISS**
- **Strict context-based LLM prompting**
- **Agentic workflow automation**

The result is a **trustworthy AI assistant** that retrieves information, validates it, and helps users act on it.

---

## 🌟 Key Features

### 🔒 Zero-Hallucination Design

- Model answers **only from retrieved document context**
- Explicit refusal when the answer is not found
- No guessing or speculative responses

### ⚡ Fast Semantic Search

- FAISS vector database
- Local embeddings using FastEmbed
- Efficient CPU-based retrieval

### 📝 Source Citations

- Each answer includes:
  - Document name
  - Page number
- Enables verification and audit readiness

### 🤖 Agentic Workflow (Action Module)

- One-click **professional email drafting**
- Converts retrieved knowledge into actionable communication

### 🛡️ Security-Oriented Design

- Documents processed locally
- No cloud-based embedding APIs
- Minimal data exposure

---

## 🌍 Real-World Usefulness

### 🏢 Enterprise Knowledge Search

Employees can quickly query internal documents instead of manually searching long PDFs, saving time and effort.

### ⚖️ Legal & Compliance Teams

- Prevents hallucinated legal interpretations
- Provides traceable answers
- Useful for audits and policy verification

### 👩‍💼 HR & Policy Management

Safely answers questions related to:

- Leave policies
- Company rules
- Internal guidelines

### 🧑‍💻 Engineering Teams

Developers can query technical documentation and instantly draft clarification emails.

### 📧 From Information to Action

Action-RAG bridges the gap between **information retrieval and real-world action** by generating ready-to-send professional emails.

---

## ⚙️ System Architecture (High-Level Flow)

1. User uploads documents
2. Documents are chunked and embedded locally
3. Embeddings are stored in FAISS
4. User asks a question
5. Relevant chunks are retrieved
6. LLM answers strictly from context
7. Response includes citations
8. Optional email draft is generated

---

## 🧰 Tech Stack

- **Language:** Python 3.10+
- **LLM Orchestration:** LangChain
- **Vector Database:** FAISS
- **Embeddings:** FastEmbed (local)
- **Inference Engine:** Groq (Llama 3)
- **Frontend:** Streamlit

---

▶️ How to Run This Project (Local Setup)
1️⃣ Clone the Repository
git clone https://github.com/yourusername/Action-RAG.git
cd Action-RAG

2️⃣ Create Virtual Environment
python -m venv venv

Activate the environment

# Windows

venv\Scripts\activate

# Linux / Mac

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in the root directory:

GROQ_API_KEY=your_groq_api_key

5️⃣ Run the Application
streamlit run app.py

Open your browser and visit: http://localhost:8501

## 🚫 Anti-Hallucination Strategy

- Strict prompt instructions
- Context-only answering
- Explicit refusal when data is missing

This ensures **safe and reliable responses**, suitable for **enterprise-like environments**.

---

## 🔐 Security & Privacy

- Local document processing
- No cloud-based embeddings
- Suitable for confidential internal documents

---

## 🔮 Future Enhancements

- Role-based access control
- Multi-agent workflows
- Slack / Email integration
- Multi-language document support

---

## 👤 Author

**Harsh Malokar**  
BE Computer Engineering | Pune, India  
Aspiring Software Engineer | AI & Backend Enthusiast

⭐ _If you find this project useful, feel free to star the repository!_

---
