import os
from fastapi import FastAPI, Depends, UploadFile, File, Query, HTTPException
from sqlalchemy.orm import Session
import models, database, ingestor, ai_engine

app = FastAPI(title="Peblo AI Quiz Engine")

# Initialize database tables on startup
database.init_db()

# Dependency to get a database session for each request
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Content Ingestion Endpoint
@app.post("/ingest", tags=["Ingestion"])
async def ingest_content(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a PDF, extract its text, chunk it, and save it to the database.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Save file temporarily to process it
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    try:
        # Extract and Chunk text using your ingestor logic
        chunks = ingestor.process_pdf(file_location)
        
        # Save Document metadata
        doc = models.Document(filename=file.filename)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        # Save each chunk to the database
        for text in chunks:
            new_chunk = models.ContentChunk(doc_id=doc.id, text=text)
            db.add(new_chunk)
        
        db.commit()
        return {
            "message": f"Successfully ingested {len(chunks)} sections from {file.filename}",
            "document_id": doc.id
        }
    finally:
        # Always clean up the temporary file
        if os.path.exists(file_location):
            os.remove(file_location)

# 2. Quiz Generation Endpoint
@app.post("/generate-quiz", tags=["Quiz"])
async def generate_quiz(chunk_id: int, difficulty: str = "medium", db: Session = Depends(get_db)):
    """
    Triggers the LLM to generate questions based on a specific chunk of content.
    """
    chunk = db.query(models.ContentChunk).filter(models.ContentChunk.id == chunk_id).first()
    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found")
    
    # Call the AI Engine to get JSON questions
    questions_data = ai_engine.generate_quiz_from_chunk(chunk.text, difficulty)
    
    # Save the generated questions to the database
    for q in questions_data:
        new_q = models.QuizQuestion(
            chunk_id=chunk.id,
            question_text=q['question'],
            question_type=q['type'],
            options=str(q.get('options', [])), # Store MCQ options as string
            correct_answer=q['answer'],
            difficulty=q['difficulty']
        )
        db.add(new_q)
    
    db.commit()
    return {"message": "Quiz questions generated", "count": len(questions_data)}

# 3. Quiz Retrieval Endpoint
@app.get("/quiz", tags=["Quiz"])
async def get_quiz(difficulty: str = "easy", db: Session = Depends(get_db)):
    """
    Retrieve questions filtered by the requested difficulty.
    """
    questions = db.query(models.QuizQuestion).filter(models.QuizQuestion.difficulty == difficulty).all()
    return questions

# 4. Student Submission & Adaptive Logic
@app.post("/submit-answer", tags=["Adaptive Logic"])
async def submit_answer(student_id: str, question_id: int, answer: str, db: Session = Depends(get_db)):
    """
    Grade the student's answer and calculate the next suggested difficulty level.
    """
    question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Grade the answer
    is_correct = (answer.strip().lower() == question.correct_answer.strip().lower())
    
    # Adaptive Logic Ladder
    current_diff = question.difficulty
    next_diff = current_diff
    
    if is_correct:
        if current_diff == "easy": next_diff = "medium"
        elif current_diff == "medium": next_diff = "hard"
    else:
        if current_diff == "hard": next_diff = "medium"
        elif current_diff == "medium": next_diff = "easy"
        
    # Log the response in the database
    response_log = models.StudentResponse(
        question_id=question_id,
        student_id=student_id,
        selected_answer=answer,
        is_correct=is_correct
    )
    db.add(response_log)
    db.commit()

    return {
        "is_correct": is_correct,
        "current_difficulty": current_diff,
        "next_suggested_difficulty": next_diff,
        "feedback": "Correct! Stepping up." if is_correct else "Incorrect. Let's try something easier."
    }
