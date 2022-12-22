from django.shortcuts import render, get_object_or_404
from .models import Post, Category
# Create your views here.
def blog(request):
    posts = Post.objects.all()
    result = {
        "posts": posts
    }
    return render(request, 'blog/blog.html', result)

def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    """
    En vez de hacer esto, usar template tag
    posts = Post.objects.filter(categories=category)

    result = {
        'category': category,
        'posts': posts
    }
    """
    return render(request, 'blog/category.html', {'category': category})