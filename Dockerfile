#!/bin/bash

# Utiliser une image de base officielle pour Python
FROM python:3.11-slim-bullseye

# Definir le dossier de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements et le reste du dossier
COPY requirements.txt requirements.txt
COPY . .

# Installer les dépendances
RUN apt-get update && apt-get install -y
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

ENV TOKEN = ""

# Exposer le port que streamlit utilisera
EXPOSE 8501

# Commande à exécuter pour démarrer l'application
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]