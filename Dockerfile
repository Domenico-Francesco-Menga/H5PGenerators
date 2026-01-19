# Usa un'immagine base di Python
FROM python:3.10-slim

# Imposta la cartella di lavoro nel container
WORKDIR /app

# Copia il file dei requisiti e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del progetto
COPY . .

# Espone la porta su cui gira il tuo servizio REST (es. 5000, 8000 o 8080)
EXPOSE 5000 

CMD ["python", "Server.py"]
