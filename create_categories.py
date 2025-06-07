import subprocess
import sys

def create_categories():
    """Créer les catégories dans la base de données Django via Docker"""
    
    container_name = "evimeria-website-backend-1"
    
    # Script Python à exécuter dans Django
    django_script = """
from products.models import Category

categories = [
    'Hommes',
    'Femmes', 
    'Chaussures',
    'Montres',
    'Casquettes',
    'Baskets',
]

print("Creation des categories...")
for cat_name in categories:
    category, created = Category.objects.get_or_create(name=cat_name)
    if created:
        print(f"[OK] Categorie '{cat_name}' creee avec succes")
    else:
        print(f"[INFO] Categorie '{cat_name}' existe deja")

print(f"\\nNombre total de categories: {Category.objects.count()}")
print("Categories disponibles:")
for cat in Category.objects.all():
    print(f"  - {cat.name}")
"""
    
    # Commande pour exécuter le script Python dans le conteneur Django
    cmd = [
        "docker", "exec", "-i", container_name,
        "python", "manage.py", "shell"
    ]
    
    try:
        print("Création des catégories dans la base de données...")
        process = subprocess.Popen(
            cmd, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=django_script)
        
        if process.returncode == 0:
            print("[OK] Categories creees avec succes!")
            print(stdout)
        else:
            print(f"Erreur lors de la creation des categories: {stderr}")
            return False
            
    except Exception as e:
        print(f"Erreur lors de l'exécution de la commande: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if create_categories():
        print("\n[OK] Les categories sont pretes! Vous pouvez maintenant utiliser upload_products_docker.py")
    else:
        print("\n[ERREUR] Echec de la creation des categories")
        sys.exit(1)
