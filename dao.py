from models import Jogo, Usuario
# Query para Jogo
SQL_DELETA_JOGO = 'delete from jogo where id = %s'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console from jogo where id = %s'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome=%s, categoria=%s, console=%s where id = %s'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console from jogo'
SQL_CRIA_JOGO = 'INSERT into jogo (nome, categoria, console) values (%s, %s, %s)'

# Query para Usuario
SQL_CRIA_USUARIO = 'INSERT INTO usuario (id,nome,senha) values(%s, %s, %s)'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_DELETA_USUARIO = 'DELTE FROM usuario WHERE id = %s'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET id=%s, nome=%s, senha=%s'


# Criando objeto referente ao Jogo para faciliar o uso do DB
class JogoDao:
    def __init__(self, db):
        self.__db = db
    # Func criada para salvar um jogo
    def salvar(self, jogo):
        cursor = self.__db.connection.cursor()

        if (jogo.id):
            # Caso o jogo existir, apenas update
            cursor.execute(SQL_ATUALIZA_JOGO, (jogo.nome, jogo.categoria, jogo.console, jogo.id))
        else:
            # Caso nao existir, cria um novo jogo
            cursor.execute(SQL_CRIA_JOGO, (jogo.nome, jogo.categoria, jogo.console))
            jogo.id = cursor.lastrowid
        self.__db.connection.commit()
        return jogo

    # Obtem a lista de jogos do DB
    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_JOGOS)
        jogos = traduz_jogos(cursor.fetchall())
        return jogos

    # Busca o jogo pelo id
    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    # Deleta o jogo utilizando id como parametro
    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_JOGO, (id,))
        self.__db.connection.commit()


# Criando o objeto referente ao Usuario para facilitar o uso do DB
class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, usuario):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CRIA_USUARIO, (usuario.id, usuario.nome, usuario.senha))
        self.__db.connection.commit()
        return usuario

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_jogos(jogos):
    def cria_jogo_com_tupla(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    return list(map(cria_jogo_com_tupla, jogos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
