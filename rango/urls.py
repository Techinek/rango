from django.urls import path

from .views import (AboutView, AddCategoryView, IndexView, ShowCategoryView,
                    AddPageView, RegisterView, UserLogin, UserLogout,
                    GotoView, RegisterProfile)

app_name = 'rango'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('category/<slug:category_name_slug>/', ShowCategoryView.as_view(),
         name='show_category'),
    path('category/<slug:category_name_slug>/add-page/', AddPageView.as_view(),
         name='add_page'),
    path('add-category/', AddCategoryView.as_view(), name='add_category'),

    # Old simple auth system with no 3-rd library packages for test purposes
    path('old/register/', RegisterView.as_view(), name='register'),
    path('old/login/', UserLogin.as_view(), name='login'),
    path('old/logout/', UserLogout.as_view(), name='logout'),

    # Working with django-redux only. Start from '/accounts/register/'
    path('register-profile/', RegisterProfile.as_view(),
         name='register_profile'),

    path('goto/', GotoView.as_view(), name='goto'),
]
