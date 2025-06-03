import os
import cloudinary
import cloudinary.uploader
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv
import uuid

# Charger les variables d'environnement
load_dotenv()

# Configuration Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'dmcaguchx'),
    api_key=os.environ.get('CLOUDINARY_API_KEY', '238869761337271'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', 'G1AQ85xIMHSFSLgPOXeNsGFnfJA')
)

# Récupérer l'URL de connexion de l'environnement
database_url = os.environ.get('DATABASE_URL', '')

if not database_url:
    print("❌ Aucune URL de base de données trouvée dans les variables d'environnement.")
    exit(1)

# Fonction pour initialiser les catégories
def init_categories(cursor):
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

# Fonction pour créer des produits de démonstration
def create_demo_products(cursor):
    # Récupérer les catégories
    cursor.execute("SELECT id, name FROM products_category")
    categories = {name: id for id, name in cursor.fetchall()}
    
    if not categories:
        print("❌ Aucune catégorie trouvée. Impossible de créer des produits.")
        return
    
    print(f"\n🔄 Création de produits de démonstration...")
    
    # Produits pour hommes
    homme_products = [
        {
            "name": "T-shirt Classic Homme",
            "description": "T-shirt en coton de haute qualité, coupe classique et confortable",
            "price": 24.99,
            "category": categories["Hommes"],
            "image_url": "https://res.cloudinary.com/dmcaguchx/image/upload/v1622547896/jaelleshop/products/hommes/tshirt_classic.jpg"
        },
        {
            "name": "Jean Slim Homme",
            "description": "Jean slim en denim élastique, parfait pour toutes les occasions",
            "price": 59.99,
            "category": categories["Hommes"],
            "image_url": "https://res.cloudinary.com/dmcaguchx/image/upload/v1622547896/jaelleshop/products/hommes/jean_slim.jpg"
        }
    ]
    
    # Produits pour femmes
    femme_products = [
        {
            "name": "Robe Élégante",
            "description": "Robe élégante parfaite pour les soirées et événements spéciaux",
            "price": 79.99,
            "category": categories["Femmes"],
            "image_url": "https://res.cloudinary.com/dmcaguchx/image/upload/v1622547896/jaelleshop/products/femmes/robe_elegante.jpg"
        },
        {
            "name": "Top Tendance",
            "description": "Top léger et tendance pour la saison estivale",
            "price": 29.99,
            "category": categories["Femmes"],
            "image_url": "https://res.cloudinary.com/dmcaguchx/image/upload/v1622547896/jaelleshop/products/femmes/top_tendance.jpg"
        }
    ]
    
    # Chaussures
    chaussures_products = [
        {
            "name": "Baskets Urban Style",
            "description": "Baskets urbaines pour un style décontracté et moderne",
            "price": 89.99,
            "category": categories["Chaussures"],
            "image_url": "https://res.cloudinary.com/dmcaguchx/image/upload/v1622547896/jaelleshop/products/chaussures/baskets_urbaines.jpg"
        }
    ]
    
    # Montres
    montres_products = [
        {
            "name": "Montre Chronographe",
            "description": "Montre chronographe élégante avec bracelet en cuir",
            "price": 129.99,
            "category": categories["Montres"],
            "image_url": "https://res.cloudinary.com/dmcaguchx/image/upload/v1622547896/jaelleshop/products/montres/chrono_elegant.jpg"
        }
    ]
    
    all_products = homme_products + femme_products + chaussures_products + montres_products
    
    for product in all_products:
        # Vérifier si le produit existe déjà
        cursor.execute("SELECT id FROM products_product WHERE name = %s", (product["name"],))
        if cursor.fetchone():
            print(f"  - {product['name']} existe déjà")
            continue
        
        # Générer un slug unique
        slug = product["name"].lower().replace(' ', '-').replace('\'', '')
        
        # Insérer le produit
        cursor.execute("""
            INSERT INTO products_product 
            (name, description, price, is_published, featured, stock, 
             created_at, updated_at, category_id, slug, available) 
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s, %s)
            RETURNING id
            """, 
            (
                product["name"], 
                product["description"], 
                product["price"],
                True,  # is_published
                True,  # featured
                10,    # stock
                product["category"],
                slug,
                True   # available
            )
        )
        product_id = cursor.fetchone()[0]
        
        # Ajouter l'image du produit - utiliser la table ProductImage si elle existe
        try:
            cursor.execute("""
                INSERT INTO products_productimage
                (image, is_primary, created_at, updated_at, product_id)
                VALUES (%s, %s, NOW(), NOW(), %s)
                """,
                (
                    product["image_url"],
                    True,  # is_primary
                    product_id
                ))
        except Exception as img_error:
            print(f"    ⚠️ Impossible d'ajouter l'image: {img_error}")
            # Fallback: essayer d'utiliser directement le champ image du produit si disponible
            try:
                cursor.execute("""
                    UPDATE products_product
                    SET image = %s
                    WHERE id = %s
                    """,
                    (
                        product["image_url"],
                        product_id
                    ))
                print("    ✓ Image ajoutée directement au produit")
            except Exception as upd_error:
                print(f"    ❌ Impossible de mettre à jour l'image: {upd_error}")
        )
        
        print(f"  + {product['name']} créé (ID: {product_id})")

# Se connecter et initialiser les données
try:
    print(f"🔧 Connexion à la base de données...")
    conn = psycopg2.connect(database_url)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Initialiser les catégories
    init_categories(cursor)
    
    # Créer des produits de démonstration
    create_demo_products(cursor)
    
    print("\n✅ Initialisation des données terminée avec succès!")
    
    # Fermer la connexion
    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Erreur lors de l'initialisation des données: {e}")
