from django.db import transaction
from core.apps.main.models import CategoryModel


@transaction.atomic
def populate_categories():
    """
    PDF'dagi kategoriyalarni 3 tilda tarjima qilingan holda CategoryModel'ga saqlaydi.
    Fayl o‘qilmaydi, ma’lumotlar kod ichida mavjud.
    """
    data = [
        ("01", "Tadbirkorlik faoliyati", "Предпринимательская деятельность", "Entrepreneurship"),
        ("01.1", "Sanoat", "Промышленность", "Industry"),
        ("01.1.1", "Neft-gaz sanoati", "Нефтегазовая промышленность", "Oil and gas industry"),
        ("01.1.2", "Metallurgiya", "Металлургия", "Metallurgy"),
        ("01.1.3", "Mashinasozlik", "Машиностроение", "Mechanical engineering"),
        ("01.2", "Qishloq xo‘jaligi", "Сельское хозяйство", "Agriculture"),
        ("01.2.1", "Paxtachilik", "Хлопководство", "Cotton growing"),
        ("01.2.2", "Bog‘dorchilik", "Садоводство", "Horticulture"),
        ("01.2.3", "Chorvachilik", "Животноводство", "Animal husbandry"),
        ("01.3", "Savdo va xizmat ko‘rsatish", "Торговля и сфера услуг", "Trade and services"),
        ("01.3.1", "Chakana savdo", "Розничная торговля", "Retail trade"),
        ("01.3.2", "Ulgurji savdo", "Оптовая торговля", "Wholesale trade"),
        ("01.3.3", "Restoran va kafelar", "Рестораны и кафе", "Restaurants and cafes"),
        ("01.4", "Axborot texnologiyalari", "Информационные технологии", "Information technology"),
        ("01.4.1", "Dasturiy ta'minot ishlab chiqish", "Разработка программного обеспечения", "Software development"),
        ("01.4.2", "Sun'iy intellekt", "Искусственный интеллект", "Artificial intelligence"),
        ("01.4.3", "Ma'lumotlar tahlili", "Анализ данных", "Data analysis"),
        ("01.5", "Transport va logistika", "Транспорт и логистика", "Transport and logistics"),
        ("01.5.1", "Yo‘l tashish", "Автоперевозки", "Road transportation"),
        ("01.5.2", "Temir yo‘l tashish", "Железнодорожные перевозки", "Rail transportation"),
        ("01.5.3", "Aviatsiya", "Авиация", "Aviation"),
        ("01.6", "Turizm", "Туризм", "Tourism"),
        ("01.6.1", "Ichki turizm", "Внутренний туризм", "Domestic tourism"),
        ("01.6.2", "Xalqaro turizm", "Международный туризм", "International tourism"),
        ("01.7", "Ta'lim", "Образование", "Education"),
        ("01.7.1", "Maktabgacha ta'lim", "Дошкольное образование", "Preschool education"),
        ("01.7.2", "Oliy ta'lim", "Высшее образование", "Higher education"),
        ("01.8", "Sog‘liqni saqlash", "Здравоохранение", "Healthcare"),
        ("01.8.1", "Davolash muassasalari", "Лечебные учреждения", "Medical institutions"),
        ("01.8.2", "Dorixona tarmoqlari", "Аптечные сети", "Pharmacy networks"),
        ("01.9", "Moliyaviy xizmatlar", "Финансовые услуги", "Financial services"),
        ("01.9.1", "Bank sektori", "Банковский сектор", "Banking sector"),
        ("01.9.2", "Sug‘urta", "Страхование", "Insurance"),
        ("01.9.3", "Investitsiya", "Инвестиции", "Investment"),
        ("02", "Davlat boshqaruvi", "Государственное управление", "Public administration"),
        ("02.1", "Mahalliy hokimiyat", "Местное самоуправление", "Local governance"),
        ("02.2", "Ichki ishlar", "Внутренние дела", "Internal affairs"),
        ("02.3", "Tashqi siyosat", "Внешняя политика", "Foreign policy"),
        ("03", "Madaniyat va san’at", "Культура и искусство", "Culture and art"),
        ("03.1", "Adabiyot", "Литература", "Literature"),
        ("03.2", "Musiqa", "Музыка", "Music"),
        ("03.3", "Tasviriy san’at", "Изобразительное искусство", "Visual arts"),
        ("03.4", "Teatr va kino", "Театр и кино", "Theatre and cinema"),
    ]

    cache = {}  # code → CategoryModel
    print("🚀 Kategoriyalar bazaga yozilmoqda...")

    for code, uz, ru, en in data:
        parts = code.split(".")
        level = len(parts)
        parent_code = ".".join(parts[:-1]) if len(parts) > 1 else None
        order = int(parts[-1])
        parent = cache.get(parent_code) if parent_code else None

        obj = CategoryModel.objects.create(
            name=uz,
            code=code,
            parent=parent,
            level=level,
            order=order,
            is_leaf=True
        )
        obj.name_uz = uz
        obj.name_ru = ru
        obj.name_en = en
        obj.save()

        if parent:
            parent.is_leaf = False
            parent.save(update_fields=["is_leaf"])

        cache[code] = obj
        print(f"✅ {code} | {uz} / {ru} / {en}")

    print("\n🎉 Barcha kategoriyalar muvaffaqiyatli saqlandi!")
