#coding:utf-8
import os
import subprocess
import sys
from settings import *


class Diretorio():
    '''
        A classe Diretório é responsável por detectar mudanças
        no diretório onde estão os arquivos do cliente e iniciar
        os comando necessários para atualização tanto do cliente
        quanto do servidor na hora que for preciso.


        Estrutura do comando RSYNC:

        São utilizados três tipos de comando RSYNC para atualização
        do arquivos:

        - Sincroniza servidor:
            Utilizado para sincronizar os arquivos do servidor:
                rsync -arzp --delete --exclude=.* -T [diretório temporário]
                --delay-updates --partial-dir=[diretório temporário]
                [diretório do cliente] [login servidor]@[endereço servidor]:/
                [diretório do servidor]/
        - Sincroniza cliente:
            Utilizado para sincronizar os arquivos do cliente:
                rsync -arzp --delete --exclude=.* [login servidor]@
                [endereço servidor]:/[diretório do servidor]/
                [diretório do cliente]
        - Sincroniza cliente sem delete:
            Utilizado para sincronizar os arquivos do cliente sem deletar
            arquivos que estão no cliente e não estão no servidor:
                rsync -arzp --exclude=.* [login servidor]@
                [endereço servidor]:/[diretório do servidor]/
                [diretório do cliente]

            Argumentos Rsync:

            -a: Garante a recursão na hora da verificação dos arquivos.

            -r: Faz com que o Rsync procure arquivos recursivamente dentro
                dos diretórios do diretório indicado.

            -z: Faz com que o Rsync faça uma compressão dos arquivos antes
                de fazer o envio deles.

            -p: Preserva a permissão dos arquivos.

            --exclude=.*: Não transfere nenhum arquivo oculto.

            -T [dir]: Indica uma pasta temporária para guardar o arquivo
                      que está sendo transferido.

            --delay-updates: Indica que todos os arquivos que estão sendo
                             transferidos naquela transação devem ficar na
                             pasta indica com --partial-dir= até toda a
                             transação ser concluída.

            --partial-dir=[dir]: Indica onde os arquivos ficarão até o fim
                                 da transação.
    '''
    def __init__(self, servidor, pasta, pasta_servidor,
                pasta_temporaria, usuario, senha):
        self.servidor = servidor
        self.pasta_servidor = pasta_servidor

        self.pasta = pasta
        self.usuario = usuario
        self.senha = senha

        self.ultima_modificacao = os.path.getmtime(self.pasta)
        print self.ultima_modificacao

        self.sincroniza_servidor = 'sshpass -p {0} rsync -arzp --delete \
            --exclude=.* -T {1} --delay-updates --partial-dir={1} \
            {2}/ {3}@{4}:{5}/'.format(self.senha, pasta_temporaria,
            self.pasta, self.usuario, self.servidor, self.pasta_servidor)

        self.sincroniza_cliente = 'sshpass -p {0} rsync -arzp --delete \
            --exclude=.* {2}@{3}:{4}/ {1}/ '.format(self.senha, self.pasta,
            self.usuario, self.servidor, self.pasta_servidor)

        self.sincroniza_cliente_sem_delete = 'sshpass -p {0} rsync -arzp \
            --exclude=.* {2}@{3}:{4}/ {1}/ '.format(self.senha, self.pasta,
            self.usuario, self.servidor, self.pasta_servidor)

    def sincronizar_servidor(self):
        '''
            Método que executa o comando rsync para atualizar o servidor.
        '''
        try:
            subprocess.check_output(self.sincroniza_servidor.split())
        except subprocess.CalledProcessError:
            sys.stderr.write('Erro Rsync')

    def sincrozinar_cliente(self):
        '''
            Método que executa o comando rsync para atualizar o cliente.
        '''
        try:
            subprocess.check_output(self.sincroniza_cliente.split())
        except subprocess.CalledProcessError:
            sys.stderr.write('Erro Rsync')

    def sincronizar_cliente_sem_delete(self):
        '''
            Método que executa o comando rsync para atualizar
            o cliente sem delete.
        '''
        try:
            subprocess.check_output(self.sincroniza_cliente_sem_delete.split())
        except subprocess.CalledProcessError:
            sys.stderr.write('Erro Rsync')

    def novos_arquivos(self):
        '''
            Método que detecta se houve mudança nos arquivos do cliente.
        '''
        temp = os.path.getmtime(self.pasta)
        if temp != self.ultima_modificacao:
            self.ultima_modificacao = temp
            return True
        else:
            return False
