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

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the root directory and add your Google Gemini API key:

Plaintext
GEMINI_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite:///./peblo_quiz.db
🚦 How to Run the Backend
Start the local development server using Uvicorn:

Bash
uvicorn main:app --reload
The backend will be available at: http://127.0.0.1:8000

🧪 How to Test Endpoints
The easiest way to test the system is through the Interactive API Documentation (Swagger UI).

Open your browser and navigate to http://127.0.0.1:8000/docs.

Step 1: Ingest – Use POST /ingest to upload a PDF (e.g., vkvn.pdf). Note the document_id and chunk_id in the response.

Step 2: Generate – Use POST /generate-quiz by passing a chunk_id. This triggers the AI engine and duplicate detection logic.

Step 3: Submit – Use POST /submit-answer with a question_id and student_answer. Observe the adaptive_feedback field for the performance evaluation.

🏗️ System Architecture & Logic
1. Document Ingestion
Uses a Fixed-Size Chunking Strategy with a sliding window overlap. This ensures that semantic meaning is preserved at the boundaries of text segments, preventing context loss for the AI.

2. AI Orchestration & Validation
Validation: Uses Pydantic to ensure AI responses follow a strict JSON schema (Question, 4 Options, Correct Answer).

Duplicate Detection: A pre-write check verifies if questions already exist for a specific chunk, ensuring the system is idempotent and cost-effective.

3. Adaptive Feedback Loop
The system performs text normalization on student inputs and evaluates mastery. Correct answers trigger a signal to increase difficulty, creating a personalized, non-linear learning path.
