from django.urls import path

from . import views
app_name = 'rango'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('category/<slug:category_name_slug>/',
         views.ShowCategoryView.as_view(),
         name='show_category'),
    path('category/<slug:category_name_slug>/add-page/',
         views.AddPageView.as_view(),
         name='add_page'),
    path('add-category/', views.AddCategoryView.as_view(),
         name='add_category'),

    # Old simple auth system with no 3-rd library packages for test purposes
    path('old/register/', views.RegisterView.as_view(), name='register'),
    path('old/login/', views.UserLogin.as_view(), name='login'),
    path('old/logout/', views.UserLogout.as_view(), name='logout'),

    # Working with django-redux only. Start from '/accounts/register/'
    path('register-profile/', views.RegisterProfile.as_view(),
         name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),

    # Complementary views: for adding likes, views, filtering categories
    path('goto/', views.GotoView.as_view(), name='goto'),
    path('like-category/', views.LikeCategoryView.as_view(),
         name='like_category'),
    path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
]
