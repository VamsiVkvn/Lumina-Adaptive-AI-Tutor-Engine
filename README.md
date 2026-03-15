# Lumina: Adaptive AI Tutor Engine

**Lumina** is a sophisticated backend architecture designed to bridge the gap between static educational resources and personalized learning. By transforming raw PDF content into an intelligent, responsive quiz environment, the system creates a dynamic feedback loop that caters to the individual needs of every student.

## 🌟 Project Overview
This engine automates the pedagogical workflow—from document ingestion to real-time difficulty adjustment. It ensures that educational content is not just consumed, but understood through active, AI-generated assessments.

---

## 🚀 Core Capabilities

### 🧠 Semantic Content Processing
Beyond simple text extraction, the system utilizes an intelligent chunking strategy to maintain pedagogical context, allowing for precise mapping of questions to their original source material.

### 📝 Generative Assessment Framework
Orchestrates Large Language Models (LLMs) to synthesize diverse question types—including Multiple Choice, True/False, and Fill-in-the-blank—ensuring a comprehensive evaluation of student comprehension.

### 📈 Real-Time Adaptive Logic
Implements a proprietary difficulty-scaling algorithm. By monitoring student accuracy in real-time, the engine dynamically adjusts the complexity of the learning path, scaling between **Easy**, **Medium**, and **Hard** tiers.

### ⚡ High-Performance API Design
Built on the **FastAPI** framework, providing asynchronous data handling and a fully documented, interactive interface (Swagger UI) for seamless frontend integration.

---

## 🛠️ Technical Implementation

- **Orchestration**: Python-based FastAPI with Pydantic for strict data validation.
- **Data Layer**: SQLAlchemy ORM for relational data management and SQLite for lightweight, persistent storage.
- **AI Layer**: Deep integration with state-of-the-art LLMs (OpenAI/Gemini) using advanced prompt engineering for structured JSON outputs.
- **Extraction**: PyMuPDF (Fitz) for high-fidelity PDF parsing and character-based content segmentation.

---

## 🏁 Quick Start
1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Setup Keys**: Add your API key to the `.env` file.
3. **Run Server**: `uvicorn main:app --reload --port 8001`
4. **Interactive Docs**: Navigate to `http://127.0.0.1:8001/docs`