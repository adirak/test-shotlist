from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models import Shot
from app.schemas import ShotCreate, ShotRead, ShotUpdate, Status

router = APIRouter(prefix="/shots", tags=["shots"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=list[ShotRead])
async def list_shots(db: SessionDep, status: Status | None = None,
                     limit: int = Query(20, le=100), offset: int = 0):
    stmt = select(Shot).order_by(Shot.created_at.desc()).limit(limit).offset(offset)
    if status:
        stmt = stmt.where(Shot.status == status)
    return (await db.execute(stmt)).scalars().all()


@router.post("", response_model=ShotRead, status_code=201)
async def create_shot(payload: ShotCreate, db: SessionDep):
    shot = Shot(**payload.model_dump())
    db.add(shot)
    await db.commit()
    await db.refresh(shot)
    return shot


@router.get("/{shot_id}", response_model=ShotRead)
async def get_shot(shot_id: int, db: SessionDep):
    shot = await db.get(Shot, shot_id)
    if not shot:
        raise HTTPException(404, "Shot not found")
    return shot


@router.patch("/{shot_id}", response_model=ShotRead)
async def update_shot(shot_id: int, payload: ShotUpdate, db: SessionDep):
    shot = await db.get(Shot, shot_id)
    if not shot:
        raise HTTPException(404, "Shot not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(shot, field, value)
    await db.commit()
    await db.refresh(shot)
    return shot


@router.delete("/{shot_id}", status_code=204)
async def delete_shot(shot_id: int, db: SessionDep):
    shot = await db.get(Shot, shot_id)
    if not shot:
        raise HTTPException(404, "Shot not found")
    await db.delete(shot)
    await db.commit()
