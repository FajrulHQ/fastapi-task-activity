# Task Activity FastAPI

### Description

This project demonstrates a CRUD (Create, Read, Update, Delete) and History capture in server application built with FastAPI and the official PostgreSQL. It allows you to manage a task, filter, sort, pagination query, and also track the history of the tasks.

### Models:
Represents a post with details below.

```py
class TaskActivityBase(BaseModel):
  task_name                         : Optional[str]
  task_description                  : Optional[str]
  activity_type_name                : Optional[str]
  activity_group_sub_category_name  : Optional[str]
  activity_group_name               : Optional[str]
  core_group_category               : Optional[str]
  status                            : Optional[str]
  ...
```

### Prerequisites:
- Python (version 3.7 or later)
- Local or Cloud PostgreSQL server

### Installation:
- Clone this repository.
- Install dependencies using `pip install -r requirements.txt`.
- Add file `.env` with these variables
```py
MAIN_DB_NAME=task-activity
MAIN_DB_USER=fajrulhaqqi
MAIN_DB_PASSWORD=inipassword
MAIN_DB_HOST=localhost
MAIN_DB_PORT=5432

SECRET_KEY=94a4b31fae13d6d2537b3e43b8a783ba15cecaddeffc3f327163c87cd4338bc0
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Running the Application:
- Compile and run the application: `python -m uvicorn app.main:app --host=0.0.0.0 --port=8080 --reload`

### API Endpoints:

#### Authentication
- `POST /auth/users`: Create user account using username and password.
- `GET /auth/user/me`: Retrieves an active user.
- `POST /auth/login`: Login an get an access token.

#### Task
- `GET /task`: Retrieve task activities.
- `GET /task/{id}`: Retrieve task activitiy by id.
- `GET /task?{column}={value}`: Filter task by value that contains in specific column.
- `GET /task?page={page}&size={size}`: Paginate list of task by page and size
- `GET /task?order={column}&sort={asc|desc}`: Sorting list of task by column and asc or desc method
- `POST /task` : Creates a new task. (Payload should be a JSON object representing the Task schema)
- `PUT /task/{id}`: Update status in existing task. (Payload should be a JSON object with updated status)
- `DELETE /task/{id}`: Deletes an existing task.
- `POST /notification`: Webhooks to send notification of created and modified task