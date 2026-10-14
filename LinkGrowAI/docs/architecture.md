# Architecture

LinkGrow AI is a modular Flask application.

```mermaid
flowchart LR
    User["Student or job seeker"] --> UI["Bootstrap UI"]
    UI --> Routes["Flask routes"]
    Routes --> Services["Profile, content, networking, analytics, agent services"]
    Routes --> DB["SQLAlchemy database"]
    ML["ML pipeline"] --> Artifacts["joblib artifacts"]
    Services --> ML
```

The local development database is SQLite. MySQL can be used by setting `DATABASE_URL`, for example `mysql+pymysql://user:password@localhost/linkgrow_ai`.
