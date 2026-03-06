import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Charger les variables d'environnement
load_dotenv("API.env")

# Initialiser le client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuration
DOCUMENTS_FOLDER = r"C:\Users\hp\Downloads\Documents a analyser"
ALLOWED_EXTENSIONS = {".pdf", ".pptx"}

def get_documents(folder_path):
    """
    Récupère tous les fichiers PDF et PPTX d'un dossier.
    
    Args:
        folder_path (str): Chemin du dossier à analyser
        
    Returns:
        list: Liste des chemins des fichiers trouvés
    """
    documents = []
    
    if not os.path.exists(folder_path):
        print(f"❌ Le dossier n'existe pas: {folder_path}")
        return documents
    
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            
            # Vérifier si c'est un fichier (pas un dossier)
            if os.path.isfile(file_path):
                file_ext = Path(file).suffix.lower()
                
                # Vérifier l'extension
                if file_ext in ALLOWED_EXTENSIONS:
                    documents.append(file_path)
        
        return sorted(documents)
    
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du dossier: {e}")
        return documents

def upload_document(file_path):
    """
    Upload un seul document sur l'API OpenAI.
    
    Args:
        file_path (str): Chemin du fichier à uploader
        
    Returns:
        dict: Informations du fichier uploadé ou None en cas d'erreur
    """
    try:
        file_name = os.path.basename(file_path)
        
        with open(file_path, "rb") as f:
            response = client.files.create(
                file=(file_name, f),
                purpose="assistants"
            )
        
        return {
            "file_name": file_name,
            "file_id": response.id,
            "status": "✅ Succès"
        }
    
    except FileNotFoundError:
        return {
            "file_name": os.path.basename(file_path),
            "file_id": None,
            "status": f"❌ Fichier introuvable"
        }
    
    except Exception as e:
        return {
            "file_name": os.path.basename(file_path),
            "file_id": None,
            "status": f"❌ Erreur: {str(e)}"
        }

def batch_upload(folder_path):
    """
    Upload tous les documents PDF et PPTX d'un dossier.
    
    Args:
        folder_path (str): Chemin du dossier contenant les documents
    """
    print("=" * 60)
    print("🚀 UPLOAD EN BATCH - DOCUMENTS PDF ET PPTX")
    print("=" * 60)
    
    # Récupérer les documents
    documents = get_documents(folder_path)
    
    if not documents:
        print(f"⚠️  Aucun fichier PDF ou PPTX trouvé dans: {folder_path}")
        return
    
    print(f"\n📁 Dossier: {folder_path}")
    print(f"📄 Fichiers trouvés: {len(documents)}\n")
    
    # Uploader les documents
    results = []
    for file_path in tqdm(documents, desc="Upload en cours", unit="fichier"):
        result = upload_document(file_path)
        results.append(result)
        
        # Afficher le résultat pour chaque fichier
        print(f"{result['status']} - {result['file_name']}")
        if result['file_id']:
            print(f"   ID du fichier: {result['file_id']}")
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    successful = sum(1 for r in results if r['file_id'] is not None)
    failed = len(results) - successful
    
    print(f"✅ Succès: {successful}/{len(results)}")
    print(f"❌ Échecs: {failed}/{len(results)}")
    
    if failed > 0:
        print("\nFichiers avec erreur:")
        for r in results:
            if r['file_id'] is None:
                print(f"  - {r['file_name']}: {r['status']}")
    
    # Sauvegarder les résultats
    save_results(results)

def save_results(results):
    """
    Sauvegarde les résultats dans un fichier texte.
    
    Args:
        results (list): Liste des résultats d'upload
    """
    try:
        output_file = "upload_results.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("RÉSULTATS DE L'UPLOAD EN BATCH\n")
            f.write("=" * 60 + "\n\n")
            
            for result in results:
                f.write(f"Fichier: {result['file_name']}\n")
                f.write(f"Statut: {result['status']}\n")
                if result['file_id']:
                    f.write(f"ID: {result['file_id']}\n")
                f.write("\n")
        
        print(f"\n💾 Résultats sauvegardés dans: {output_file}")
    
    except Exception as e:
        print(f"\n⚠️  Erreur lors de la sauvegarde des résultats: {e}")

if __name__ == "__main__":
    batch_upload(DOCUMENTS_FOLDER)
