from django.urls import path

from .views import about, index, show_category, add_page, add_category

app_name = 'rango'

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('category/<slug:category_name_slug>/', show_category,
         name='show_category'),
    path('category/<slug:category_name_slug>/add-page/', add_page,
         name='add_page'),
    path('add-category/', add_category, name='add_category')
]