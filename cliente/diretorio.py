#coding:utf-8
import os
import time
import subprocess
import sys
from settings import *

class Diretorio():
	def __init__(self, servidor, pasta, pasta_servidor, pasta_temporaria, usuario, senha):
		self.servidor = servidor
		self.pasta_servidor = pasta_servidor

		self.pasta = pasta
		self.usuario = usuario
		self.senha = senha
		
		self.arquivos = []
		self.carregar_arquivos()

		self.ultima_modificacao = os.path.getmtime(self.pasta)
		print self.ultima_modificacao

#		self.sincroniza_servidor = 'sshpass -p {0} rsync -arzp --delete --filter=P_.* {1}/ {2}@{3}:{4}/'.format(self.senha, self.pasta, self.usuario, self.servidor, self.pasta_servidor)

		self.sincroniza_servidor = 'sshpass -p {0} rsync -arzp --delete --exclude=.* -T {1} --delay-updates --partial-dir={1} {2}/ {3}@{4}:{5}/'.format(self.senha, pasta_temporaria, self.pasta, self.usuario, self.servidor, self.pasta_servidor)
		self.sincroniza_cliente = 'sshpass -p {0} rsync -arzp --delete --exclude=.* {2}@{3}:{4}/ {1}/ '.format(self.senha, self.pasta, self.usuario, self.servidor, self.pasta_servidor)


	def sincronizar_servidor(self):
		subprocess.check_output(self.sincroniza_servidor.split())

	def sincrozinar_cliente(self):
		try:
			subprocess.check_output(self.sincroniza_cliente.split())
		except subprocess.CalledProcessError:
			print 'Erro na chave Rsync'
			print 'Abra uma conexão SSH com o servidor.'
			sys.exit()


	def carregar_arquivos(self):
		if os.path.exists(self.pasta):
			for caminho, nome, arquivos in os.walk(self.pasta):
				for arquivo in arquivos:
					nome_arquivo = '{0}/{1}'.format(caminho, arquivo)
					edicao_arquivo = os.path.getmtime(nome_arquivo)
					self.arquivos.append((nome_arquivo, edicao_arquivo))
		else:
			os.mkdir(self.pasta)

	def listar_arquivos(self):
		lista_temporaria = []
		for caminho, nome, arquivos in os.walk(self.pasta):
			for arquivo in arquivos:
				nome_arquivo = '{0}/{1}'.format(caminho, arquivo)
				edicao_arquivo = os.path.getmtime(nome_arquivo)
				lista_temporaria.append((nome_arquivo, edicao_arquivo))
		return lista_temporaria

	def comparar_arquivos(self):
		print self.arquivos
		alteracao = False
		lista_temporaria = self.listar_arquivos()
		if len(self.arquivos) != 0:
			for arquivo in self.arquivos:
				if arquivo not in lista_temporaria:
					print 'Alteração detectada, sincronizando os arquivos do servidor.'
					self.arquivos = lista_temporaria
					return True
			for arquivo in lista_temporaria:
				if arquivo not in self.arquivos:
					print 'Alteração detectada, sincronizando os arquivos do servidor.'
					self.arquivos = lista_temporaria
					return True				
		else:
			if len(lista_temporaria) > 0:
				self.arquivos = lista_temporaria
				return True
		
		self.arquivos = lista_temporaria
		return False

	def novos_arquivos(self):
		temp = os.path.getmtime(self.pasta)
		if temp != self.ultima_modificacao:
			self.ultima_modificacao = temp
			return True
		else:
			return False
