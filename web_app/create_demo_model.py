"""
Script de création d'un modèle de démonstration
Crée un modèle simple pour tester l'application web sans avoir besoin du dataset complet
"""

import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import os

def create_demo_model():
    """Crée un modèle de démonstration avec des données synthétiques"""
    print("="*80)
    print("🎭 CRÉATION D'UN MODÈLE DE DÉMONSTRATION")
    print("="*80)
    print("⚠️  Note: Ce modèle est uniquement pour tester l'interface web")
    print("    Pour une utilisation réelle, utilisez save_model.py avec vos données\n")
    
    # Créer le dossier models
    os.makedirs('models', exist_ok=True)
    
    # Générer des données synthétiques pour l'entraînement
    print("📊 Génération de données synthétiques...")
    np.random.seed(42)
    
    # 24 features: Gender, Age, 2 Race features, 20 gene mutations
    n_samples = 500
    X = np.random.rand(n_samples, 24)
    
    # Créer une cible corrélée (GBM plus probable avec certaines mutations)
    y = (X[:, 4] + X[:, 5] + X[:, 6] > 1.5).astype(int)  # IDH1, TP53, ATRX
    
    # Créer et entraîner le modèle
    print("🤖 Entraînement du modèle de démonstration...")
    model = RandomForestClassifier(
        n_estimators=50,
        max_depth=5,
        random_state=42
    )
    model.fit(X, y)
    
    # Créer le scaler
    print("📏 Création du scaler...")
    scaler = MinMaxScaler()
    scaler.fit(np.array([[0], [100]]))  # Age de 0 à 100 ans
    
    # Sauvegarder
    print("\n💾 Sauvegarde des fichiers...")
    with open('models/best_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("✅ Modèle sauvegardé: models/best_model.pkl")
    
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print("✅ Scaler sauvegardé: models/scaler.pkl")
    
    # Sauvegarder les noms de features
    feature_names = [
        'Gender', 'Age_at_diagnosis', 'Race_black or african american',
        'Race_white', 'IDH1', 'TP53', 'ATRX', 'PTEN', 'EGFR', 'CIC',
        'MUC16', 'PIK3CA', 'NF1', 'PIK3R1', 'FUBP1', 'RB1', 'NOTCH1',
        'BCOR', 'CSMD3', 'SMARCA4', 'GRIN2A', 'IDH2', 'FAT4', 'PDGFRA'
    ]
    
    with open('models/feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    print("✅ Features sauvegardées: models/feature_names.pkl")
    
    print("\n" + "="*80)
    print("✅ MODÈLE DE DÉMONSTRATION CRÉÉ AVEC SUCCÈS!")
    print("="*80)
    print("🚀 Vous pouvez maintenant lancer l'application:")
    print("   python app.py")
    print("\n⚠️  RAPPEL: Ce modèle est UNIQUEMENT pour tester l'interface")
    print("   Pour une utilisation réelle avec vos données:")
    print("   1. Placez votre fichier CSV dans le dossier")
    print("   2. Exécutez: python save_model.py")
    print("="*80)

if __name__ == "__main__":
    create_demo_model()
