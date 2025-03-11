from firebase.config_firebase import db

def verificar_livro(id):
    livro_ref = db.collection('livros').document(id)
    livro = livro_ref.get()
    if livro.exists:
        print(f'Opa! Um Livro com o {id} já existe.')
        return True
    return False

def criar_livro(titulo, autor, paginas, ano, id):
    if not titulo:
        print('Faltou informa o titulo.')
        return
    if not autor:
        print('Faltou informa o autor.')
        return
    if not paginas:
        print('Faltou informa as páginas.')
        return
    if not ano:
        print('Faltou informa o ano.')
        return
    if not id:
        print('Faltou informa o id.')
        return

    #INFO: Verifica se tem um livro com o mesmo ID.
    if verificar_livro(id):
        return

    livro_ref = db.collection('livros').document(id)
    livro_ref.set({
        'titulo': titulo,
        'autor': autor,
        'paginas': paginas,
        'ano': ano,
        'id': id
    })
    print(f'Livro {titulo} criado com sucesso!')

def listar_livros():
    livros_ref = db.collection('livros')
    return livros_ref.stream()

def atualizar_livro(id, titulo=None, autor=None, paginas=None, ano=None):
    if not verificar_livro(id): #INFO: verifica se o livro existe.
        print(f'Esse livro com o id {id} não existe.')
        return

    livro_ref = db.collection('livros').document(id)
    atualizar = {}
    if titulo:
        atualizar['titulo'] = titulo
    if autor:
        atualizar['autor'] = autor,
    if paginas:
        atualizar['paginas'] = paginas,
    if ano:
        atualizar['ano'] = ano
    if atualizar:
        livro_ref.update(atualizar)
        print(f'Livro {id} atualizado com sucesso!')
    else:
        print('Nada para atualizar.')

def deletar_livro(id):
    livro_ref = db.collection('livros').document(id)
    livro_ref.delete()
    print(f'Livro {id} deletado com sucesso!')
