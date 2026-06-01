import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Partner, Product, BlogPost, NavMenu

# Create superuser if not exists
if not User.objects.filter(username='admin').exists():
    admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', os.urandom(16).hex())
    User.objects.create_superuser('admin', 'admin@example.com', admin_password)
    print(f'Superuser created: admin / {admin_password}')
    print('WARNING: Change DJANGO_SUPERUSER_PASSWORD in .env for a custom password.')

# Categories
cats = ['Electronics', 'Fashion', 'Home & Kitchen', 'Health & Beauty', 'Food & Grocery']
for c in cats:
    Category.objects.get_or_create(name=c)
print('Categories created')

# Partners
partners_data = [
    {'name': 'Khulshiuddokterbazar', 'description': 'Visit for Khulshiuddokterbazar deals!', 'is_dealer': True},
    {'name': 'Bholauddokterbazar', 'description': 'Visit for Bholauddokterbazar deals!', 'is_dealer': True},
    {'name': 'Gafargaonuddoktarbazar', 'description': 'Visit for Gafargaonuddoktarbazar deals!', 'is_seller': True},
    {'name': 'MatlabNorthuddoktarbazar', 'description': 'Visit for MatlabNorthuddoktarbazar deals!', 'is_seller': True},
    {'name': 'LatifpurGopalganj', 'description': 'Premium products from Latifpur', 'is_dealer': True, 'is_seller': True},
]
for p in partners_data:
    Partner.objects.get_or_create(name=p['name'], defaults=p)
print('Partners created')

# Products
partner = Partner.objects.first()
categories = list(Category.objects.all())
products_data = [
    {'name': 'Flower Heat Resistant Silicone Mat Drink Cup Coasters Non-slip Pot Holder', 'price': 590, 'old_price': 640, 'label': 'new', 'category': categories[2]},
    {'name': 'Ramadan Decoration is an excellent choice', 'price': 250, 'old_price': 350, 'label': 'discounted', 'category': categories[2]},
    {'name': 'Tea pot set or single cattle', 'price': 700, 'old_price': 800, 'label': 'new', 'category': categories[2]},
    {'name': '32 piece ceramic dinner set premium quality', 'price': 3200, 'old_price': 3500, 'label': 'hot', 'category': categories[2]},
    {'name': 'Rice Cooker Miyako 1.8L Double SS pot', 'price': 2550, 'old_price': 2850, 'label': 'hot', 'category': categories[0]},
    {'name': 'Miyako 3 LTR Double Pot Rice Cooker ASL-300', 'price': 4500, 'old_price': 4490, 'label': 'new', 'category': categories[0]},
    {'name': 'Pahari Natural Honey', 'price': 1200, 'old_price': 1300, 'label': 'hot', 'category': categories[4]},
    {'name': 'Super Slim Fit Solid Chinos', 'price': 2300, 'old_price': 2500, 'label': 'hot', 'category': categories[1]},
    {'name': 'Vegetable Chopper with Mandoline Slicer', 'price': 700, 'old_price': 850, 'label': 'hot', 'category': categories[2]},
    {'name': 'Girls T-Shirt (2-4 Years) - Disney', 'price': 650, 'old_price': 750, 'label': 'hot', 'category': categories[1]},
    {'name': 'Premium China Watch', 'price': 885, 'old_price': 980, 'label': 'new', 'category': categories[1]},
    {'name': 'Tab.Nexum mups 20 mg', 'price': 850, 'old_price': 1000, 'label': 'hot', 'category': categories[3]},
    {'name': 'Topp Super Clean Detergent Powder', 'price': 60, 'old_price': 80, 'label': 'new', 'category': categories[4]},
    {'name': 'Syrup Safini 450ml', 'price': 650, 'old_price': 700, 'label': '', 'category': categories[3]},
    {'name': 'Syrup Liverton 450ml', 'price': 280, 'old_price': 300, 'label': '', 'category': categories[3]},
    {'name': 'Getwell Nebulizer Compressor Machine', 'price': 2400, 'old_price': 2800, 'label': 'new', 'category': categories[3]},
]
for p in products_data:
    partner_obj = partner
    cat = p.pop('category')
    Product.objects.get_or_create(
        name=p['name'],
        defaults={**p, 'partner': partner_obj, 'category': cat, 'stock': 50, 'available': True}
    )
print('Products created')

# Blog posts
posts = [
    {'title': 'Latest Bridal Gold jewelry Gold Plated Choker Mala Jewellery Design', 'content': 'Latest Bridal Gold jewelry Gold Plated Choker Mala Jewellery Design. Discover our exclusive collection of gold plated jewelry perfect for weddings and special occasions.', 'excerpt': 'Latest Bridal Gold jewelry Gold Plated Choker Mala Jewellery Design.', 'views': 49, 'comments': 5},
    {'title': 'Gold plate Necklaces Enhance Your Style with Majumder shop\'s Collection', 'content': 'Gold plate Necklaces Enhance Your Style with Majumder shop\'s Collection. Explore our wide range of necklaces designed to complement any outfit.', 'excerpt': 'Gold plate Necklaces Enhance Your Style with Majumder shop\'s Collection.', 'views': 49, 'comments': 5},
    {'title': 'New Arrivals: Best Deals This Season', 'content': 'Check out our latest arrivals with amazing deals. From electronics to fashion, we have everything you need at the best prices.', 'excerpt': 'Check out our latest arrivals with amazing deals.', 'views': 35, 'comments': 3},
]
for p in posts:
    BlogPost.objects.get_or_create(title=p['title'], defaults=p)
print('Blog posts created')

# Nav Menu items
menu_items = [
    {'title': 'Home', 'url': 'home', 'url_type': 'named_url', 'order': 0, 'login_required': False, 'logout_required': False, 'match_startswith': False},
    {'title': 'All Product', 'url': 'shop_grid', 'url_type': 'named_url', 'order': 1, 'login_required': False, 'logout_required': False, 'match_startswith': False},
    {'title': 'All Partner', 'url': 'partner_list', 'url_type': 'named_url', 'order': 2, 'login_required': False, 'logout_required': False, 'match_startswith': False},
    {'title': 'All Dealer', 'url': 'dealer_list', 'url_type': 'named_url', 'order': 3, 'login_required': False, 'logout_required': False, 'match_startswith': False},
    {'title': 'Seller List', 'url': 'seller_list', 'url_type': 'named_url', 'order': 4, 'login_required': False, 'logout_required': False, 'match_startswith': False},
    {'title': 'Blog', 'url': 'blog_list', 'url_type': 'named_url', 'order': 5, 'login_required': False, 'logout_required': False, 'match_startswith': False},
    {'title': 'Contact', 'url': 'contact', 'url_type': 'named_url', 'order': 6, 'login_required': False, 'logout_required': False, 'match_startswith': False},
    {'title': 'Dashboard', 'url': 'dashboard', 'url_type': 'named_url', 'order': 7, 'login_required': True, 'logout_required': False, 'match_startswith': True},
    {'title': 'Login', 'url': 'login', 'url_type': 'named_url', 'order': 8, 'login_required': False, 'logout_required': True, 'match_startswith': False},
    {'title': 'Registration', 'url': 'register', 'url_type': 'named_url', 'order': 9, 'login_required': False, 'logout_required': True, 'match_startswith': False},
]
for item in menu_items:
    NavMenu.objects.get_or_create(title=item['title'], defaults=item)
print('Nav menu items created')

print('\n--- Seed complete! ---')
print(f'Admin login: admin / {os.getenv("DJANGO_SUPERUSER_PASSWORD", "[random - see output above]")}')
print(f'Products: {Product.objects.count()}')
print(f'Categories: {Category.objects.count()}')
print(f'Partners: {Partner.objects.count()}')
print(f'Blog posts: {BlogPost.objects.count()}')
