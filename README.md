Adaptive AI Learning Engine
An AI-powered backend system that transforms PDF documents into interactive, adaptive quizzes. Built with FastAPI, SQLAlchemy, and Google Gemini, this system features intelligent document chunking, duplicate question detection, and a dynamic feedback loop that adjusts to student performance.

🚀 Key Technical Highlights
Idempotent Generation: Implemented duplicate detection logic to prevent redundant database entries and optimize API costs.

Schema Validation: Strictly enforced AI-generated content structures using Pydantic models.

Adaptive Learning Loop: Real-time evaluation of student answers to trigger difficulty scaling.

Relational Data Modeling: Normalized SQLite schema with cascading deletes and strict foreign key constraints.

🛠️ Installation & Setup
1. Clone the Repository
Bash
git clone <your-repo-link>
cd <project-folder>
2. Install Dependencies
Ensure you have Python 3.9+ installed. It is recommended to use a virtual environment.

Bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the root directory:

Plaintext
GEMINI_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite:///./peblo_quiz.db
🚦 How to Run the Backend
Start the local development server on Port 8002:

Bash
uvicorn main:app --reload --port 8002
The backend will be available at: http://127.0.0.1:8002

🧪 How to Test Endpoints
Access the Interactive API Documentation (Swagger UI) at: http://127.0.0.1:8002/docs

Step 1: Ingest – Use POST /ingest to upload a PDF. Note the document_id and chunk_id.

Step 2: Generate – Use POST /generate-quiz with a chunk_id. This triggers the AI engine and the Duplicate Detection logic.

Step 3: Submit – Use POST /submit-answer. Observe the is_correct boolean and the adaptive_feedback for mastery evaluation.

🏗️ System Architecture & Optional Features
1. Duplicate Question Detection
Location: main.py -> POST /generate-quiz

Logic: Before calling the Gemini API, the system queries the database via SQLAlchemy filters to check if questions already exist for the given chunk_id.

Effect: Eliminates UNIQUE constraint errors and reduces redundant LLM API costs.

2. Schema Validation (Pydantic)
Location: ai_engine.py

Logic: Enforces a strict JSON structure (Question, Options, Correct Answer) on the AI's probabilistic output.

Effect: Prevents runtime crashes caused by malformed or incomplete AI responses.

3. Adaptive Learning Loop
Location: main.py -> POST /submit-answer

Logic: Implements text normalization and a logic gate that generates a "Mastery Signal" based on performance.

Effect: Provides dynamic, real-time feedback that informs the system to increase or decrease difficulty.
Duplicate Detection: A pre-write check verifies if questions already exist for a specific chunk, ensuring the system is idempotent and cost-effective.

3. Adaptive Feedback Loop
The system performs text normalization on student inputs and evaluates mastery. Correct answers trigger a signal to increase difficulty, creating a personalized, non-linear learning path.
