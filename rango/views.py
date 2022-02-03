from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import Category, Page
from .forms import CategoryForm, PageForm


def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': categories,
        'pages': pages
    }
    return render(request, 'rango/index.html', context)


def about(request):
    context = {
        'boldmessage': 'This tutorial has been put together by A.K.'
    }
    return render(request, 'rango/about.html', context)


def show_category(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    category_pages = category.pages.all()

    context = {
        'category': category,
        'pages': category_pages
    }
    return render(request, 'rango/category.html', context)


def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    if not category:
        return redirect(reverse('rango:home'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(reverse('rango:show_category',
                            kwargs={'category_name_slug': category_name_slug}))

    context = {
        'form': form,
        'category': category
    }
    return render(request, 'rango/add_page.html', context)


def add_category(request):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rango:home'))

    context = {
        'form': form
    }
    return render(request, 'rango/add_category.html', context)
