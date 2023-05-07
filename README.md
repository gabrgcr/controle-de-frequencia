# Controle de Frequência
Sistema de Controle de Frequência para o Projeto Integrador I do Eixo de Computação da UNIVESP. Desenvolvido em Python com Framework Flask.

## Introdução
O sistema tem como objetivo ser de simples funcionamento e fácil utilização. Visa ser um sistema prático para gerenciamento de frequência em uma escola, podendo cadastrar turmas, alunos, professores, diretores e responsáveis, visando um maior controle da comunidade escolar à frequencia dos alunos. Ao fim de um dia letivo na sala de aula, o professor faz o controle de frequência, e, na ausência de um aluno, é gerado um alerta para a direção, que entrará em contato com os responsáveis do aluno.

## Desenvolvimento
O sistema foi desenvolvido utilizando Python e framework Flask, Bulma CSS e Supabase. O deploy foi feito com Vercel.

## Instalação
Para fazer a instalação local, é necessária a instalação do [Python mais recente](https://www.python.org/downloads/) e do [PostgreSQL](https://www.postgresql.org/download/) em sua máquina, primeiramente.

Após isso, é necessário o download do código, a partir de um Git Clone do repositório.

É necessária a criação de uma conexão de banco de dados, seu usuário e senha. Para maior facilidade, o banco de dados deve rodar na porta 6543. Caso rode em outra porta, será necessária a mudança da porta no arquivo database.py. Após essa criação, rodar o SQL DDL em creation_db.sql localizado na raíz do projeto.

Com o projeto aberto em sua IDE, é necessária a instalaçao das dependencias localizadas no arquivo Requirements.txt.
Por fim, deve ser rodado o arquivo app.py do projeto, com a variável de ambiente DATABASE_URL com a URL de seu db.

### Aplicação

Seguem prints de algumas telas da aplicação para referência:

![Criação de Turmas](https://imgur.com/TAkvRLN)

![Iniciar Dia Letivo](https://imgur.com/VCa0F2e)

![Lista de Frequência](https://imgur.com/zvROXIA)

![Avisos de Ausência](https://imgur.com/IcLcC2q)
