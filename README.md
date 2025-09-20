<h1 align="center" id="title">sozinho</h1>
<h3 align="center""><strong>sozinho® é uma ferramenta modular focada em automatizar qualquer pesquisa em fontes públicas (OSINT), com foco total no Brasil</strong></h3>
<hr>

<p align="center"><img src="assets/crying.png" width=350/></p><br>

> essa ferramenta é um protótipo do começo ao fim e tem o objetivo de ser experimental e uma base de aprendizado para um projeto que planejo para o futuro.
> por esse e outros motivos (sou noob), estará sujeita a grandes mudanças durante o seu desenvolvimento.
<hr>


<h1 align="center">Formas de uso</h2>

- É possível utilizar a ferramenta no console, selecionando e interagindo com os módulos livremente
> usando o help, é possível entender como todos os comandos disponiveis funcionam
```
$ python3 sozinho.py
```
<hr>
<p align="center"><img src="assets/tool_1.png"></p>

```
> help
Documented commands (type help <topic>):
========================================
exit  help  run  select  set  show

```

<p align="center"><img src="assets/tool_2.png"></p>

```
> select escavador
escavador> show arguments
set <função> <argumento(s)>
```
<p align="center"><img src="assets/tool_3.png"></p><hr>

- ou, caso preferir, diretamente pela linha de comando
```
$ python3 modules/escavador.py --help
```
<p align="center"><img src="assets/tool_4.png"></p><hr>

<h1 align="center">Instalação</h1>

```
$ git clone https://github.com/evildocument/sozinho.git
$ cd ./sozinho
$ pip3 install -r requirements.txt
```
