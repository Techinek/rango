from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from datetime import datetime

from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered}
                  )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse('Your Rango account is disabled')
        else:
            print(f'Invalid login details: {username}, {password}')
            return HttpResponse('Invalid login details supplied')
    else:
        return render(request, 'rango/login.html')


@login_required()
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]

    visitor_cookie_handler(request)

    context = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': categories,
        'pages': pages,
    }
    response = render(request, 'rango/index.html', context)
    return response


def about(request):
    visitor_cookie_handler(request)
    visits = int(request.session['visits'])
    context = {
        'boldmessage': 'This tutorial has been put together by A.K.',
        'visits': visits
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


@login_required()
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


@login_required()
def add_category(request):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rango:index'))

    context = {
        'form': form
    }
    return render(request, 'rango/add_category.html', context)


def search(request):
    result_list = []
    query = ''

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = Page.objects.filter(
                Q(title__contains=query) | Q(category__name__contains=query))
    context = {
        'result_list': result_list,
        'query': query
    }

    return render(request, 'rango/search.html', context)


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits
