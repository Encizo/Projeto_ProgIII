from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from .forms import UsuarioCreationForm


def custom_logout(request):
    logout(request)
    return redirect('home')

class UsuarioCreateView(CreateView):
    template_name = 'usuario/cadusuario.html'
    form_class = UsuarioCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.set_password(form.cleaned_data['password1'])
        usuario.save()
        messages.success(self.request, "Usuário cadastrado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Erro no campo '{field}': {error}")
        return super().form_invalid(form)

class LoginUserView(FormView):
    template_name = 'usuario/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.cleaned_data['username']
        senha = form.cleaned_data['password']
        usuario = authenticate(self.request, username=user, password=senha)
        if usuario is not None:
            login(self.request, usuario)
            return redirect(self.success_url)
        else:
            messages.error(self.request, "Usuário ou senha inválida")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Usuário ou senha inválida")
        return super().form_invalid(form)

class LogoutUserView(LoginRequiredMixin, LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


