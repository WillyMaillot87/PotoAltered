#!/bin/bash

# Utiliser une image de base officielle pour Python
FROM python:3.11-slim-bullseye

# Definir le dossier de travail dans le conteneur
WORKDIR /app

RUN mkdir /app/data

VOLUME /app/data

# Copier le fichier requirements et le reste du dossier
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY get_cards_data.py get_cards_data.py
COPY get_collection_data.py get_collection_data.py
COPY get_card_images.py get_card_images.py
COPY get_csv_data.py get_csv_data.py
COPY get_csv_collection.py get_csv_collection.py
COPY get_all_data.py get_all_data.py
COPY utils.py utils.py
COPY run_all.sh run_all.sh
COPY PotoAltered.png PotoAltered.png

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