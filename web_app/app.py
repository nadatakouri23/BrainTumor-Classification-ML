from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

app = Flask(__name__)

# Charger le modèle et le scaler
MODEL_PATH = os.path.join('models', 'best_model.pkl')
SCALER_PATH = os.path.join('models', 'scaler.pkl')

model = None
scaler = None

def load_model():
    """Charger le modèle et le scaler"""
    global model, scaler
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        print("✅ Modèle et scaler chargés avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle: {e}")
        return False

# Liste des features du modèle
FEATURE_NAMES = [
    'Gender', 'Age_at_diagnosis', 'Race_black or african american',
    'Race_white', 'IDH1', 'TP53', 'ATRX', 'PTEN', 'EGFR', 'CIC',
    'MUC16', 'PIK3CA', 'NF1', 'PIK3R1', 'FUBP1', 'RB1', 'NOTCH1',
    'BCOR', 'CSMD3', 'SMARCA4', 'GRIN2A', 'IDH2', 'FAT4', 'PDGFRA'
]

# Informations sur les gènes
GENE_INFO = {
    'IDH1': 'Isocitrate Dehydrogenase 1 - Marqueur pronostique majeur',
    'TP53': 'Tumor Protein P53 - Gène suppresseur de tumeur',
    'ATRX': 'Alpha-Thalassemia/Mental Retardation Syndrome X-Linked',
    'PTEN': 'Phosphatase and Tensin Homolog',
    'EGFR': 'Epidermal Growth Factor Receptor',
    'CIC': 'Capicua Transcriptional Repressor',
    'MUC16': 'Mucin 16 - Protéine de surface cellulaire',
    'PIK3CA': 'Phosphatidylinositol-4,5-Bisphosphate 3-Kinase',
    'NF1': 'Neurofibromin 1',
    'PIK3R1': 'Phosphoinositide-3-Kinase Regulatory Subunit 1',
    'FUBP1': 'Far Upstream Element Binding Protein 1',
    'RB1': 'Retinoblastoma 1',
    'NOTCH1': 'Notch Receptor 1',
    'BCOR': 'BCL6 Corepressor',
    'CSMD3': 'CUB and Sushi Multiple Domains 3',
    'SMARCA4': 'SWI/SNF Related Chromatin Remodeling Complex',
    'GRIN2A': 'Glutamate Ionotropic Receptor NMDA Type Subunit 2A',
    'IDH2': 'Isocitrate Dehydrogenase 2',
    'FAT4': 'FAT Atypical Cadherin 4',
    'PDGFRA': 'Platelet Derived Growth Factor Receptor Alpha'
}

@app.route('/')
def home():
    """Page d'accueil"""
    return render_template('index.html', genes=GENE_INFO)

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint pour faire une prédiction"""
    try:
        # Récupérer les données du formulaire
        data = request.get_json()
        
        # Créer un vecteur de features
        features = []
        
        # Gender (0 = Female, 1 = Male)
        features.append(1 if data['gender'] == 'male' else 0)
        
        # Age (sera normalisé)
        age = float(data['age'])
        features.append(age)
        
        # Race (One-Hot Encoding)
        race = data['race']
        features.append(1 if race == 'black' else 0)  # Race_black or african american
        features.append(1 if race == 'white' else 0)  # Race_white
        
        # Mutations génétiques (20 gènes)
        gene_mutations = [
            'IDH1', 'TP53', 'ATRX', 'PTEN', 'EGFR', 'CIC', 'MUC16', 'PIK3CA',
            'NF1', 'PIK3R1', 'FUBP1', 'RB1', 'NOTCH1', 'BCOR', 'CSMD3',
            'SMARCA4', 'GRIN2A', 'IDH2', 'FAT4', 'PDGFRA'
        ]
        
        for gene in gene_mutations:
            features.append(1 if data.get(gene, False) else 0)
        
        # Convertir en DataFrame pour préserver l'ordre des colonnes
        features_array = np.array(features).reshape(1, -1)
        features_df = pd.DataFrame(features_array, columns=FEATURE_NAMES)
        
        # Normaliser l'âge avec le scaler
        features_df['Age_at_diagnosis'] = scaler.transform(features_df[['Age_at_diagnosis']])
        
        # Faire la prédiction
        prediction = model.predict(features_df)[0]
        probability = model.predict_proba(features_df)[0]
        
        # Préparer la réponse
        result = {
            'prediction': 'GBM (Glioblastoma Multiforme)' if prediction == 1 else 'LGG (Low-Grade Glioma)',
            'prediction_class': int(prediction),
            'probability_lgg': float(probability[0]) * 100,
            'probability_gbm': float(probability[1]) * 100,
            'confidence': float(max(probability)) * 100,
            'interpretation': get_interpretation(prediction, max(probability))
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def get_interpretation(prediction, confidence):
    """Interpréter le résultat"""
    tumor_type = "GBM (Glioblastome)" if prediction == 1 else "LGG (Gliome de bas grade)"
    
    if confidence >= 0.9:
        confidence_level = "très élevée"
    elif confidence >= 0.75:
        confidence_level = "élevée"
    elif confidence >= 0.6:
        confidence_level = "modérée"
    else:
        confidence_level = "faible"
    
    interpretation = f"Le modèle prédit un {tumor_type} avec une confiance {confidence_level} ({confidence*100:.1f}%)."
    
    if prediction == 1:
        interpretation += " Le GBM est une tumeur agressive nécessitant une prise en charge urgente."
    else:
        interpretation += " Le LGG est une tumeur de croissance plus lente, mais nécessite un suivi régulier."
    
    return interpretation

@app.route('/api/info')
def api_info():
    """Informations sur l'API"""
    return jsonify({
        'model': 'Brain Tumor Classification (GBM vs LGG)',
        'version': '1.0',
        'features': FEATURE_NAMES,
        'genes': GENE_INFO
    })

if __name__ == '__main__':
    # Charger le modèle au démarrage
    if load_model():
        print("🚀 Démarrage du serveur Flask...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Impossible de démarrer le serveur sans modèle")
        print("📝 Veuillez d'abord exécuter save_model.py pour entraîner et sauvegarder le modèle")
