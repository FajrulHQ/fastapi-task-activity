from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from app.config import database, settings
from app.services.auth import crud as crud_auth, schemas as schemas_auth
from . import schemas, crud, models

router = APIRouter()
module = 'task'
route = f"/{module}"

@router.post("/activity/", tags=[module])
def create_task_activity(
  task: schemas.TaskActivityBase, 
  user: schemas_auth.User = Depends(crud_auth.verify_token),
  db: Session = Depends(database.get_db)
):
  return crud.create_task_activity(db=db, user=user, task=task)

@router.get("/activity/", tags=[module], dependencies=[Depends(crud_auth.verify_token)])
def get_task_activity(
  params: schemas.TaskActivityParams = Depends(),
  db: Session = Depends(database.get_db)
):
  return crud.get_tasks_activity(db=db, params=params)

@router.get("/activity/{id}", tags=[module], dependencies=[Depends(crud_auth.verify_token)])
def get_task_activity_by_id(
  id: int,
  db: Session = Depends(database.get_db)
):
  task = db.query(models.TaskActivity).filter_by(task_id=id).first()
  if task is None:
    raise HTTPException(status_code=404, detail="Not found")
  return task

@router.delete("/activity/{id}", tags=[module], dependencies=[Depends(crud_auth.verify_token)])
def get_task_activity_by_id(
  id: int,
  db: Session = Depends(database.get_db)
):
  task = db.query(models.TaskActivity).filter_by(task_id=id).first()
  if task is None:
    raise HTTPException(status_code=404, detail="Not found")
  db.delete(task)
  db.commit()
  return {"detail": "Task deleted successfully"}

@router.put("/activity/{id}", tags=[module])
def get_task_activity_by_id(
  id: int,
  data: schemas.TaskActivityUpdate,
  user: schemas_auth.User = Depends(crud_auth.verify_token),
  db: Session = Depends(database.get_db)
):
  data.id = id
  return crud.update_task_activity_status(db=db, user=user, data=data)
