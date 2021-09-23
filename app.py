from flask.app import Flask
from flask.templating import render_template
from flask_socketio import SocketIO, emit, send
import random
from operator import itemgetter, attrgetter
import os

app = Flask(__name__)
io = SocketIO(app)

pacientes = []
novo_arquivo = ""

"""
Função que renderiza o front ao servidor ser começado
"""
@app.route("/")
def home():
    return render_template("front.html")

""" recebe o nome do form html e gera os dados aleatorios do oxímetro"""
@io.on('sendMessage')
def send_message_handler(msg):
    global novo_arquivo

    msg["temp"] = round(random.uniform(36.5,39.0),1)
    msg["oximetro"] = random.randint(85, 99)
   
    novo_arquivo = novo_arquivo + str(msg["nome"]) + "|" + str(msg["oximetro"]) + "|" + str(msg["temp"]) + '\n'
    arquivo_escrita = open(os.path.dirname(os.path.realpath(__file__)) + "\\pacientes.txt", 'w')
    arquivo_escrita.write(novo_arquivo)
    arquivo_escrita.close()

    pacientes.append(msg)
    pacientes.sort(key=mysort)


"""
Recebe o nome do front pra exluir ao percorrer o arquivo onde os pacientes estão salvos
"""
@io.on('sendNameDelete') 
def send_name_delete(msg):
    with open("pacientes.txt", "r") as f:
        lines = f.readlines()
    with open("pacientes.txt", "w") as f:
        for line in lines:
            conteudo = line.split('|')
            if str(conteudo[0]) != str(msg["nome"]):
                f.write(line)

"""
Função usada para ordenar a lista de pacientes pela ordem de oximetria
"""
def mysort(el):
    return el["oximetro"]

"""
Função que ler o arquivo de parcientes e retorna pro front para ser visualizado na tela
"""
@io.on('message')
def message_handler(msg):
    pacientes = []
    arquivo_leitura = open(os.path.dirname(os.path.realpath(__file__)) + "\\pacientes.txt", 'r')
    for linha in arquivo_leitura:
        conteudo = linha.split('|')
        temp = round(float(conteudo[2]) + random.uniform(-0.2,0.2),1)
        nome = conteudo[0]
        oximetro = int(conteudo[1]) + random.randint(-1, 1)
        pacientes.append({'nome':nome,'oximetro':oximetro, 'temperatura':temp})
        pacientes.sort(key=mysort)
    arquivo_leitura.close()
    send(pacientes)

"""
Execução do projeto com debug que reinicia o servidor sempre que houver alteração no fonte
"""
if __name__ == "__main__":
    io.run(app,host="26.183.98.240",port=5000, debug=True)