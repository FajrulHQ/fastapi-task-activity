from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from fastapi import Query

ActivityTypeNameEnum                = ["Tasks", "Email", "Chats", "Notes", "Meetings", "Calls", "Logs"]
ActivityGroupSubCategoryNameEnum    = ["Customer Contact", "Partner Contact", "Employee Contact"]
ActivityGroupNameEnum               = ["Contact", "Engagement", "Products", "Partners", "Quotes", "Notes", "Stage History", "Approval History", "Files"]
CoreGroupCategoryEnum               = ["Contacts", "Leads", "Opportunity", "Customers"]
StageNameEnum                       = ["New", "Proposal Creation", "Presentation", "Negotiation", "Closed", "Mark As Completed"]
StatusEnum                          = ["Not Started", "In Progress", "Completed", "Waiting on", "Differed"]
  
class TaskActivityBase(BaseModel):
  task_name                         : Optional[str] = None
  task_description                  : Optional[str] = None
  activity_type_name                : Optional[Literal[*ActivityTypeNameEnum]] = None
  activity_group_sub_category_name  : Optional[Literal[*ActivityGroupSubCategoryNameEnum]] = None
  activity_group_name               : Optional[Literal[*ActivityGroupNameEnum]] = None
  core_group_category               : Optional[Literal[*CoreGroupCategoryEnum]] = None
  status                            : Optional[Literal[*StatusEnum]] = None
  
TaskActivityColumns = list(TaskActivityBase.__fields__.keys())
                             
class TaskActivityParams(TaskActivityBase):
  order                             : Optional[Literal[*TaskActivityColumns]] = None
  sort                              : Literal['asc','desc'] = 'asc'
  page                              : Optional[int] = Query(1, ge=1)
  size                              : Optional[int] = Query(10, ge=1, le=100)
  
class TaskActivity(TaskActivityBase):
  task_id                           : int
  created_by                        : str
  created_at                        : datetime
  modified_by                       : str
  modified_at                       : datetime
  
class TaskHistory(BaseModel):
  object_id                         : int
  object_type                       : Literal[*TaskActivityColumns]
  object_name                       : str
  activity                          : Literal[*StatusEnum]
  created_by                        : str
  created_at                        : datetime
  
class TaskHistoryDetail(BaseModel):
  history_id                        : int
  field_name                        : str
  previous_data_value               : str
  latest_data_value                 : str

class TaskActivityUpdate(BaseModel):
  id                                : Optional[int] = None
  status                            : Literal[*StatusEnum]
  
class TaskNotification(BaseModel):
  category                          : Optional[str] = ""
  object_type                       : Optional[str] = ""
  object_name                       : Optional[str] = ""
  action                            : Optional[str] = ""
  event                             : Optional[str] = ""
  