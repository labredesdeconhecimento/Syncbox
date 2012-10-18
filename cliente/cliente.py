#coding:utf-8
import socket
import time
import os
import sys
import platform
from diretorio import Diretorio
from settings import *


class Cliente():
    '''
        A classe Cliente é reponsável por manipular todas as funções
        que os clientes desempenham.

        A classe Cliente detecta mudanças nos arquivos da pasta selecionada
        e faz todos procedimentos para atualizar o servidor e quando necessário
        atualizar seus arquivos.

        Atualizações nos arquivos do cliente ou nos arquivos do servidor só
        são lançadas após a autorização do servidor.
    '''
    def __init__(self):
        print 'Iniciando Cliente...'

        print 'Configurando socket...'
        self.porta = PORTA
        self.socket = socket.socket()
        self.servidor = SERVIDOR

        if os.path.exists(PASTA) == False:
            print 'Criando pasta...'
            try:
                os.mkdir(PASTA)
            except OSError:
                sys.stderr.write('Erro ao criar pasta.')
                sys.exit()

        pasta_servidor = self.requisicao('PASTA#')
        pasta_temporaria = self.requisicao('PASTA_TEMP#')

        print 'Configurando Cliente...'
        self.diretorio = Diretorio(self.servidor, PASTA, pasta_servidor,
        pasta_temporaria, USUARIO, SENHA)

        print 'Configuração completa!'

    def requisicao(self, mensagem):
        '''
            Método para enviar uma requisição para o servidor
            e retornar a resposta do servidor.

            Argumento: Mensagem para ser enviada para o servidor.
        '''
        self.socket = socket.socket()

        try:
            self.socket.connect((self.servidor, self.porta))
        except socket.error:
            sys.stderr.write('Não foi possível conectar com o servidor.')
            sys.exit()

        self.socket.sendall(mensagem)
        resposta = self.read(self.socket)
        self.socket.close()
        return resposta

    def read(self, socket):
        '''
            Método que lê o fluxo de dados do socket.

            Argumento: Socket que recebe o fluxo.
        '''
        msg = []
        while True:
            temp = socket.recv(1)
            if temp == '#':
                break
            msg.append(temp)
        return ''.join(msg)

    def start(self):
        '''
            Método que inicia o cliente.

            Quando uma alteração nos arquivos é detectada, o cliente
            manda para o servidor uma mensagem pedindo autorização
            para fazer a atualização dos dados do servidor.

            O cliente manda uma mensagem para o servidor perguntado
            se houve alteração nos arquivos do servidor desde a
            última atualização do cliente. Caso seja constado que
            os arquivos do cliente não são os mais atuais, o cliente
            atualiza seus arquivos.

            Em um intervalo de tempo determinado todas essas ações
            são realizadas.
        '''
        resposta = self.requisicao('PRIMEIRA#')
        if resposta == 'OK':
            print 'Sincronizando pasta do cliente...'
            self.diretorio.sincrozinar_cliente()
            time.sleep(5)

        while True:
            update = self.diretorio.novos_arquivos()
            if update == True:
                resposta = self.requisicao('ATUALIZAR#')
                if resposta == 'SEMDELETE':
                    print 'Atualizando arquivos..'
                    self.diretorio.sincronizar_cliente_sem_delete()
                    self.diretorio.sincronizar_servidor()
                    self.diretorio.sincrozinar_cliente()
                    self.requisicao('COMPLETA#')
                    print 'Arquivos atualizados!'
                elif resposta == 'ATUALIZE':
                    print 'Atualizando arquivos...'
                    self.diretorio.sincronizar_servidor()
                    self.diretorio.sincrozinar_cliente()
                    self.requisicao('COMPLETA#')
                    print 'Arquivos atualizados!'
            else:
                resposta = self.requisicao('NOVIDADE#')
                if resposta == 'SIM':
                    print 'Atualizando arquivos...'
                    self.diretorio.sincrozinar_cliente()
                    self.requisicao('COMPLETA#')
                    print 'Arquivos atualizados!'
            time.sleep(2)
