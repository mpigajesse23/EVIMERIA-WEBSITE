import os
import psycopg2
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de connexion de l'environnement
database_url = os.environ.get('DATABASE_URL', '')

if not database_url:
    print("❌ Aucune URL de base de données trouvée dans les variables d'environnement.")
    exit(1)

print(f"🔧 Utilisation de la connexion: {database_url[:20]}...")

try:
    # Se connecter à la base de données
    conn = psycopg2.connect(database_url)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Initialiser les catégories
    categories = [
        {"name": "Hommes", "description": "Vêtements et accessoires pour hommes", "is_published": True},
        {"name": "Femmes", "description": "Vêtements et accessoires pour femmes", "is_published": True},
        {"name": "Chaussures", "description": "Chaussures pour hommes et femmes", "is_published": True},
        {"name": "Montres", "description": "Montres élégantes et accessoires", "is_published": True},
        {"name": "Casquettes", "description": "Casquettes et chapeaux tendance", "is_published": True},
        {"name": "Baskets", "description": "Baskets et sneakers à la mode", "is_published": True}
    ]
    
    print(f"\n🔄 Création de {len(categories)} catégories...")
    
    for cat in categories:
        # Vérifier si la catégorie existe déjà
        cursor.execute("SELECT id FROM products_category WHERE name = %s", (cat["name"],))
        if cursor.fetchone():
            print(f"  - {cat['name']} existe déjà")
            continue
            
        # Insérer la nouvelle catégorie
        cursor.execute("""
            INSERT INTO products_category 
            (name, description, is_published, created_at, updated_at, slug) 
            VALUES (%s, %s, %s, NOW(), NOW(), %s)
            RETURNING id
            """, 
            (cat["name"], cat["description"], cat["is_published"], cat["name"].lower().replace(' ', '-'))
        )
        cat_id = cursor.fetchone()[0]
        print(f"  + {cat['name']} créée (ID: {cat_id})")
    
    # Fermer la connexion
    cursor.close()
    conn.close()
    
    print("\n✅ Initialisation des catégories terminée avec succès!")
    
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation des catégories: {e}")
