from ninja import Query, Router
from .models import Livros, Categorias, Streaming
from .schemas import LivroSchema, AvaliacaoSchema, FiltrosSortear, LivroSchemaCreate

livros_router = Router()


@livros_router.get("/", response={200: list[LivroSchema], 404: dict})
def get_livros(request):
    livros = Livros.objects.all()

    if livros.count() > 0:
        return 200, livros
    return 404, {"status": "Livros não encontrados"}


@livros_router.post("/", response={200: LivroSchema, 400: dict})
def create_livro(request, livro_schema: LivroSchemaCreate):
    # querysets para buscar streaming e categorias
    streaming_obj = Streaming.objects.all()
    categoria_obj = Categorias.objects.all()

    # Extrair dados do schema
    nome = livro_schema.nome
    autor = livro_schema.autor
    streaming_name = livro_schema.streaming
    categoria_list_name = livro_schema.categorias
    ano_publicacao = livro_schema.ano_publicacao

    # Verificar se o nome do streaming já existe
    if streaming_obj.filter(nome=streaming_name).exists():
        # Buscar o serviço de streaming
        streaming = streaming_obj.get(nome=streaming_name)
    else:
        # Gerar o código para o streaming (primeiros 2 caracteres do nome,
        # em maiúsculo)
        codigo_streaming = streaming_name[:2].upper()
        # Verificar se o código do streaming já existe
        if streaming_obj.filter(codigo=codigo_streaming).exists():
            # Gera o código para o streaming
            codigo_streaming = streaming_name[1].upper() + streaming_name[3].upper()

        # Criar o serviço de streaming
        streaming = streaming_obj.create(nome=streaming_name, codigo=codigo_streaming)

    # Criar o livro e associar o streaming e as categorias
    livro = Livros(
        nome=nome, streaming=streaming, autor=autor, ano_publicacao=ano_publicacao
    )
    livro.save()

    # Associar ou criar categorias
    for categoria_name in categoria_list_name:
        # Verificar se o nome do streaming já existe
        if not categoria_obj.filter(nome=categoria_name).exists():
            categoria = categoria_obj.create(nome=categoria_name)
        else:
            categoria = categoria_obj.get(nome=categoria_name)
        livro.categorias.add(categoria)

    return livro


@livros_router.put("/{livro_id}")
def avaliar_livro(request, livro_id: int, avaliacao_schema: AvaliacaoSchema):
    comentarios = avaliacao_schema.dict()["comentarios"]
    nota = avaliacao_schema.dict()["nota"]

    livro = Livros.objects.get(id=livro_id)
    livro.comentarios = comentarios
    livro.nota = nota

    livro.save()
    return {"status": "Avaliação realizada com sucesso"}


@livros_router.delete("/{livro_id}")
def deletar_livro(request, livro_id: int):
    livro = Livros.objects.get(id=livro_id)
    livro.delete()

    return livro_id


@livros_router.get("/sortear/", response={200: LivroSchema, 404: dict})
def sortear_livro(request, filtros: Query[FiltrosSortear]):
    nota_minima = filtros.dict()["nota_minima"]
    categoria = filtros.dict()["categorias"]
    reassistir = filtros.dict()["reassistir"]

    livros = Livros.objects.all()

    if not reassistir:
        livros = livros.filter(nota=None)

    if nota_minima:
        livros = livros.filter(nota__gte=nota_minima)
    if categoria:
        livros = livros.filter(categorias__id=categoria)

    livro = livros.order_by("?").first()

    if livros.count() > 0:
        return 200, livro
    return 404, {"status": "Livro não encontrado"}
