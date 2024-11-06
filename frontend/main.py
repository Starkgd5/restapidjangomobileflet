import flet as ft
import requests
from urllib.parse import urlparse, parse_qs
from connect import get_livros, cadastrar


def main(page: ft.Page):
    page.title = "Cadastro App"
    page.window.width = 400

    # Inputs Globais
    nome_input = ft.TextField(label="Nome do Livro", text_align=ft.TextAlign.LEFT)
    autor_input = ft.TextField(label="Nome do Autor", text_align=ft.TextAlign.LEFT)
    streaming_input = ft.TextField(label="Nome do Streaming")
    categoria_input = ft.TextField(label="Categorias (separadas por vírgula)")
    ano_publicacao_input = ft.TextField(label="Ano de pulicação")

    # Lista de Livros
    lista_livros = ft.ListView()

    # Função de Cadastro
    def cadastrar_livro(e):
        categorias = [cat.strip() for cat in categoria_input.value.split(",")]
        response = cadastrar(
            nome=nome_input.value,
            autor=autor_input.value,
            streaming=streaming_input.value,
            categorias=categorias,
            ano_publicacao=int(ano_publicacao_input.value),
        )

        if response:
            page.snack_bar = ft.SnackBar(ft.Text("Livro cadastrado com sucesso!"))
            page.snack_bar.open = True
            carregar_livros()  # Recarregar lista de livros
            nome_input.value = ""
            autor_input.value = ""
            categoria_input.value = ""
            ano_publicacao_input.value = None
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao cadastrar o livro"))
            page.snack_bar.open = True

    cadastrar_btn = ft.ElevatedButton("Cadastrar", on_click=cadastrar_livro)

    # Função para carregar e exibir os livros
    def carregar_livros():
        lista_livros.controls.clear()
        for livro in get_livros():
            lista_livros.controls.append(
                ft.Container(
                    ft.Text(livro["nome"]),
                    bgcolor=ft.colors.BLACK12,
                    padding=15,
                    alignment=ft.alignment.center,
                    margin=3,
                    border_radius=10,
                    on_click=lambda e, livro_id=livro["id"]: page.go(
                        f"/review?id={livro_id}"
                    ),
                )
            )
        page.update()

    # Função de Avaliação
    def avaliar_livro(e, livro_id):
        data = {"nota": int(nota_input.value), "comentarios": comentario_input.value}
        try:
            response = requests.put(
                f"http://127.0.0.1:8000/api/livros/{livro_id}", json=data
            )
            if response.status_code == 200:
                page.snack_bar = ft.SnackBar(ft.Text("Avaliação enviada com sucesso!"))
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Erro ao enviar a avaliação."))
            page.snack_bar.open = True
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro de conexão: {ex}"))
            page.snack_bar.open = True
        page.update()

    # Página de Review
    def review_page(livro_id):
        global nota_input, comentario_input
        nota_input = ft.TextField(
            label="Nota (inteiro)", text_align=ft.TextAlign.LEFT, value="0", width=100
        )
        comentario_input = ft.TextField(label="Comentário", multiline=True, expand=True)

        avaliar_btn = ft.ElevatedButton(
            "Avaliar", on_click=lambda e: avaliar_livro(e, livro_id)
        )
        voltar_btn = ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/"))

        page.views.append(
            ft.View(
                "/review",
                controls=[
                    ft.Text("Review Page"),
                    ft.Text(f"Detalhes do livro com ID: {livro_id}"),
                    nota_input,
                    comentario_input,
                    avaliar_btn,
                    voltar_btn,
                ],
            )
        )
        page.update()

    # Página Home
    def home_page():
        carregar_livros()
        page.views.append(
            ft.View(
                "/",
                controls=[
                    nome_input,
                    autor_input,
                    streaming_input,
                    categoria_input,
                    ano_publicacao_input,
                    cadastrar_btn,
                    lista_livros,
                ],
            )
        )
        page.update()

    # Controle de Rotas
    def route_change(e):
        page.views.clear()
        if page.route == "/":
            home_page()
        elif page.route.startswith("/review"):
            parsed_url = urlparse(page.route)
            query_params = parse_qs(parsed_url.query)
            livro_id = query_params.get("id", [None])[0]
            if livro_id:
                review_page(livro_id)

    page.on_route_change = route_change
    page.go("/")


ft.app(target=main)
