# 🚀 Guide de Déploiement - Document Analyzer

## Option 1: Streamlit Community Cloud (GRATUIT - RECOMMANDÉ)

### Étape 1: Préparer GitHub

1. Allez sur https://github.com/new
2. Créez un nouveau repo appelé `doc-analyzer`
3. Laissez-le public
4. Cliquez "Create repository"

### Étape 2: Pousser le code

Ouvrez PowerShell dans le dossier du projet et exécutez:

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/doc-analyzer.git
git push -u origin main
```

*Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur GitHub*

### Étape 3: Configurer les secrets

1. Allez sur https://share.streamlit.io
2. Connectez-vous avec GitHub
3. Cliquez sur votre app ou "New app"
4. Repository: `doc-analyzer`
5. Branch: `main`
6. Main file path: `app.py`
7. Cliquez "Deploy"

8. **Une fois déployée**, ouvrez "Settings" → "Secrets"
9. Ajoutez votre clé API:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx
```

### Étape 4: Accéder à l'app

L'app sera accessible via: `https://doc-analyzer-[code-aléatoire].streamlit.app`

---

## Option 2: Déploiement sur Render

Le projet inclut un fichier `render.yaml` prêt à l'emploi.

### Étapes

1. Poussez le code vers GitHub.
2. Sur Render: **New +** → **Blueprint**.
3. Sélectionnez votre repository.
4. Render détecte automatiquement `render.yaml`.
5. Ajoutez la variable d'environnement suivante dans Render:
  - `OPENAI_API_KEY` = votre clé API OpenAI
6. Lancez le déploiement.

### Commandes configurées

- Build: `pip install -r requirements.txt`
- Start: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`

### Important

- Le disque Render est éphémère: les fichiers générés localement (résultats d'upload, exports Excel) peuvent être perdus après redémarrage.

---

## Option 3: Déploiement local persistant

Si vous avez un serveur toujours allumé, lancez:

```bash
streamlit run app.py --server.runOnSave true
```

---

## Remarques Importantes

### Pour le déploiement en ligne
- ⚠️ Ne commitez JAMAIS votre `API.env` (il est dans `.gitignore`)
- ✅ Utilisez TOUJOURS Streamlit Cloud Secrets pour stocker les clés
- ✅ Les utilisateurs doivent fournir le chemin du dossier dans l'app

### Limites de Streamlit Cloud
- RAM: ~1 GB
- Stockage: Limité (pas de stockage persistant des fichiers)
- Filesize: Max ~200MB par déploiement

### Coûts
- Streamlit Cloud: GRATUIT
- OpenAI API: Dépend de l'usage
  - ~$0.03 par 1000 tokens (GPT-4o)
  - Estimez ~$0.10-1 par document

---

## Vérifier si ça fonctionne

1. Allez sur votre app Streamlit
2. Entrez le chemin d'un dossier avec des PDFs/PPTXs
3. Cliquez "Upload"
4. Cliquez "Évaluer"
5. Attendez les résultats!

---

## Troubleshooting

**App ne démarre pas?**
- Vérifiez les logs sur Streamlit Cloud (Settings → Logs)
- Assurez-vous que `requirements.txt` est à jour

**Permission denied?**
- Le chemin du dossier doit être accessible depuis votre machine
- En cloud, utilisez un chemin relatif

**API Key invalide?**
- Vérifiez dans Streamlit Cloud (Settings → Secrets)
- Assurez-vous que c'est bien `OPENAI_API_KEY`

**Notes non détectées?**
- L'extraction de regex peut ne pas fonctionner avec tous les formats
- Vérifiez le format de réponse dans "Évaluation"
