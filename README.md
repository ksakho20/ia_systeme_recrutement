# Système de Recrutement en Ligne avec IA

Ce projet est une application web complète permettant aux recruteurs de publier des offres et aux candidats de postuler en ligne. Une intelligence artificielle (IA) est utilisée pour analyser et classer automatiquement les candidatures en fonction des compétences, mots-clés et pertinence.

---

## 🚀 Fonctionnalités principales

- 👤 Espace candidat :
  - Inscription et connexion
  - Soumission de candidature
  - Visualisation des offres

- 🧑‍💼 Espace recruteur :
  - Création d’offres d’emploi
  - Visualisation et classement des candidatures par IA
  - Notification des candidats sélectionnés

- 📊 IA intégrée :
  - Analyse de fichiers JSON de candidatures
  - Matching entre offres et profils selon mots-clés et scores

---

## 🗂️ Structure du projet

mon_projet/
├── app.py # Point d’entrée de l’application Flask
├── app/
│ ├── routes.py # Définition des routes Flask
│ ├── models.py # Modèle de données
│ ├── offres.json # Offres d’emploi (JSON)
│ ├── candidatures.json # Candidatures (JSON)
│ ├── templates/ # Fichiers HTML (Jinja2)
│ ├── static/ # CSS, JS, images
│ └── uploads/ # (Facultatif) Uploads de fichiers


---

## 🧪 Lancer l'application localement

### 📦 Prérequis
- Python 3.10+
- Flask

### ▶️ Démarrage

```bash
pip install -r requirements.txt  # à créer si besoin
python app.py

L’application sera disponible sur http://127.0.0.1:5000/.
📁 Données simulées

Les candidatures et offres sont stockées dans :

    candidatures.json

    offres.json

L’IA lit ces fichiers pour effectuer un classement automatique.
📬 Contact

Projet réalisé par Kaba Sakho – Étudiant en informatique
GitHub du projet
✅ TODO futur

    🔐 Ajouter l’authentification sécurisée (JWT ou sessions)

    📥 Intégrer l’upload de CV (PDF)

    📈 Ajouter des statistiques d’offres et de candidatures