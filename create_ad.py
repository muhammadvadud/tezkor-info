import random
from core.apps.main.models import CategoryModel, AdModel
from core.apps.accounts.models import User
from django.contrib.auth.hashers import make_password


def generate_ads_and_users():
    # 1. Avval 10–15 ta user yaratib olamiz
    user_count = 15
    password = "test12345"  # Bir xil parol
    users = []

    for i in range(user_count):
        phone = f"90{1000 + i}"  # qisqa telefonlar: 901000, 901001 ...
        user = User.objects.create(
            phone=phone,
            password=make_password(password),
            person_type="LEGAL_ENTITY",
            role="USER"
        )
        users.append(user)

    print(f"{len(users)} ta user yaratildi.")

    # 2. Category larni olamiz
    categories = CategoryModel.objects.all()
    print(f"{categories.count()} ta category topildi.")

    # 3. Har bir category uchun bitta Ad qo‘shamiz
    for cat in categories:
        creator = random.choice(users)

        ad = AdModel.objects.create(
            created_by=creator,
            title=f"Reklama for category {cat.pk}",
            description=f"Auto generated ad for category {cat.name}",
            total_price=random.randint(10000, 100000)
        )
        ad.types.add(cat)

    print("Hammasi yaratildi.")
