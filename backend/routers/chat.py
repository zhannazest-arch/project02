from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import schemas
from ai.advisor import generate_response

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    message, universities = generate_response(request.messages, db)
    return schemas.ChatResponse(
        message=message,
        universities=universities if universities else None,
    )
