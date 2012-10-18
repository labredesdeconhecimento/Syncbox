Syncbox
=======

Syncbox é uma aplicação para sincronização de arquivos entre computadores diferentes. É usado
um servidor para centralizar os arquivos e coordenar o processo de sincronização.

Todas as transferência de arquivos são monitoradas pelo servidor. É utilizado o Rsync
para fazer todas as tranferências de arquivos, todos pacotes de arquivos sendo 
transferidos são criptografados.

A comunicação entre clientes e servidor é feita via socket TCP.

Para o funcionamento é necessário um servidor rodando (para centralizar e coordenar
todas as ações) e N clientes conectados a esse servidor.


Autor: Thiago Dias da Silva

Email: thiagodd.silva@gmail.com

Data: 16/10/2012

Dependência:
    Rsync: http://www.samba.org/ftp/rsync/rsync.html

    sshpass: http://sourceforge.net/projects/sshpass/
