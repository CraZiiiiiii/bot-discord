# Utiliser une image Python légère
FROM python:3.10-slim

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY CodePython.py .

# Installer les dépendances
# Note : Je recommande de vérifier que 'dotenv' est bien 'python-dotenv' dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Commande de lancement
CMD ["python", "CodePython.py"]
