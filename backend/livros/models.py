from django.db import models


class Streaming(models.Model):
    nome = models.CharField(
        max_length=50, unique=True
    )  # Nome do serviço de streaming, com valor único
    codigo = models.CharField(
        max_length=2, unique=True
    )  # Código único para identificar cada serviço (ex.: 'N' para Netflix)

    def __str__(self):
        return self.nome


class Categorias(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Livros(models.Model):
    nome = models.CharField(max_length=50)
    autor = models.CharField(max_length=100)
    streaming = models.ForeignKey(
        Streaming, on_delete=models.CASCADE
    )  # Relacionamento com o modelo Streaming
    ano_publicacao = models.IntegerField()
    nota = models.IntegerField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    categorias = models.ManyToManyField(Categorias)

    def __str__(self):
        return self.nome
