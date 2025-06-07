import os
import requests
import random

# URLs des images de casquettes
CAP_IMAGES = [
    "https://images.unsplash.com/photo-1521369909029-2afed882baee?ixlib=rb-4.0.3",  # Cap on white
    "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?ixlib=rb-4.0.3",  # Red cap
    "https://images.unsplash.com/photo-1576871337622-98d48d1cf531?ixlib=rb-4.0.3",  # Cap with model
    "https://images.unsplash.com/photo-1556306535-0f09a537f0a3?ixlib=rb-4.0.3",  # Cap fashion
    "https://images.unsplash.com/photo-1517941823-815bea90d291?ixlib=rb-4.0.3",  # Stylish cap
]

# URLs des images de baskets
SNEAKER_IMAGES = [
    "https://images.unsplash.com/photo-1552346154-21d32810aba3?ixlib=rb-4.0.3",  # Nike Air Force
    "https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3",  # New Balance
    "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?ixlib=rb-4.0.3",  # Sneakers fashion
    "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?ixlib=rb-4.0.3",  # Nike Air Jordan
    "https://images.unsplash.com/photo-1597045566677-8cf032ed6634?ixlib=rb-4.0.3",  # Lifestyle sneakers
]

def download_image(url, category, index):
    """Télécharge une image depuis l'URL donnée."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Créer le dossier s'il n'existe pas
            os.makedirs(f"Mesproduits/{category}", exist_ok=True)
            
            # Générer un nom de fichier
            filename = f"{category}_{index + 1}.jpg"
            filepath = os.path.join("Mesproduits", category, filename)
            
            # Sauvegarder l'image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✓ Image téléchargée : {filename}")
            return True
    except Exception as e:
        print(f"✗ Erreur lors du téléchargement : {str(e)}")
    return False

def main():
    print("Téléchargement des images de casquettes...")
    for i, url in enumerate(CAP_IMAGES):
        download_image(url, "casquettes", i)
    
    print("\nTéléchargement des images de baskets...")
    for i, url in enumerate(SNEAKER_IMAGES):
        download_image(url, "baskets", i)
    
    print("\nTéléchargement terminé!")

if __name__ == "__main__":
    main() 