from PyQt5 import uic, QtWidgets
import mysql.connector


def connection():

    conn = mysql.connector.connect (
        host = "localhost",
        user = "root",
        password = "12341234",
        database = "db_produtos"
    )
    return conn

def funcao_login():
    
    usuario = login.lineEdit.text()
    senha = login.lineEdit_2.text()
    login.label_4.setText("")

    conn = connection()

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT senha_login, id_login FROM tb_login WHERE email_login = '{}'".format(usuario))
        senha_bd = cursor.fetchall()
        print(f"Senha no banco: {senha_bd[0][0]}")

        id_login = int(senha_bd[0][1])

        cursor.execute("SELECT email_login, id_login FROM tb_login WHERE senha_login = '{}'".format(senha))
        user_db = cursor.fetchall()
        print(f'Usuario no banco: {user_db[0][0]}')


        if senha == senha_bd[0][0] and usuario == user_db[0][0]:

            login.lineEdit_2.setText("")
            login.label_4.setText("")
            menu.show()
            login.close()
    
        
        elif senha != senha_bd[0][0]:
            
            login.label_4.setText("Login ou senha incorretos!")
        
    except:
        id_login = 0
        login.label_4.setText("Login ou senha incorretos!")

    return login

def funcao_cadastrar():
    linha1 = cadastro.lineEdit.text()
    linha2 = cadastro.lineEdit_2.text()
    linha3 = cadastro.lineEdit_3.text()
    
    conn = connection()

    categoria = ''

    if cadastro.radioButton.isChecked():
        print('Categoria Informática foi selecionada')
        categoria = 'Informática'
    elif cadastro.radioButton_2.isChecked():
        print('Categoria Alimentos foi selecionada')
        categoria = 'Alimentos'
    else:
        print('Categoria Eletronicos foi selecionada')
        categoria = 'Eletronicos'



    print('Codigo:', linha1)
    print('Descrição:', linha2)
    print('Preço:', linha3)

    cursor = conn.cursor()
    comando_SQL = 'INSERT INTO tb_produtos (codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)'
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    conn.commit()
    cadastro.lineEdit.setText('')
    cadastro.lineEdit_2.setText('')
    cadastro.lineEdit_3.setText('')

def mostrar_dados():


    conn = connection()

    segunda_tela.show()

    cursor = conn.cursor()
    comando_SQL = 'SELECT * from tb_produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range (0, len(dados_lidos)):
        for j in range (0, 5):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app= QtWidgets.QApplication([])
login = uic.loadUi('login.ui')
menu = uic.loadUi('menu.ui')
cadastro =uic.loadUi('cadastrar.ui')
segunda_tela =uic.loadUi('listar_produtos.ui')
login.pushButton.clicked.connect(funcao_login)
cadastro.pushButton.clicked.connect(funcao_cadastrar)
cadastro.pushButton_2.clicked.connect(mostrar_dados)

login.show()
app.exec()
