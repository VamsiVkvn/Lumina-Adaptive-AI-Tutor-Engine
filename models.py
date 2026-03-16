from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)

class ContentChunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    content = Column(String)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("chunks.id"))
    question_text = Column(String, unique=True, nullable=False) # Bonus: Duplicate Detection
    options = Column(String, nullable=True) # JSON string
    correct_answer = Column(String, nullable=False)
    difficulty = Column(String, default="medium")
    question_type = Column(String)

    __table_args__ = (UniqueConstraint('question_text', name='_question_text_uc'),)

class StudentProgress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String)
    question_id = Column(Integer, ForeignKey("questions.id"))
    is_correct = Column(Boolean)
