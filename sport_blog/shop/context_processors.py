from .models import CategoryShop


def base_cat_shop(request):
    cat_shop = CategoryShop.objects.all()
    return {'cat_shop': cat_shop}


