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
		Class cliente.
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
				print 'Erro ao criar pasta.'
				sys.exit()
		
		pasta_servidor = self.requisicao('PASTA#')
		pasta_temporaria = self.requisicao('PASTA_TEMP#')

		print 'Configurando Cliente...'
		self.diretorio = Diretorio(self.servidor, PASTA, pasta_servidor, pasta_temporaria, USUARIO, SENHA)
		
		print 'Configuração completa!'

	def requisicao(self, mensagem):
		self.socket = socket.socket()

		try:
			self.socket.connect((self.servidor, self.porta))
		except socket.error:
			print 'Não foi possível conectar com o servidor.'
			sys.exit()
			
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

	def start(self):
		resposta = self.requisicao('PRIMEIRA#')
		if resposta == 'OK':
			print 'Sincronizando pasta do cliente...'
			self.diretorio.sincrozinar_cliente()
			time.sleep(5)

		while True:
			update = self.diretorio.novos_arquivos()
			if update == True:
				resposta = self.requisicao('ATUALIZAR#')
				if resposta == 'ATUALIZE':
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
				time.sleep(5)

