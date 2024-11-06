import requests


def cadastrar(
    nome: str, autor: str, streaming: str, categorias: str, ano_publicacao: int
):
    data = {
        "nome": nome,
        "autor": autor,
        "streaming": streaming,
        "categorias": categorias,
        "ano_publicacao": ano_publicacao,
    }

    response = requests.post("http://127.0.0.1:8000/api/livros/", json=data)
    return response.json()


def get_livros():
    response = requests.get("http://127.0.0.1:8000/api/livros/")
    return response.json()
