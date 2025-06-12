from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Grupo, Mensagem
from .forms import GrupoForm

class IndexView(ListView):
    model = Grupo
    template_name = 'index.html'
    context_object_name = 'grupos'
    paginate_by = 3
    ordering = ['-criado_em']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupos_list = Grupo.objects.order_by('-criado_em')
        paginator = Paginator(grupos_list, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            grupos = paginator.page(page)
        except PageNotAnInteger:
            grupos = paginator.page(1)
        except EmptyPage:
            grupos = paginator.page(paginator.num_pages)

        context['page_obj'] = grupos
        return context

class GrupoDetalhesView(DetailView):
    model = Grupo
    template_name = 'grupo_detalhes.html'
    context_object_name = 'grupo'

    def get_object(self, queryset=None):
        grupo_id = self.kwargs.get('grupo_id')
        return get_object_or_404(Grupo, id=grupo_id)

    def post(self, request, *args, **kwargs):
        grupo = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar logado para enviar mensagens.")
            return redirect('loginuser')
        texto = request.POST.get('texto')
        if texto:
            Mensagem.objects.create(grupo=grupo, usuario=request.user, texto=texto)
            messages.success(request, "Mensagem enviada com sucesso!")
        return self.get(request, *args, **kwargs)


class CriarGrupoView(LoginRequiredMixin, View):
    template_name = "criar_grupo.html"

    def get(self, request):
        form = GrupoForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.criador = request.user
            grupo.save()
            return redirect("minhas_comunidades")
        return render(request, self.template_name, {"form": form})

class MinhasComunidadesView(LoginRequiredMixin, ListView):
    model = Grupo
    template_name = 'minhas_comunidades.html'
    context_object_name = 'minhas_comunidades'
    paginate_by = 5

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, "Você não está logado e não tem acesso às comunidades.")
            return Grupo.objects.none()
        return Grupo.objects.filter(criador=self.request.user)

class EditarGrupoView(LoginRequiredMixin, UpdateView):
    model = Grupo
    form_class = GrupoForm
    template_name = 'editar_grupo.html'

    def get_success_url(self):
        messages.success(self.request, "Grupo editado com sucesso!")
        return reverse_lazy('grupo_detalhes', kwargs={'grupo_id': self.object.id})

    def get_object(self, queryset=None):
        grupo_id = self.kwargs.get('grupo_id')
        return get_object_or_404(Grupo, id=grupo_id, criador=self.request.user)

class ExcluirGrupoView(LoginRequiredMixin, DeleteView):
    model = Grupo
    context_object_name = 'grupo'
    success_url = reverse_lazy('minhas_comunidades')
    template_name = 'grupo_confirm_delete.html'

    def get_object(self, queryset=None):
        grupo_id = self.kwargs.get('grupo_id')
        return get_object_or_404(Grupo, id=grupo_id, criador=self.request.user)

    def delete(self, request, *args, **kwargs):
        grupo = self.get_object()
        grupo.delete()
        messages.success(request, "Grupo excluído com sucesso!")
        return redirect(self.success_url)
