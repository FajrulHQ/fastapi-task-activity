from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, models
from app.services.auth import schemas as schemas_auth
from app.config.utils import page_size_pagination
import requests
from datetime import datetime

def create_task_activity(db: Session, user: schemas_auth.User, task: schemas.TaskActivity):
  db_task = models.TaskActivity(**task.__dict__, created_by=user.username, modified_by=user.username)
  db.add(db_task)
  db.commit()
  db.refresh(db_task)
        
  return db_task

def get_tasks_activity(db: Session, params: schemas.TaskActivityParams):
  query = db.query(models.TaskActivity)
  # Filter by params
  for (key, value) in params.__dict__.items():
    if (key not in ['order','sort','page','size']) and \
       (value is not None):
      filter_column = getattr(models.TaskActivity, key)
      query = query.filter(filter_column.contains(value))
      
  # Sort with order
  if params.order != None:
    order_column = getattr(models.TaskActivity, params.order)
    if params.sort == 'asc':
      order_column = order_column.asc()
    else:
      order_column = order_column.desc()
    query = query.order_by(order_column)
    
  return page_size_pagination(query, params.page, params.size)

def update_task_activity_status(db: Session, user: schemas_auth.User, data: schemas.TaskActivityUpdate):
  task = db.query(models.TaskActivity).filter_by(task_id=data.id).first()
  if task is None:
    raise HTTPException(status_code=404, detail="Not found")
  
  if data.status:
    now = datetime.now()
    history_exist = db.query(models.TaskHistory).filter_by(object_id=data.id).first()
    
    # History capture
    history = models.TaskHistory(
      object_id=task.task_id,
      object_type='Tasks Activity',
      object_name=task.task_name,
      activity=data.status,
      created_by=user.username,
      created_at=now,
    )
    db.add(history)
    db.commit()
    
    # History detail capture
    previous_action = 'Modified' if history_exist else 'Created'
    latest_action = 'Modified'
    print(previous_action, latest_action)
    for field, values in zip(
      ["status", "created_at", "created_by", "action"],
      [
        [task.status, data.status],
        [task.modified_at, now],
        [task.modified_by, user.username],
        [previous_action, latest_action]
      ]):
      if values[0] != values[1]:
        history_detail = models.TaskHistoryDetail(
          field_name=field,
          previous_data_value=values[0],
          latest_data_value=values[1],
          history_id=history.id
        ) 
        db.add(history_detail)
        db.commit()
    
    # Update task activitiy status
    task.status = data.status
    task.modified_at = now
    task.modified_by = user.username
    db.commit()
    
  return {"detail", "task updated successfully"}
  