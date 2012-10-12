#coding:utf-8
import socket
import time
import os
from diretorio import Diretorio
from settings import *

class Cliente():
	def __init__(self):
		print 'Iniciando Cliente...'
		
		print 'Configurando socket...'
		self.porta = PORTA
		self.socket = socket.socket()
		self.socket.settimeout(1)
		self.servidor = SERVIDOR
		self.porta = PORTA
		
		if os.path.exists(PASTA) == False:
			print 'Criando pasta...'
			os.mkdir(PASTA)
		
		pasta_servidor = self.requisicao('PASTA#')
		
		print 'Configurando Cliente...'
		self.diretorio = Diretorio(self.servidor, PASTA, pasta_servidor, USUARIO, SENHA)
		
		print 'Configuração completa!'

	def requisicao(self, mensagem):
		self.socket = socket.socket()
		self.socket.connect((self.servidor, self.porta))
		self.socket.sendall(mensagem)
		resposta = self.read(self.socket)
		self.socket.close()
		return resposta

	def read(self, socket):
		msg = []
		while True:
			temp = socket.recv(1)
			if temp == '#':
				break
			msg.append(temp)
		return ''.join(msg)

cli = Cliente()
'''
while True:
	print cli.diretorio.comparar_arquivos()
	time.sleep(5)
'''
resposta = cli.requisicao('PRIMEIRA#')
if resposta == 'OK':
	print 'Sincronizando pasta do cliente'
	cli.diretorio.sincrozinar_cliente()
	print 'Sincronização completa'
	print
	print
	time.sleep(5)

while True:
	update = cli.diretorio.comparar_arquivos()
	print 'Novos arquivos {0}'.format(update)
	if update == True:
		print 'Pedindo atualização'
		resposta = cli.requisicao('ATUALIZAR#')
		if resposta == 'ATUALIZE':
			print 'OK, atualizar servidor'
			cli.diretorio.sincronizar_servidor()
			cli.diretorio.sincrozinar_cliente()
			cli.requisicao('COMPLETA#')
	else:
		resposta = cli.requisicao('NOVIDADE#')
		print 'Novidade? {0}'.format(resposta)
		if resposta == 'SIM':
			cli.diretorio.sincrozinar_cliente()
			resposta = cli.requisicao('COMPLETA#')
			print 'lol'
		print
		print
		time.sleep(5)