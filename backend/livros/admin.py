from django.contrib import admin
from .models import Livros, Categorias, Streaming


admin.site.register(Livros)
admin.site.register(Categorias)
admin.site.register(Streaming)
