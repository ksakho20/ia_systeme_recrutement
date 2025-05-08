from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Offre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    competences_requises = db.Column(db.Text)
    recruteur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))

class Candidature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidat_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    offre_id = db.Column(db.Integer, db.ForeignKey('offre.id'))
    cv_filename = db.Column(db.String(200))
    lettre_filename = db.Column(db.String(200))
    score = db.Column(db.Float)
    statut = db.Column(db.String(20), default='en cours')
    date_soumission = db.Column(db.DateTime, default=datetime.utcnow)

    offre = db.relationship("Offre", backref="candidatures")
