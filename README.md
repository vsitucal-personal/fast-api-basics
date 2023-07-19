# fast-api-basics
Fast API Introduction

**Local Setup**

```

To run the app locally on host `0.0.0.0` port `8000`:

```$ uvicorn app:app --host 0.0.0.0 --port 8000```

---
**Setup Docker Containerization**

NOTE : Make sure to have installed docker Desktop in your machine

From your local repository code root folder, run this command

(1) Initial run

```docker-compose up -d```

(2) Rebuilding container

```docker-compose up --build -d```

To stop and remove the container

```docker-compose down```
```
---
API DOCS:

http://127.0.0.1:8000/docs#/