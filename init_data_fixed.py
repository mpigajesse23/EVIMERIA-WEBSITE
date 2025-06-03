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
            (name, description, price, is_published, featured, stock, available,
             created_at, updated_at, category_id, slug) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s)
            RETURNING id
            """, 
            (
                product["name"], 
                product["description"], 
                product["price"],
                True,  # is_published
                True,  # featured
                10,    # stock
                True,  # available
                product["category"],
                slug
            )
        )
        product_id = cursor.fetchone()[0]
        
        # Ajouter l'image du produit
        cursor.execute("""
            INSERT INTO products_productimage 
            (product_id, image, is_main, created_at) 
            VALUES (%s, %s, %s, NOW())
            """, 
            (
                product_id,
                product["image_url"],
                True  # is_main
            )
        )
        
        print(f"  + {product['name']} créé (ID: {product_id})")

# Téléchargement des images de Mesproduits vers Cloudinary
def upload_local_products(cursor):
    products_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Mesproduits')
    
    if not os.path.exists(products_dir):
        print(f"\n⚠️ Le dossier 'Mesproduits' n'existe pas. Aucun produit local à importer.")
        return
    
    # Récupérer les catégories
    cursor.execute("SELECT id, name FROM products_category")
    categories = cursor.fetchall()
    
    if not categories:
        print("❌ Aucune catégorie trouvée. Impossible de créer des produits.")
        return
    
    # Demander à l'utilisateur de choisir une catégorie
    print("\n📁 Importation des produits locaux")
    print("Veuillez choisir une catégorie pour les produits:")
    
    for i, (cat_id, cat_name) in enumerate(categories):
        print(f"{i+1}. {cat_name}")
    
    choice = input("Entrez le numéro de la catégorie (1-6) ou 'skip' pour ignorer: ")
    
    if choice.lower() == 'skip':
        print("⏩ Importation des produits locaux ignorée.")
        return
    
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(categories):
            raise ValueError("Numéro de catégorie invalide")
        
        selected_cat_id, selected_cat_name = categories[index]
    except ValueError:
        print("❌ Entrée invalide. Importation des produits locaux ignorée.")
        return
    
    print(f"\n🔄 Importation des produits dans la catégorie: {selected_cat_name}")
    
    # Parcourir les fichiers d'images dans le dossier Mesproduits
    imported_count = 0
    for filename in os.listdir(products_dir):
        if any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            file_path = os.path.join(products_dir, filename)
            
            # Extraire le nom du produit à partir du nom de fichier
            product_name = " ".join(os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').split())
            
            # Vérifier si le produit existe déjà
            cursor.execute("SELECT id FROM products_product WHERE name = %s", (product_name,))
            if cursor.fetchone():
                print(f"  - {product_name} existe déjà, ignoré")
                continue
            
            # Télécharger l'image vers Cloudinary
            try:
                print(f"  📤 Téléchargement de {filename}...")
                upload_result = cloudinary.uploader.upload(
                    file_path,
                    folder=f"jaelleshop/products/{selected_cat_name.lower()}",
                    public_id=os.path.splitext(filename)[0]
                )
                
                # Générer un slug unique
                slug = product_name.lower().replace(' ', '-').replace('\'', '')
                
                # Insérer le produit
                cursor.execute("""
                    INSERT INTO products_product 
                    (name, description, price, is_published, featured, stock, available,
                    created_at, updated_at, category_id, slug) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s)
                    RETURNING id
                    """, 
                    (
                        product_name, 
                        f"Produit {product_name} de notre collection {selected_cat_name}", 
                        round(30 + (70 * uuid.uuid4().int / 2**128), 2),  # Prix aléatoire entre 30 et 100
                        True,  # is_published
                        uuid.uuid4().int % 3 == 0,  # featured (1/3 de chance)
                        5 + (uuid.uuid4().int % 15),  # stock entre 5 et 20
                        True,  # available
                        selected_cat_id,
                        slug
                    )
                )
                product_id = cursor.fetchone()[0]
                
                # Ajouter l'image du produit
                cursor.execute("""
                    INSERT INTO products_productimage 
                    (product_id, image, is_main, created_at) 
                    VALUES (%s, %s, %s, NOW())
                    """, 
                    (
                        product_id,
                        upload_result['secure_url'],
                        True  # is_main
                    )
                )
                
                imported_count += 1
                print(f"  ✅ {product_name} importé avec succès (ID: {product_id})")
                
            except Exception as e:
                print(f"  ❌ Erreur lors de l'importation de {filename}: {str(e)}")
    
    print(f"\n✅ Importation terminée! {imported_count} produits ont été ajoutés à la catégorie {selected_cat_name}.")

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
    
    # Proposer d'importer les images locales
    upload_local_products(cursor)
    
    print("\n✅ Initialisation des données terminée avec succès!")
    
    # Fermer la connexion
    cursor.close()
    conn.close()

except Exception as e:
    print(f"\n❌ Erreur lors de l'initialisation des données: {e}")
