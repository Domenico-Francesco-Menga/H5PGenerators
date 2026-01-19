FROM python:3.10-slim

WORKDIR /app

# Installiamo uvicorn esplicitamente oltre ai tuoi requisiti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt uvicorn

COPY . .

# FastAPI di default gira spesso sulla 8000, ma la mappiamo sulla 5000 come volevi
EXPOSE 5000

# Usiamo uvicorn per far girare l'app FastAPI
# --host 0.0.0.0 è fondamentale per Docker
# --port 5000 mappa la porta interna
CMD ["uvicorn", "Server:app", "--host", "0.0.0.0", "--port", "5000"]
