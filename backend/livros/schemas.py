from ninja import ModelSchema, Schema
from .models import Livros
from typing import List


class LivroSchema(ModelSchema):
    class Meta:
        model = Livros
        fields = [
            "id",
            "nome",
            "autor",
            "streaming",
            "categorias",
            "comentarios",
            "nota",
            "ano_publicacao",
        ]


class LivroSchemaCreate(Schema):
    nome: str
    autor: str
    streaming: str
    categorias: List[str]
    ano_publicacao: int


class AvaliacaoSchema(ModelSchema):
    class Meta:
        model = Livros
        fields = ["nota", "comentarios"]


class FiltrosSortear(Schema):
    nota_minima: int = None
    categorias: int = None
    reassistir: bool = False
