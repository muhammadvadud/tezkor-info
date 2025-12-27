import json
from django.db import transaction
from core.apps.main.models import CategoryModel


def get_parent_code(code: str) -> str | None:
    """
    01.11.11.1 -> 01.11.11
    01 -> None
    """
    if "." not in code:
        return None
    return ".".join(code.split(".")[:-1])


def get_level(code: str) -> int:
    """
    01 -> 1
    01.1 -> 2
    01.11.11.1 -> 4
    """
    return len(code.split("."))


@transaction.atomic
def import_categories(
        uz_path: str,
        ru_path: str,
        en_path: str,
):
    # --- JSONlarni o‘qiymiz
    with open(uz_path, encoding="utf-8") as f:
        uz_data = {i["CODE"]: i["NAME"] for i in json.load(f)["result"]["data"]}

    with open(ru_path, encoding="utf-8") as f:
        ru_data = {i["CODE"]: i["NAME"] for i in json.load(f)["result"]["data"]}

    with open(en_path, encoding="utf-8") as f:
        en_data = {i["CODE"]: i["NAME"] for i in json.load(f)["result"]["data"]}

    all_codes = set(uz_data) | set(ru_data) | set(en_data)

    # --- Oldindan bor kategoriyalar
    existing = CategoryModel.objects.in_bulk(field_name="code")

    # --- Avval hammasini is_leaf=True deb yaratamiz
    created = {}

    for code in sorted(all_codes, key=lambda x: (get_level(x), x)):
        if code in existing:
            created[code] = existing[code]
            continue

        parent_code = get_parent_code(code)
        parent = created.get(parent_code)

        category = CategoryModel.objects.create(
            code=code,
            parent=parent,
            level=get_level(code),
            is_leaf=True,
            name_uz=uz_data.get(code),
            name_ru=ru_data.get(code),
            name_en=en_data.get(code),
        )

        created[code] = category

        # parent leaf emas endi
        if parent:
            parent.is_leaf = False
            parent.save(update_fields=["is_leaf"])

    return len(created)
