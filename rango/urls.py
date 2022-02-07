from django.urls import path

from .views import (about, index, show_category, add_page,
                    add_category, register, user_login, user_logout,
                    goto_url, register_profile)

app_name = 'rango'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('category/<slug:category_name_slug>/', show_category,
         name='show_category'),
    path('category/<slug:category_name_slug>/add-page/', add_page,
         name='add_page'),
    path('add-category/', add_category, name='add_category'),
    path('register/', register, name='register'),
    path('register-profile/', register_profile, name='register_profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('goto/', goto_url, name='goto'),
]
