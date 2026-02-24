# Interactive Product Analytics Dashboard - Backend

A high-performance FastAPI backend for tracking user interactions and providing real-time analytics. This project features JWT-based authentication, demographic-based filtering, and a managed Neon PostgreSQL database.

## 🚀 Features

- **User Authentication:** Secure registration and login using JWT (JSON Web Tokens).
- **Event Tracking:** Lightweight endpoint to record feature interactions in real-time.
- **Advanced Analytics:** 
  - Aggregated click counts per feature.
  - Daily interaction trends (line charts).
  - Dynamic filtering by date range, age group, and gender.
- **Cloud Database:** Integrated with Neon DB for managed PostgreSQL persistence.
- **Data Seeding:** Automated script to generate realistic users and tracking events.

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL (Neon)
- **Security:** Jose (JWT), Passlib (Bcrypt)
- **Data Generation:** Faker

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd PythonProject6
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Unix/macOS:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add the following:
```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=your_host
POSTGRES_PORT=5432
POSTGRES_DB=your_db
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

### 5. Initialize & Seed Database
```bash
python seed.py
```

### 6. Run the Application
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`. Documentation (Swagger UI) is available at `http://localhost:8000/docs`.

## 🌐 Deployment (Render)

To deploy this project successfully on Render:

1.  **Using Blueprint (Recommended):**
    - Connect your GitHub repository to Render.
    - Render will automatically detect the `render.yaml` file and configure the service.
2.  **Manual Configuration:**
    - **Service Type:** Web Service
    - **Runtime:** Python
    - **Build Command:** `pip install -r requirements.txt`
    - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
    - **Environment Variables:**
        - `DATABASE_URL`: Your Neon DB connection string.
        - `SECRET_KEY`: A random strong secret.
        - `ALGORITHM`: `HS256`
        - `ACCESS_TOKEN_EXPIRE_MINUTES`: `60`
        - `BACKEND_CORS_ORIGINS`: `["*"]` (or specific frontend URLs)

---

## 📡 API Endpoints

### Authentication
- `POST /auth/register`: Create a new user account.
- `POST /auth/login`: Authenticate and receive an access token.

### Tracking
- `POST /track/`: Record a feature interaction (Requires Auth).

### Analytics
- `GET /analytics/`: Retrieve aggregated data with optional filters:
  - `start_date`, `end_date`: Filter by timeframe.
  - `age_group`: Filter by demographic (`<18`, `18-40`, `>40`).
  - `gender`: Filter by gender (`male`, `female`, `other`).
  - `feature_name`: Focus on a specific feature for trend analysis.

### System
- `GET /health`: Basic service health check.

## 🗄️ Database Schema

The project uses two main tables:
1. `users`: Stores user credentials and basic demographic info (age, gender).
2. `feature_clicks`: Stores every interaction, linked to a user and timestamped.
