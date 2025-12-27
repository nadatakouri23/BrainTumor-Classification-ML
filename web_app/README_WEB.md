# 🚀 Déploiement de l'Application Web

## Instructions de démarrage

### 1. Installation des dépendances
```bash
cd web_app
pip install -r requirements.txt
```

### 2. Entraîner et sauvegarder le modèle
```bash
python save_model.py
```
⚠️ Assurez-vous que le fichier `TCGA_GBM_LGG_Mutations_all.csv` est accessible.

### 3. Lancer l'application Flask
```bash
python app.py
```

### 4. Accéder à l'application
Ouvrez votre navigateur et allez sur: **http://localhost:5000**

---

## Structure du projet web
```
web_app/
│
├── app.py                 # Application Flask principale
├── save_model.py          # Script pour entraîner et sauvegarder le modèle
├── requirements.txt       # Dépendances Python
│
├── models/               # Modèles sauvegardés
│   ├── best_model.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
│
├── templates/            # Templates HTML
│   └── index.html
│
└── static/              # Fichiers statiques
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

---

## Utilisation de l'interface

1. **Remplir les informations démographiques** : Âge, genre, origine ethnique
2. **Sélectionner les mutations génétiques** : Cocher les gènes mutés
3. **Cliquer sur "Analyser"** : Le modèle fait la prédiction
4. **Consulter les résultats** :
   - Type de tumeur prédit (GBM ou LGG)
   - Niveau de confiance
   - Distribution des probabilités
   - Interprétation clinique

---

## Déploiement en production

### Option 1: Heroku
```bash
# Créer un Procfile
echo "web: python app.py" > Procfile

# Déployer
heroku create your-app-name
git push heroku main
```

### Option 2: Railway
1. Connecter votre repository GitHub
2. Railway détectera automatiquement Flask
3. L'application sera déployée automatiquement

### Option 3: PythonAnywhere
1. Upload des fichiers via l'interface web
2. Configurer le WSGI file
3. Reload l'application

---

## API Endpoints

- `GET /` - Page d'accueil
- `POST /predict` - Faire une prédiction
- `GET /api/info` - Informations sur l'API

---

## Sécurité

⚠️ **Important** : Cette application est à usage académique/démonstratif uniquement.
Ne pas utiliser en production sans :
- Authentification utilisateur
- Chiffrement HTTPS
- Validation médicale professionnelle
- Conformité RGPD/HIPAA
