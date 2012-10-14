#coding:utf-8
from datetime import datetime
from settings import *


class Log():
    '''
        Classe responsável por escrever no arquivo
        de log.
    '''
    def __init__(self):
        self.arquivo = ARQUIVO_LOG

    def escrever(self, mensagem):
        '''
            Escreve a mensagem no arquivo de log.
        '''
        try:
            with open(self.arquivo, 'a') as arquivo:
                arquivo.write('{0}  --  {1}\n'.format(datetime.today(), mensagem))
        except:
            sys.stderr('Erro ao escrever log.')
            sys.exit()
