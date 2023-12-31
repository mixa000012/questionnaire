from fastapi import APIRouter, Request, FastAPI, WebSocket, WebSocketDisconnect
from app.core import store
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.deps import get_db
from app.questions.schema import QuestionCreate


class SurveyDoesntExist(Exception):
    pass


async def create_question(obj: QuestionCreate, db: AsyncSession = Depends(get_db)):
    survey = await store.survey.get(id=obj.survey_id, db=db)
    if survey:
        question = await store.question.create_question(db=db, obj_in=obj)
    else:
        raise SurveyDoesntExist
    return question


async def get_question(db: AsyncSession = Depends(get_db)):
    question = await store.question.get_question_with_options(db=db, skip=0, limit=100)
    return question
