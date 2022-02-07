from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views import View

from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm


class RegisterProfile(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserProfileForm()
        context = {'form': form}
        return render(request, 'rango/profile_registration.html', context)

    @method_decorator(login_required)
    def post(self, request):
        form = UserProfileForm(request.FILES, request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = self.request.user
            form.save()
            return redirect(reverse('rango:index'))
        context = {'form': form}
        return render(request, 'rango/profile_registration.html', context)


class IndexView(View):
    def get(self, request):
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


class AboutView(View):
    def get(self, request):
        visitor_cookie_handler(request)
        visits = int(request.session['visits'])
        context = {
            'boldmessage': 'This tutorial has been put together by A.K.',
            'visits': visits
        }
        return render(request, 'rango/about.html', context)


class ShowCategoryView(View):
    def create_context(self, category_name_slug):
        category = get_object_or_404(Category, slug=category_name_slug)
        category_pages = category.pages.order_by('-views')
        context = {
            'category': category,
            'pages': category_pages
        }
        return context

    def get(self, request, category_name_slug):
        context = self.create_context(category_name_slug)
        return render(request, 'rango/category.html', context)

    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        context = self.create_context(category_name_slug)
        query = request.POST['query'].strip()
        if query:
            result_list = context['category'].pages.filter(
                    Q(title__contains=query) | Q(url__contains=query))
            context['result_list'] = result_list

        return render(request, 'rango/category.html', context)


class AddPageView(View):
    @method_decorator(login_required)
    def get(self, request, category_name_slug):
        category = get_object_or_404(Category, slug=category_name_slug)
        if not category:
            return redirect(reverse('rango:home'))
        form = PageForm()
        context = {
            'form': form,
            'category': category
        }
        return render(request, 'rango/add_page.html', context)

    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        category = get_object_or_404(Category, slug=category_name_slug)
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(reverse
                            ('rango:show_category', kwargs={
                                'category_name_slug': category_name_slug}))
        context = {
            'form': form,
            'category': category
        }
        return render(request, 'rango/add_page.html', context)


class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        context = {'form': form}
        return render(request, 'rango/add_category.html', context)

    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
        context = {'form': form}
        return render(request, 'rango/add_category.html', context)


class GotoView(View):
    def get(self, request):
        param_query = request.GET.get('page_id')
        page = get_object_or_404(Page, pk=param_query)
        if page:
            page.views += 1
            page.save()
            return redirect(page.url)
        else:
            return redirect(reverse('rango:index'))


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


# Old and simple auth system with no 3-rd packages used. For test purposes only
class RegisterView(View):
    def get(self, request):
        registered = False
        user_form = UserForm()
        profile_form = UserProfileForm()

        context = {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered}

        return render(request, 'rango/register.html', context)

    def post(self, request):
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

            context = {'user_form': user_form,
                       'profile_form': profile_form,
                       'registered': registered}

            return render(request, 'rango/register.html', context)


class UserLogin(View):
    def get(self, request):
        return render(request, 'rango/login.html')

    def post(self, request):
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


class UserLogout(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect(reverse('rango:index'))
