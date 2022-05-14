from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views
from .views import AuthorUpdateView, UserUpdateView

app_name = 'my_auth'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', login_required(views.about), name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name="logout"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('profile/', login_required(views.profile), name='profile'),
    path('users/<int:pk>/userupdate/', login_required(UserUpdateView.as_view()), name='userupdate'),
    path('authors/<int:pk>/authorupdate/', login_required(AuthorUpdateView.as_view()), name='authorupdate'),
    # path("accounts/", include("django.contrib.auth.urls")),
    path('profile/api_token/', login_required(views.get_api_token), name='api_token'),
    path('profile/api_token/<token>/', login_required(views.send_api_token_email), name='api_token_email'),
]