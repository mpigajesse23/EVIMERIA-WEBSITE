import os
import psycopg2
from dotenv import load_dotenv
import random

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de connexion de l'environnement
database_url = os.environ.get('DATABASE_URL', '')

if not database_url:
    print("❌ Aucune URL de base de données trouvée dans les variables d'environnement.")
    exit(1)

print(f"🔧 Connexion à la base de données...")

# Données pour les catégories
categories_data = [
    {"name": "Hommes", "description": "Vêtements et accessoires pour hommes"},
    {"name": "Femmes", "description": "Vêtements et accessoires pour femmes"},
    {"name": "Chaussures", "description": "Chaussures pour hommes et femmes"},
    {"name": "Montres", "description": "Montres élégantes et accessoires"},
    {"name": "Casquettes", "description": "Casquettes et chapeaux tendance"},
    {"name": "Baskets", "description": "Baskets et sneakers à la mode"}
]

# Données pour les produits
products_data = [
    # Hommes
    {
        "name": "T-shirt Classic Homme",
        "description": "T-shirt en coton de haute qualité, coupe classique et confortable",
        "price": 24.99,
        "category": "Hommes",
        "image": "https://res.cloudinary.com/dmcaguchx/image/upload/v1717442642/jaelleshop/hommes/tshirt_classic_slqjio.jpg"
    },
    {
        "name": "Jean Slim Homme",
        "description": "Jean slim en denim élastique, parfait pour toutes les occasions",
        "price": 59.99,
        "category": "Hommes",
        "image": "https://res.cloudinary.com/dmcaguchx/image/upload/v1717442642/jaelleshop/hommes/jean_slim_hkqcvo.jpg"
    },
    # Femmes
    {
        "name": "Robe Élégante",
        "description": "Robe élégante parfaite pour les soirées et événements spéciaux",
        "price": 79.99,
        "category": "Femmes",
        "image": "https://res.cloudinary.com/dmcaguchx/image/upload/v1717442267/jaelleshop/femmes/robe_elegante_ehvhr5.jpg"
    },
    {
        "name": "Top Tendance",
        "description": "Top léger et tendance pour la saison estivale",
        "price": 29.99,
        "category": "Femmes",
        "image": "https://res.cloudinary.com/dmcaguchx/image/upload/v1717442267/jaelleshop/femmes/top_tendance_lffhtr.jpg"
    },
    # Chaussures
    {
        "name": "Baskets Urban Style",
        "description": "Baskets urbaines pour un style décontracté et moderne",
        "price": 89.99,
        "category": "Chaussures",
        "image": "https://res.cloudinary.com/dmcaguchx/image/upload/v1717442366/jaelleshop/chaussures/baskets_urban_style_zvs8yu.jpg"
    },
    # Montres
    {
        "name": "Montre Chronographe",
        "description": "Montre chronographe élégante avec bracelet en cuir",
        "price": 129.99,
        "category": "Montres",
        "image": "https://res.cloudinary.com/dmcaguchx/image/upload/v1717442470/jaelleshop/montres/chronographe_elegant_nl2ptk.jpg"
    }
]

try:
    # Se connecter à la base de données
    conn = psycopg2.connect(database_url)
    conn.autocommit = True  # Important pour que les modifications soient enregistrées
    cursor = conn.cursor()
    
    print("\n🔄 Insertion des catégories...")
    
    # Créer les catégories
    category_ids = {}
    for category in categories_data:
        # Vérifier si la catégorie existe
        cursor.execute("SELECT id FROM products_category WHERE name = %s", (category["name"],))
        existing = cursor.fetchone()
        
        if existing:
            print(f"  ➡️ Catégorie '{category['name']}' existe déjà (ID: {existing[0]})")
            category_ids[category["name"]] = existing[0]
        else:
            # Créer la catégorie
            cursor.execute("""
                INSERT INTO products_category 
                (name, description, slug, is_published, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, NOW(), NOW())
                RETURNING id
                """, 
                (
                    category["name"],
                    category["description"],
                    category["name"].lower().replace(" ", "-"),
                    True
                )
            )
            cat_id = cursor.fetchone()[0]
            category_ids[category["name"]] = cat_id
            print(f"  ✅ Catégorie '{category['name']}' créée (ID: {cat_id})")
    
    print("\n🔄 Insertion des produits...")
    
    # Créer les produits
    for product in products_data:
        # Vérifier si le produit existe
        cursor.execute("SELECT id FROM products_product WHERE name = %s", (product["name"],))
        existing = cursor.fetchone()
        
        if existing:
            print(f"  ➡️ Produit '{product['name']}' existe déjà (ID: {existing[0]})")
            continue
        
        # Obtenir l'ID de catégorie
        cat_id = category_ids.get(product["category"])
        if not cat_id:
            print(f"  ❌ Catégorie '{product['category']}' introuvable pour le produit '{product['name']}'")
            continue
        
        # Créer le produit
        cursor.execute("""
            INSERT INTO products_product 
            (name, description, price, slug, category_id, stock, is_published, featured, available, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            RETURNING id
            """, 
            (
                product["name"],
                product["description"],
                product["price"],
                product["name"].lower().replace(" ", "-"),
                cat_id,
                random.randint(5, 20),
                True,
                random.choice([True, False]),
                True
            )
        )
        prod_id = cursor.fetchone()[0]
        print(f"  ✅ Produit '{product['name']}' créé (ID: {prod_id})")
        
        # Ajouter l'image du produit
        cursor.execute("""
            INSERT INTO products_productimage 
            (product_id, image, is_main, created_at) 
            VALUES (%s, %s, %s, NOW())
            """, 
            (
                prod_id,
                product["image"],
                True
            )
        )
        print(f"     ➕ Image ajoutée pour '{product['name']}'")
    
    print("\n✅ Initialisation des données terminée avec succès!")
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
finally:
    if 'conn' in locals():
        conn.close()
        print("🔒 Connexion fermée")
