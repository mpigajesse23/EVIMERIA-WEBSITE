import os
import cloudinary
import cloudinary.uploader
from supabase import create_client
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'dmcaguchx'),
    api_key=os.environ.get('CLOUDINARY_API_KEY', '238869761337271'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', 'G1AQ85xIMHSFSLgPOXeNsGFnfJA')
)

# Configuration Supabase
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

if not supabase_url or not supabase_key:
    print("❌ Variables d'environnement Supabase manquantes")
    exit(1)

supabase = create_client(supabase_url, supabase_key)

# Fonction pour initialiser les catégories
def init_categories():
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
        result = supabase.table('products_category').select('id').eq('name', cat["name"]).execute()
        if result.data:
            print(f"  - {cat['name']} existe déjà")
            continue
            
        # Insérer la nouvelle catégorie
        result = supabase.table('products_category').insert({
            'name': cat["name"],
            'description': cat["description"],
            'is_published': cat["is_published"],
            'slug': cat["name"].lower().replace(' ', '-')
        }).execute()
        
        if result.data:
            print(f"  + {cat['name']} créée (ID: {result.data[0]['id']})")
        else:
            print(f"  ❌ Erreur lors de la création de {cat['name']}")

# Fonction pour créer des produits de démonstration
def create_demo_products():
    # Récupérer les catégories
    categories_result = supabase.table('products_category').select('id,name').execute()
    categories = {cat['name']: cat['id'] for cat in categories_result.data}
    
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
    
    all_products = homme_products + femme_products
    
    for product in all_products:
        # Vérifier si le produit existe déjà
        result = supabase.table('products_product').select('id').eq('name', product["name"]).execute()
        if result.data:
            print(f"  - {product['name']} existe déjà")
            continue
        
        # Générer un slug unique
        slug = product["name"].lower().replace(' ', '-').replace('\'', '')
        
        # Insérer le produit
        product_data = {
            'name': product["name"],
            'description': product["description"],
            'price': product["price"],
            'is_published': True,
            'featured': True,
            'stock': 10,
            'category_id': product["category"],
            'slug': slug,
            'available': True,
            'image': product["image_url"]
        }
        
        result = supabase.table('products_product').insert(product_data).execute()
        
        if result.data:
            print(f"  + {product['name']} créé (ID: {result.data[0]['id']})")
        else:
            print(f"  ❌ Erreur lors de la création de {product['name']}")

# Initialiser les données
try:
    print(f"🔧 Connexion à Supabase...")
    
    # Initialiser les catégories
    init_categories()
    
    # Créer des produits de démonstration
    create_demo_products()
    
    print("\n✅ Initialisation des données terminée avec succès!")

except Exception as e:
    print(f"❌ Erreur lors de l'initialisation des données: {e}")
