from django.urls import path
from .views import GrupoDetalhesView, IndexView, CriarGrupoView, MinhasComunidadesView, ExcluirGrupoView, EditarGrupoView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('grupo/<int:grupo_id>/', GrupoDetalhesView.as_view(), name='grupo_detalhes'),
    path('criar-grupo/', CriarGrupoView.as_view(), name='criar_grupo'),
    path('minhas-comunidades/', MinhasComunidadesView.as_view(), name='minhas_comunidades'),
    path('grupo/<int:grupo_id>/editar/', EditarGrupoView.as_view(), name='editar_grupo'),
    path('grupo/<int:grupo_id>/excluir/', ExcluirGrupoView.as_view(), name='excluir_grupo'),
]
