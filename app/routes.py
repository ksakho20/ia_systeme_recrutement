import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == 'admin@test.com' and password == '123':
            session['user_id'] = email
            session['user_role'] = 'recruteur'
            flash("Connexion réussie !")
            return redirect(url_for('main.dashboard'))

        elif email == 'user@test.com' and password == '123':
            session['user_id'] = email
            session['user_role'] = 'candidat'
            flash("Connexion réussie !")
            return redirect(url_for('main.dashboard'))

        else:
            flash("Identifiants incorrects.")

    return render_template('connexion.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash("Inscription fictive réussie.")
        return redirect(url_for('main.login'))
    return render_template('inscription.html')

@bp.route('/ajouter-offre', methods=['GET', 'POST'])
def ajouter_offre():
    if 'user_id' not in session or session.get('user_role') != 'recruteur':
        flash("Accès réservé aux recruteurs.")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        competences = request.form['competences']

        chemin_fichier = os.path.join('app', 'offres.json')
        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, 'r') as f:
                offres = json.load(f)
        else:
            offres = []

        nouvelle_offre = {
            "id": len(offres),  # identifiant unique par index
            "titre": titre,
            "description": description,
            "competences": competences,
            "auteur": session['user_id']
        }

        offres.append(nouvelle_offre)

        with open(chemin_fichier, 'w') as f:
            json.dump(offres, f, indent=4)

        flash(f"L’offre « {titre} » a été publiée.")
        return redirect(url_for('main.dashboard'))

    return render_template('ajouter-offre.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash("Déconnecté.")
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    if session.get('user_role') == 'candidat':
        return render_template('candidat.html')
    else:
        return render_template('recruteur.html')




@bp.route('/candidature/<int:offre_id>', methods=['GET', 'POST'])
def candidature(offre_id):
    if 'user_id' not in session or session.get('user_role') != 'candidat':
        flash("Accès réservé aux candidats.")
        return redirect(url_for('main.login'))

    # Charger l'offre depuis offres.json
    chemin = os.path.join('app', 'offres.json')
    if not os.path.exists(chemin):
        return "Aucune offre", 404

    with open(chemin, 'r') as f:
        offres = json.load(f)

    offre = next((o for o in offres if o['id'] == offre_id), None)
    if not offre:
        return "Offre introuvable", 404

    if request.method == 'POST':
        cv = request.files['cv']
        lettre = request.files['lettre']
        
        cv_text     = extract_text_from_upload(cv)
        lettre_text = extract_text_from_upload(lettre)

        competences = offre['competences'].lower()

        score = len(set(cv_text.split()) & set(competences.split())) * 10
        if score > 100:
            score = 100

        # Sauvegarde la candidature
        candidature = {
            "offre_id": offre_id,
            "candidat": session['user_id'],
            "score": score
        }

        chemin_candidatures = os.path.join('app', 'candidatures.json')
        if os.path.exists(chemin_candidatures):
            with open(chemin_candidatures, 'r') as f:
                candidatures = json.load(f)
        else:
            candidatures = []

        candidatures.append(candidature)

        with open(chemin_candidatures, 'w') as f:
            json.dump(candidatures, f, indent=4)

        flash(f"Candidature soumise avec succès ! Score IA : {score} %")
        return redirect(url_for('main.dashboard'))


    return render_template('soumettre-candidature.html', offre=offre)


@bp.route('/voir-candidatures')
def voir_candidatures():
    if 'user_id' not in session or session.get('user_role') != 'recruteur':
        flash("Accès interdit.")
        return redirect(url_for('main.index'))

    chemin_offres = os.path.join('app', 'offres.json')
    chemin_candidats = os.path.join('app', 'candidatures.json')

    if not os.path.exists(chemin_offres) or not os.path.exists(chemin_candidats):
        return render_template('candidats_offre.html', resultats=[])

    with open(chemin_offres, 'r') as f:
        offres = json.load(f)

    with open(chemin_candidats, 'r') as f:
        candidatures = json.load(f)

    # Filtrer les candidatures pour les offres de ce recruteur
    resultats = []
    for offre in offres:
        if offre['auteur'] == session['user_id']:
            cands = [c for c in candidatures if c['offre_id'] == offre['id']]
            cands.sort(key=lambda x: x['score'], reverse=True)
            resultats.append({
                "offre": offre['titre'],
                "candidatures": cands
            })

    return render_template('candidats_offre.html', resultats=resultats)

@bp.route('/notifications')
def notifications():
    if 'user_id' not in session or session.get('user_role') != 'candidat':
        flash("Accès réservé aux candidats.")
        return redirect(url_for('main.index'))

    chemin_candidatures = os.path.join('app', 'candidatures.json')
    chemin_offres = os.path.join('app', 'offres.json')

    if not os.path.exists(chemin_candidatures) or not os.path.exists(chemin_offres):
        return render_template('notifications.html', candidatures=[])

    with open(chemin_candidatures, 'r') as f:
        candidatures = json.load(f)

    with open(chemin_offres, 'r') as f:
        offres = json.load(f)

    # Filtrer les candidatures du candidat connecté
    mes_candidatures = []
    for c in candidatures:
        if c['candidat'] == session['user_id']:
            offre = next((o for o in offres if o['id'] == c['offre_id']), None)
            mes_candidatures.append({
            "titre": offre['titre'] if offre else "Offre supprimée",
            "score": c['score']
        })


    return render_template('notifications.html', candidatures=mes_candidatures)

@bp.route('/offres')
def offres():
    chemin = os.path.join('app', 'offres.json')
    with open(chemin, 'r') as f:
        offres = json.load(f)

    # S’assurer que chaque offre a un id
    for idx, offre in enumerate(offres):
        if 'id' not in offre:
            offre['id'] = idx

    # Simuler score IA
    for offre in offres:
        offre['score_ia'] = f"{50 + hash(offre['titre']) % 50}%"

    return render_template('liste_offres.html', offres=offres)


import io
from PyPDF2 import PdfReader

def extract_text_from_upload(uploaded_file):
    filename = uploaded_file.filename.lower()
    data = uploaded_file.read()
    # Si c’est un PDF, on utilise PyPDF2
    if filename.endswith('.pdf'):
        reader = PdfReader(io.BytesIO(data))
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return "\n".join(text).lower()
    # Sinon on essaie du texte UTF-8 et on ignore les erreurs
    try:
        return data.decode('utf-8').lower()
    except UnicodeDecodeError:
        return data.decode('utf-8', errors='ignore').lower()
