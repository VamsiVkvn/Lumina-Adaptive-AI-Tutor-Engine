from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import json, models, ingestor, ai_engine
from database import engine, get_db, Base

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lumina AI Demo Ready")

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    text = await ingestor.extract_text(file)
    chunks = ingestor.create_chunks(text)
    db_doc = models.Document(filename=file.filename)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    for content in chunks:
        db.add(models.ContentChunk(document_id=db_doc.id, content=content))
    db.commit()
    return {"document_id": db_doc.id, "chunks": len(chunks)}

@app.post("/generate-quiz")
async def generate_quiz(chunk_id: int, db: Session = Depends(get_db)):
    existing_qs = db.query(models.Question).filter(models.Question.chunk_id == chunk_id).all()
    if existing_qs:
        return existing_qs

    chunk = db.query(models.ContentChunk).filter(models.ContentChunk.id == chunk_id).first()
    if not chunk: return {"error": "Chunk not found"}
    
    questions = await ai_engine.generate_quiz_from_ai(chunk.content)
    saved = []
    for q in questions:
        check = db.query(models.Question).filter(models.Question.question_text == q.question).first()
        if not check:
            db_q = models.Question(
                chunk_id=chunk_id,
                question_text=q.question,
                options=json.dumps(q.options),
                correct_answer=q.answer,
                difficulty=q.difficulty,
                question_type=q.type
            )
            db.add(db_q)
            db.commit()
            db.refresh(db_q)
            saved.append(db_q)
        else:
            saved.append(check)
    return saved

@app.post("/submit-answer")
async def submit_answer(student_id: str, question_id: int, student_answer: str, db: Session = Depends(get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q: return {"error": "Question not found"}
    
    is_correct = str(student_answer).strip().lower() == str(q.correct_answer).strip().lower()
    
    return {
        "is_correct": is_correct,
        "correct_answer": q.correct_answer,
        "adaptive_feedback": "Correct! Increasing difficulty." if is_correct else "Let's try an easier one."
    }
