FROM python:3.12.10-slim

WORKDIR /app

COPY requiremnets.txt

RUN pip install --no-cache-dir -r requiremnets.txt

COPY . . 

ENV PORT = 8000

CMD ["uvicorn" , "app.main:app" ,"--host" , "0.0.0.0","--port","8000"]