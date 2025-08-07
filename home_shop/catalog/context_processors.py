from .models import Category, Product


def all_categories(request):
    return {
        'all_categories': Category.objects.all(),
        'all_models': Product.objects.all()
    }
