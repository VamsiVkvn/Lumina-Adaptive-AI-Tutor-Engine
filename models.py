from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    grade = Column(Integer, nullable=True)
    subject = Column(String, nullable=True)

class ContentChunk(Base):
    __tablename__ = "content_chunks"
    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(Integer, ForeignKey("documents.id"))
    text = Column(Text)
    topic = Column(String, nullable=True)
    
    questions = relationship("QuizQuestion", back_populates="source_chunk")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("content_chunks.id"))
    question_text = Column(Text)
    question_type = Column(String) 
    options = Column(Text, nullable=True) 
    correct_answer = Column(String)
    difficulty = Column(String) 
    
    source_chunk = relationship("ContentChunk", back_populates="questions")

class StudentResponse(Base):
    __tablename__ = "student_responses"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"))
    student_id = Column(String)
    selected_answer = Column(String)
    is_correct = Column(Boolean)
