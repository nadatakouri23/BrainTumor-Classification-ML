"""
Script pour entraîner et sauvegarder le meilleur modèle
À exécuter après avoir complété le notebook Jupyter

Ce script:
1. Charge et prépare les données
2. Entraîne le meilleur modèle (à ajuster selon vos résultats)
3. Sauvegarde le modèle et le scaler pour l'application web
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data(filepath):
    """Charge et prépare les données"""
    print("📥 Chargement des données...")
    df = pd.read_csv(filepath)
    print(f"✅ Dataset chargé: {df.shape[0]} lignes, {df.shape[1]} colonnes")
    
    # Conversion de l'âge
    def age_to_years(age_str):
        if age_str == "--":
            return 0
        age_str = str(age_str)
        parts = age_str.split(' ')
        years = int(parts[0])
        days = 0
        if len(parts) >= 4 and parts[3].lower() == 'days':
            days = int(parts[2])
        return years + days/365
    
    print("🔄 Conversion de l'âge...")
    df['Age_at_diagnosis'] = df['Age_at_diagnosis'].apply(age_to_years)
    df['Age_at_diagnosis'] = df['Age_at_diagnosis'].astype(int)
    
    # Encodage du genre
    print("🔄 Encodage du genre...")
    df['Gender'] = df['Gender'].replace('--', np.nan)
    df = df.dropna(subset=['Gender'])
    label_encoder = LabelEncoder()
    df['Gender'] = label_encoder.fit_transform(df['Gender'])
    
    # Suppression des colonnes inutiles
    print("🗑️ Suppression des colonnes inutiles...")
    df = df.drop('Primary_Diagnosis', axis=1, errors='ignore')
    df = df.drop(['Case_ID', 'Project'], axis=1, errors='ignore')
    
    # Gestion de la race
    print("🔄 Encodage de la race...")
    df = df[df['Race'] != 'not reported']
    df = pd.get_dummies(df, columns=['Race'], drop_first=True)
    
    # Encodage des mutations
    print("🔄 Encodage des mutations génétiques...")
    mutation_cols = ['IDH1','TP53','ATRX','PTEN','EGFR','CIC','MUC16','PIK3CA',
                     'NF1','PIK3R1','FUBP1','RB1','NOTCH1','BCOR','CSMD3','SMARCA4',
                     'GRIN2A','IDH2','FAT4','PDGFRA']
    
    for col in mutation_cols:
        if col in df.columns:
            df[col] = df[col].map({'MUTATED': 1, 'NOT_MUTATED': 0})
    
    # Encodage de la variable cible
    print("🔄 Encodage de la variable cible...")
    df['Grade'] = df['Grade'].map({'LGG': 0, 'GBM': 1})
    
    print(f"✅ Préparation terminée: {df.shape[0]} lignes, {df.shape[1]} colonnes")
    return df

def train_and_save_model(df, model_type='xgboost'):
    """Entraîne et sauvegarde le modèle"""
    print(f"\n🤖 Entraînement du modèle {model_type}...")
    
    # Séparation des features et de la cible
    X = df.drop('Grade', axis=1)
    y = df['Grade']
    
    print(f"📊 Features: {X.shape[1]} variables")
    print(f"📊 Distribution cible - LGG: {sum(y==0)}, GBM: {sum(y==1)}")
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Normalisation de l'âge
    print("🔄 Normalisation de l'âge...")
    scaler = MinMaxScaler()
    X_train['Age_at_diagnosis'] = scaler.fit_transform(X_train[['Age_at_diagnosis']])
    X_test['Age_at_diagnosis'] = scaler.transform(X_test[['Age_at_diagnosis']])
    
    # Entraînement du modèle
    if model_type == 'xgboost':
        print("⚙️ Entraînement XGBoost...")
        model = XGBClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
            eval_metric='logloss'
        )
    elif model_type == 'random_forest':
        print("⚙️ Entraînement Random Forest...")
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=5,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
    else:
        raise ValueError(f"Type de modèle non supporté: {model_type}")
    
    model.fit(X_train, y_train)
    
    # Évaluation
    print("\n📈 Évaluation du modèle...")
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    print(f"Accuracy Train: {accuracy_score(y_train, y_pred_train):.4f}")
    print(f"Accuracy Test:  {accuracy_score(y_test, y_pred_test):.4f}")
    print(f"Precision Test: {precision_score(y_test, y_pred_test):.4f}")
    print(f"Recall Test:    {recall_score(y_test, y_pred_test):.4f}")
    print(f"F1-Score Test:  {f1_score(y_test, y_pred_test):.4f}")
    
    # Sauvegarde du modèle et du scaler
    print("\n💾 Sauvegarde du modèle...")
    with open('models/best_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("✅ Modèle sauvegardé dans models/best_model.pkl")
    print("✅ Scaler sauvegardé dans models/scaler.pkl")
    
    # Sauvegarde des noms de features
    feature_names = X.columns.tolist()
    with open('models/feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    
    print("✅ Noms des features sauvegardés dans models/feature_names.pkl")
    
    return model, scaler

def main():
    """Fonction principale"""
    print("="*80)
    print("🧠 ENTRAÎNEMENT ET SAUVEGARDE DU MODÈLE DE CLASSIFICATION")
    print("="*80)
    
    # Chemin du dataset (à ajuster selon votre configuration)
    # Option 1: Chemin local dans le dossier parent
    dataset_path = "../TCGA_GBM_LGG_Mutations_all.csv"
    
    # Option 2: Si le fichier est dans le même dossier que le script
    if not os.path.exists(dataset_path):
        dataset_path = "TCGA_GBM_LGG_Mutations_all.csv"
    
    # Option 3: Demander à l'utilisateur
    if not os.path.exists(dataset_path):
        print("\n⚠️ Le fichier dataset n'a pas été trouvé automatiquement.")
        print("📝 Veuillez entrer le chemin complet du fichier CSV:")
        print("   Exemple: C:\\Users\\ranim\\Downloads\\TCGA_GBM_LGG_Mutations_all.csv")
        dataset_path = input("\nChemin du fichier: ").strip().strip('"')
    
    try:
        # Charger et préparer les données
        df = load_and_prepare_data(dataset_path)
        
        # Entraîner et sauvegarder le modèle
        # Vous pouvez choisir 'xgboost' ou 'random_forest'
        model, scaler = train_and_save_model(df, model_type='xgboost')
        
        print("\n" + "="*80)
        print("✅ PROCESSUS TERMINÉ AVEC SUCCÈS!")
        print("="*80)
        print("🚀 Vous pouvez maintenant lancer l'application web avec: python app.py")
        
    except FileNotFoundError:
        print(f"\n❌ Erreur: Le fichier {dataset_path} n'a pas été trouvé")
        print("📝 Veuillez ajuster le chemin dans la variable 'dataset_path'")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
