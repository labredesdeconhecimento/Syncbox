#coding:utf-8
import socket
import threading
import os
import time
import subprocess
import sys
from settings import *


class Servidor():
    '''
        Classe Servidor.
        Todas as funcionalidades do servidor synbox estão nessa classe.

        O servidor é responsável por gerenciar todos os clientes, e reponder
        todas as requisições dos clientes.

        Em um determinado intervalo de tempo, o cliente "pergunta" ao servidor
        se existem novos arquivos, o servidor verifica a pasta onde os
        arquivos que vão ser sincronizados estão, caso haja mudança
        desde a ultima atualização do cliente, o servidor responde ao cliente
        que o mesmo deve fazer uma sincronização de dados.

        Todas as sincronizações são feitas apenas depois da autorização
        do servidor.
    '''
    def __init__(self):
        print 'Iniciando servidor...'

        print 'Configurando socket...'
        self.porta = PORTA

        try:
            self.socket = socket.socket()
            self.socket.bind(('', self.porta))
            self.socket.listen(1)
        except:
            sys.stderr.write('Não foi possível abrir o socket.')
            sys.exit()

        print 'Configurando outras opções do servidor...'
        self.clientes = {}

        if os.path.exists(PASTA_SERVIDOR) == False:
            print 'Criando pasta...'

            try:
                os.mkdir(PASTA_SERVIDOR)
            except:
                sys.stderr.write('Não foi possível criar a pasta.\n')
                sys.exit()

        print 'Configuração completa!'
        print 'Servidor funcionando!'

    def start(self):
        '''
            Método responsável por escutar o socket e esperar conexões
            nesse socket.

            Quando um cliente se conecta no servidor, uma thread é lançada
            para cuidar das requisições do cliente conectado, e esse
            método volta a escutar o socket aguardando novas conexões.

            O uso de threads nessa parte do software é fundamental
            para o servidor ser capaz de atender vários clientes
            paralelamente.
        '''
        while True:
            con, cli = self.socket.accept()
            threading.Thread(target=self.escuta_cliente, args=(con,)).start()
            time.sleep(1)

    def escuta_cliente(self, cliente):
        '''
            Método responsável por atender as requisições de um cliente
            já conectado no servidor.

            Requisições:

            PRIMEIRA = Indica que o cliente está iniciando agora e faz seu
            primeiro contato com o servidor. O servidor inclui ou atualiza
            o cliente em um dicionário. O cliente sincroniza os dados do
            lado do cliente com os dados do lado do servidor.

            ATUALIZAR = O cliente informa ao servidor que irá sincronizar os
            dados do lado do servidor com os dados do lado do cliente.

            COMPLETA = O cliente informa ao servidor que acabou seu processo
            de sincronização. O servidor atribui ao cliente seu novo tempo
            de sincronização e atualiza o servidor com o novo último tempo
            de sincronização dos dados do servidor.

            NOVIDADE = O cliente procura saber com o servidor se aconteceu
            alguma sincronização desde a última sincronização que ele fez.
            O servidor compara sua última marca de tempo com a marca do cliente
            e responde se o cliente tem ou não que atualizar seu dados.

            PASTA= O cliente pede ao servidor informações sobre o caminho da
            pasta onde o servidor está guardado os dados, para que esse caminho
            possa ser configurado no mecanismo de sincrinização.

            OBS: Em cada resposta é usado um símbolo "#" para definir o final
            da string.
        '''
        opcao = self.read(cliente)

        if opcao == 'PRIMEIRA':
            self.send(cliente, 'OK#')
            if self.clientes.has_key(cliente.getpeername()[0]) == False:
                self.clientes[cliente.getpeername()[0]] \
                = os.path.getmtime(PASTA_SERVIDOR)

        elif opcao == 'ATUALIZAR':
            if os.path.getmtime(PASTA_SERVIDOR) != (
                self.clientes[cliente.getpeername()[0]]):
                self.send(cliente, 'SEMDELETE#')
            else:
                self.send(cliente, 'ATUALIZE#')

        elif opcao == 'COMPLETA':
            self.clientes[cliente.getpeername()[0]] = os.path.getmtime(PASTA_SERVIDOR)
            self.send(cliente, 'OK#')

        elif opcao == 'NOVIDADE':
            if os.path.getmtime(PASTA_SERVIDOR) != (
                self.clientes[cliente.getpeername()[0]]):
                self.send(cliente, 'SIM#')
            else:
                self.send(cliente, 'NAO#')
        elif opcao == 'PASTA':
            self.send(cliente, '{0}#'.format(PASTA_SERVIDOR))

        elif opcao == 'PASTA_TEMP':
            temp = self.gerar_pasta_temporaria(cliente.getpeername()[0])
            self.send(cliente, '{0}#'.format(temp))
        cliente.close()

    def read(self, cliente):
        '''
            Método responsável por ler as mensagens dos clientes para
            o servidor.

            Recebe como parâmetro o socket do cliente que está enviando
            a mensagem.
        '''
        msg = []
        while True:
            temp = cliente.recv(1)
            if temp == '#':
                break
            msg.append(temp)
        return ''.join(msg)

    def send(self, cliente, mensagem):
        '''
            Método responsável por enviar mensagens do servidor
            para os clientes.

            Recebe como parâmetro um socket do cliente que vai
            receber a mensagem e a mensagem que vai ser enviada.
        '''
        try:
            cliente.send(mensagem)
        except:
            sys.stderr.write('Não foi possível responder o cliente.\n \
            problema com o socket.')
            sys.exit()

    def gerar_pasta_temporaria(self, ip):
        '''
            Método que gera uma pasta para cada cliente onde
            os arquivos em transferência ficam armazenados
            temporariamente.
        '''
        pasta = ip.replace('.', '-')
        pasta = '{0}/.{1}'.format(PASTA_SERVIDOR, pasta)
        if os.path.exists(pasta) == False:
            os.mkdir('{0}'.format(pasta))
        return pasta
