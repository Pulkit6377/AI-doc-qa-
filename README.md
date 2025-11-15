# AI-Powered Document Q&A System
### Python • FastAPI • MongoDB • Groq/OpenAI • Docker

This project is an AI-driven backend application that allows users to:

- Upload documents (text/PDF)

- Store extracted content in MongoDB

- Ask questions related to uploaded documents

- Receive answers using LLMs (Groq/OpenAI)

- Run everything inside Docker



## Features

- Document upload API

- MongoDB storage

- Query API powered by LLM

- Modular FastAPI backend

- Fully containerized with Docker





## Project Structure
```bash
AI-DOC-QA/
│
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── utils.py
│   └── routes/
│       ├── upload.py
│       └── query.py
│
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```




## Tech Stack
Layer	Technology
Backend	FastAPI
Language	Python 3.10+
Database	MongoDB
AI Model	Groq/OpenAI API
Containerization	Docker
Tools	Uvicorn, Pydantic




## Setup Instructions
### Clone repo
```bash
git clone https://github.com/YOUR_USERNAME/AI-DOC-QA.git
cd AI-DOC-QA
```

### Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # mac/linux
venv\Scripts\activate     # windows
```

```bash
Install dependencies
pip install -r requirements.txt
```

 Add your .env
MONGO_URI=mongodb+srv://your...
GROQ_API_KEY=your-key

5️⃣ Start FastAPI
uvicorn app.main:app --reload


Visit Swagger UI:
👉 http://localhost:8000/docs


🐳 Run with Docker
Build image
docker build -t ai-doc-qa .

Run container
docker run -p 8000:8000 ai-doc-qa

🧠 How It Works

User uploads document via /upload

Content gets stored in MongoDB

User asks a question via /query

Backend:

Fetches document content

Sends context + question → Groq/OpenAI

Returns an accurate answer

📌 API Endpoints
POST /upload

Upload document content.

POST /query

Ask a question related to uploaded documents.
