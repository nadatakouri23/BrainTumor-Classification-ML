"""
Script alternatif: Importer le modèle depuis le notebook Jupyter

Si vous avez déjà exécuté le notebook et entraîné vos modèles,
ce script peut vous aider à les exporter pour l'application web.

INSTRUCTIONS:
1. Ouvrez votre notebook Copie_de_Untitled39.ipynb
2. À la fin du notebook, ajoutez une nouvelle cellule avec ce code:

```python
import pickle
import os

# Créer le dossier models s'il n'existe pas
os.makedirs('web_app/models', exist_ok=True)

# Sauvegarder le meilleur modèle (remplacez 'xgb' par votre meilleur modèle)
# Options: lr, dt, knn, rf, xgb ou tuned_models['XGBoost'], etc.
best_model = xgb  # ou tuned_models['XGBoost'] si vous avez fait le fine-tuning

with open('web_app/models/best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

# Sauvegarder le scaler
with open('web_app/models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Modèle et scaler sauvegardés dans web_app/models/")
```

3. Exécutez cette cellule
4. Revenez lancer l'application: python app.py
"""

print(__doc__)
