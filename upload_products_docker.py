import os
import sys
import subprocess

# Obtenir le chemin absolu du répertoire de travail actuel
current_dir = os.path.dirname(os.path.abspath(__file__))

# Définir les catégories disponibles
CATEGORIES = [
    'Hommes',
    'Femmes',
    'Chaussures',
    'Montres',
    'Casquettes',
    'Baskets',
]

def main():
    # Vérifier que le dossier Mesproduits existe
    products_dir = os.path.join(current_dir, 'Mesproduits')
    if not os.path.exists(products_dir):
        print(f"Erreur: Le dossier 'Mesproduits' n'existe pas dans {current_dir}")
        return
    
    # Demander la catégorie à l'utilisateur
    print("Veuillez choisir une catégorie pour les produits:")
    for i, category in enumerate(CATEGORIES):
        print(f"{i+1}. {category}")
    
    choice = input("Entrez le numéro de la catégorie (1-6): ")
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(CATEGORIES):
            raise ValueError("Numéro de catégorie invalide")
        selected_category = CATEGORIES[index]
    except ValueError:
        print("Erreur: Veuillez entrer un numéro valide.")
        return
    
    # Vérifier que le sous-dossier de la catégorie existe
    category_dir = os.path.join(products_dir, selected_category.lower())
    if not os.path.exists(category_dir):
        print(f"Erreur: Le dossier '{selected_category.lower()}' n'existe pas dans {products_dir}")
        return
    
    # Construire la commande Docker
    container_name = "evimeria-website-backend-1"
    
    print(f"Copie des produits de la catégorie {selected_category} dans le conteneur Docker...")
    
    # Copier d'abord tout le dossier Mesproduits
    copy_cmd = [
        "docker", "cp", 
        products_dir, 
        f"{container_name}:/app/"
    ]
    
    try:
        subprocess.run(copy_cmd, check=True)
        print("Fichiers copiés avec succès dans le conteneur.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la copie des fichiers: {e}")
        return
    
    # Exécuter la commande Django dans le conteneur Docker
    django_cmd = [
        "docker", "exec", "-it", container_name,
        "python", "manage.py", "upload_new_products",
        f"/app/Mesproduits/{selected_category.lower()}",
        "--category", selected_category
    ]
    
    # Exécuter la commande
    try:
        print(f"Importation des produits pour la catégorie '{selected_category}'...")
        subprocess.run(django_cmd, check=True)
        print(f"Importation des produits terminée avec succès pour la catégorie '{selected_category}'!")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande Django: {e}")

if __name__ == "__main__":
    main()
