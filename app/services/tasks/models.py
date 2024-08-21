from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey, orm
from datetime import datetime
from app.config.database import Base

class TaskActivity(Base):
  __tablename__                     = "tasks_activity"
  
  task_id                           = Column(Integer, primary_key=True, index=True)
  task_name                         = Column(String)
  task_description                  = Column(String)
  activity_type_id                  = Column(Integer)
  activity_type_name                = Column(String, nullable=False)
  activity_group_sub_category_id    = Column(Integer)
  activity_group_sub_category_name  = Column(String, nullable=False)
  activity_group_id                 = Column(Integer)
  activity_group_name               = Column(String, nullable=False)
  stage_id                          = Column(Integer)
  stage_name                        = Column(String, default="New", nullable=False)
  core_group_category_id            = Column(Integer)
  core_group_category               = Column(String, nullable=False)
  core_group_id                     = Column(Integer)
  core_group_name                   = Column(String)
  due_date                          = Column(DateTime)
  action_type                       = Column(String)
  related_to                        = Column(String)
  related_to_picture_id             = Column(String)
  related_to_email                  = Column(String)
  related_to_company                = Column(String)
  assigned_to                       = Column(String)
  assigned_to_picture_id            = Column(String)
  assigned_to_email                 = Column(String)
  assigned_to_company               = Column(String)
  notes                             = Column(String)
  status                            = Column(String, default="Not Started", nullable=False)
  attachment_id                     = Column(Integer)
  attachments                       = Column(String)
  link_response_id                  = Column(String)
  link_object_id                    = Column(String)
  created_by                        = Column(String)
  created_at                        = Column(DateTime, default=datetime.now)
  created_by_picture_id             = Column(Integer)
  modified_by                       = Column(String)
  modified_at                       = Column(DateTime, default=datetime.now)
  modified_by_picture_id            = Column(Integer)
  key                               = Column(String)
  favorite                          = Column(String)
  session_id                        = Column(String)
  
  history                           = orm.relationship('TaskHistory', back_populates='object')
  
  
class TaskHistory(Base):
  __tablename__                     = "tasks_history"
  
  id                                = Column(Integer, primary_key=True, index=True)
  object_type                       = Column(String, nullable=False)
  object_name                       = Column(String, nullable=False)
  activity                          = Column(String, nullable=False)
  created_by                        = Column(String)
  created_at                        = Column(DateTime, default=datetime.now)
  
  object_id                         = Column(Integer, ForeignKey("tasks_activity.task_id"))
  object                            = orm.relationship('TaskActivity', back_populates='history')
  detail                            = orm.relationship('TaskHistoryDetail', back_populates='history')
  
class TaskHistoryDetail(Base):
  __tablename__                     = "tasks_history_detail"
  
  id                                = Column(Integer, primary_key=True, index=True)
  field_name                        = Column(String, nullable=False)
  previous_data_value               = Column(String, nullable=False)  
  latest_data_value                 = Column(String, nullable=False)  
  
  history_id                        = Column(Integer, ForeignKey("tasks_history.id"))
  history                           = orm.relationship('TaskHistory', back_populates='detail')