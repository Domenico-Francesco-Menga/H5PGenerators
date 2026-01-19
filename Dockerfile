# Usa un'immagine base di Python
FROM python:3.10-slim

# Imposta la cartella di lavoro nel container
WORKDIR /app

# Copia il file dei requisiti e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del progetto
COPY . .

# Comando per avviare l'applicazione (cambia main.py col tuo file)
CMD ["python", "main.py"]
