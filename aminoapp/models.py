from django.db import models
from django.conf import settings

class Grupo(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    palavras_chave = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Mensagem(models.Model):
    grupo = models.ForeignKey(Grupo, related_name='mensagens', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username}: {self.texto[:30]}'