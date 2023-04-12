from .models import Category


def base(request):
    cat = Category.objects.all()
    return {'cat': cat}


