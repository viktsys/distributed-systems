# ChitChat

Uma pequena implementação de um programa de bate-papo rodando em Python3 utilizando sockets TCP para comunicação.

## Protocolo

O protocolo de comunicação é basicamente:

1. Inicia a conexão, o primeiro pacote recebido deverá conter uma string de texto codificada com o padrão UTF-8 que será o `username`
2. A conexão é liberada e qualquer proxima mensagem que chegar irá ser retransmitida aos outros clientes conectados ao servidor
3. Caso um dos comandos especificados seja recebido, o servidor irá respondendo de acordo:

## Comandos

- /usuarios
    Lista todos os usuarios conectados no momento.

- /sair
	Desconecta do servidor informando a todos que o usuário saiu.