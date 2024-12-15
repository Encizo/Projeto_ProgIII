from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.UsuarioCreateView.as_view(), name='cadastrouser'),  # URL para cadastro de usuário
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('usuarios/logout/', views.LogoutUserView.as_view(), name='logout'),
]
