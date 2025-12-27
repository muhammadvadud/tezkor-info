from django.db.models import F
from core.apps.main.models import CategoryModel


def find_category_by_oked(user_oked):
    user_oked = str(user_oked)

    variants = {user_oked}
    temp = user_oked
    while temp.endswith('0'):
        temp = temp[:-1]
        variants.add(temp)

    for category in CategoryModel.objects.all():
        cat_code = category.code.replace('.', '')
        if cat_code in variants:
            return category

    return None
