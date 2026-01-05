from core.apps.accounts.models import Country, Region, District
from deep_translator import GoogleTranslator
import requests
import time

BASE_URL = "https://devapi.goodsign.biz"


def get_region_or_district(item_id: int, item_type: str, country_code=1):
    try:
        country = Country.objects.get(code=str(country_code))
    except Country.DoesNotExist:
        return None

    # ================= REGION =================
    if item_type == "region":
        url = f"{BASE_URL}/v1/regions/all"
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        items = response.json()

        data = next((i for i in items if i["regionId"] == item_id), None)
        if not data:
            return None

        name_ru = data["name"]
        name_uz = GoogleTranslator(source='ru', target='uz').translate(name_ru)
        name_en = GoogleTranslator(source='ru', target='en').translate(name_ru)

        region = Region.objects.create(
            code=str(item_id),
            name=name_uz,
            name_uz=name_uz,
            name_ru=name_ru,
            name_en=name_en,
            country=country
        )
        region.save()
        return region

    # ================= DISTRICT =================
    elif item_type == "district":
        url = f"{BASE_URL}/v1/districts/all"
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        items = response.json()

        data = next((i for i in items if i["districtId"] == item_id), None)
        if not data:
            return None

        region_id = data.get("regionId")
        if not region_id:
            return None

        try:
            region = Region.objects.get(code=str(region_id))
        except Region.DoesNotExist:
            region = get_region_or_district(region_id, "region", country_code)
            if not region:
                return None

        name_ru = data["name"]
        name_uz = GoogleTranslator(source='ru', target='uz').translate(name_ru)
        name_en = GoogleTranslator(source='ru', target='en').translate(name_ru)

        district = District.objects.create(
            code=str(item_id),
            name_uz=name_uz,
            name_ru=name_ru,
            name_en=name_en,
            region=region
        )
        district.save()
        return district

    else:
        raise ValueError("type faqat 'region' yoki 'district' bo'lishi kerak")


def create_country_uzbekistan():
    obj = Country.objects.create(
        name="Uzbekistan",
        name_uz="O'zbekiston",
        name_en="Uzbekistan",
        name_ru="Узбекистан",
        code=1
    )
    return obj


def get_user_data_for_api(stir: int, max_retries=2, delay=1):
    url = f"https://devapi.goodsign.biz/v1/profile/{stir}"
    headers = {"Accept-Language": "uz"}

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=2)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"{attempt}-urinishda xatolik yuz berdi: {e}")
            if attempt < max_retries:
                print(f"{delay} soniya kutib, qayta uriniladi...")
                time.sleep(delay)
            else:
                return False


def get_user_all_data(stir: int, country_code=1):
    user_data = get_user_data_for_api(stir)

    if not user_data:
        raise ValueError("ERR_USER_NOT_FOUND_404")

    if user_data.get('statusCode') is None:
        raise ValueError("ERR_USER_NOT_FOUND_404")

    try:
        country = Country.objects.get(code=str(country_code))
    except Country.DoesNotExist:
        country = create_country_uzbekistan()

    try:
        region = Region.objects.get(code=str(user_data['regionId']))
    except Region.DoesNotExist:
        region = get_region_or_district(user_data['regionId'], "region")

    try:
        district = District.objects.get(code=str(user_data['districtId']))
    except District.DoesNotExist:
        district = get_region_or_district(user_data['districtId'], "district")
    company_name = user_data.get('name', '')

    if isinstance(company_name, str) and company_name.startswith('"'):
        company_name = company_name[1:]

    data = {
        "country": country,
        "region": region,
        "district": district,
        "director_full_name": user_data['director'],
        "company_name": company_name,
        "oked": user_data['oked'],
    }

    return data
