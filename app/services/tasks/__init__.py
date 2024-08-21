from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, responses
from sqlalchemy.orm import Session
from app.config import database, settings
from app.services.auth import crud as crud_auth, schemas as schemas_auth
from . import schemas, crud, models
import logging, sys

router = APIRouter()
module = 'task'
route = f"/{module}"

# Notification webhooks
@router.post("/notification")
def send_notification(
    body: schemas.TaskNotification
):
    message = f"{body.category[0]} {body.object_type} of {body.object_name[0]} {body.action} {body.event}"
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s:\t  %(message)s')
    logging.info(message)
  
@router.post("/", tags=[module])
def create_task_activity(
  task: schemas.TaskActivityBase, 
  bt: BackgroundTasks,
  user: schemas_auth.User = Depends(crud_auth.verify_token),
  db: Session = Depends(database.get_db),
):
  notification = schemas.TaskNotification(object_type="Tasks Activity")
  try:
    task = crud.create_task_activity(db=db, user=user, task=task)
    notification.category=task.activity_group_sub_category_name,
    notification.object_name=task.task_name,
    notification.event = "created successfully"
    bt.add_task(send_notification, notification)
    return task
  except Exception as e:
    notification.event = "failed to create"
    bt.add_task(send_notification, notification)
    return responses.JSONResponse(status_code=400, content={"detail": str(e)})
  
  

@router.get("/", tags=[module], dependencies=[Depends(crud_auth.verify_token)])
def get_task_activity(
  params: schemas.TaskActivityParams = Depends(),
  db: Session = Depends(database.get_db)
):
  return crud.get_tasks_activity(db=db, params=params)

@router.get("/{id}", tags=[module], dependencies=[Depends(crud_auth.verify_token)])
def get_task_activity_by_id(
  id: int,
  db: Session = Depends(database.get_db)
):
  task = db.query(models.TaskActivity).filter_by(task_id=id).first()
  if task is None:
    raise HTTPException(status_code=404, detail="Not found")
  return task

@router.delete("/{id}", tags=[module], dependencies=[Depends(crud_auth.verify_token)])
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

@router.put("/{id}", tags=[module])
def get_task_activity_by_id(
  id: int,
  data: schemas.TaskActivityUpdate,
  bt: BackgroundTasks,
  user: schemas_auth.User = Depends(crud_auth.verify_token),
  db: Session = Depends(database.get_db)
):
  data.id = id
  notification = schemas.TaskNotification(object_type="Tasks Activity")
  try:
    task = crud.update_task_activity_status(db=db, user=user, data=data)
    notification.category=task.activity_group_sub_category_name,
    notification.object_name=task.task_name,
    notification.event = f"status modified to `{task.status}`"
    bt.add_task(send_notification, notification)
    return task
  except Exception as e:
    notification.event = "failed to modify"
    bt.add_task(send_notification, notification)
    return responses.JSONResponse(status_code=400, content={"detail": str(e)})
