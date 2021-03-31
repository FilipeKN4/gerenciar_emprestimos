# Loan Manager

## Sobre o Projeto

O projeto se chama __Loan Manager__ e consiste em uma API Rest que permite usuários gerenciarem empréstimos bancários e seus respectivos pagamentos. Para a sua construção foram criados dois apps, que são:
* __account:__ utilizado para a criação de contas dos usuários
* __transactions:__ utilizado para a criação dos modelos de transações bancárias (empréstimos e pagamentos).

Além dos dois apps criados existe, por padrão, o app __loan_manager__, criado ao iniciar o projeto.

## Instalação e Execução

Primeiramente, deve-se clonar o repositório para o ambiente local com o comando:

`git clone https://github.com/FilipeKN4/gerenciar_emprestimos.git`

O próximo passo é, dentro da pasta do projeto, rodar o comando:

`docker-compose up --build`

Este comando irá gerar a imagem do projeto com as dependências necessárias, criar os containers referentes ao projeto e ao banco de dados e executá-lo. É necessário utilizar o comando com o parâmetro __--build__ apenas na primeira vez.
Nas próximas vezes, para executar o projeto, deve-se utilizar o comando da seguinte forma:

`docker-compose up`

Ou, para executar em segundo plano:

`docker-compose up -d`

O projeto estará rodando sempre no endereço http://localhost:8000/.

__Obs:__ Para facilitar a execução do projeto, foi mantido no repositório a variável __SECRET_KEY__
do arquivo __settings.py__ com um valor preenchido.

## Testes

Para rodar os testes com o projeto em execução deve-se utilizar o comando:

`docker-compose exec django ./manage.py test`

Ou, para executar os testes e gerar um relatório de cobertura:

`docker-compose exec django coverage run ./manage.py test`

E, para visualizar o relatório de cobertura:

`docker-compose exec django coverage report`

Caso o projeto não esteja em execução, pode-se rodar os testes criando outros containers com os comandos:

`docker-compose run django ./manage.py test`

Ou:

`docker-compose run django coverage run ./manage.py test`

`docker-compose run django coverage report`

## Comandos

Para que se possa utilizar o projeto com alguns usuários iniciais, pode-se executar o comando:

`docker-compose exec django ./manage.py create_first_accounts`

Ou, em um novo container:

`docker-compose run django ./manage.py create_first_accounts`

Caso necessário, é possível excluir todos os usuários utilizando o comando:

`docker-compose exec django ./manage.py delete_all_accounts`

Ou, em um novo container:

`docker-compose run django ./manage.py delete_all_accounts`

## Endpoints

Para a realização da autenticação existe o seguinte endpoint:

```
- /login/ (POST)
```

O app __account__ possui os seguintes endpoints disponíveis:

```
- /account/accounts/ (GET, POST)
- /account/accounts/<pk>/ (GET, PUT, DELETE)
```

O app __transactions__ possui os seguintes endpoints disponíveis:

```
- /loans/ (GET, POST)
- /loans/<pk>/ (GET, PUT, DELETE)
- /loans/<pk>/payments/ (GET)
- /loans/<pk>/outstanding_balance/ (GET)
- /payments/ (GET, POST)
- /payments/<pk>/ (GET, PUT, DELETE)
```
É importante ressaltar que o endpoint __/loans/pk/outstanding_balance/__ fornece a informação do __saldo devedor (outstanding_balance)__ de acordo com o __tipo de juros (interest_type)__, onde:
- juros simples = 1
- juros compostos = 2

## Autenticação

Para realizar a autenticação do projeto é necessário obter um __Token__ de acesso do usuário desejado. Para isso, é necessária a realização de uma requisição __POST__ para o endpoint __/login/__ no seguinte formato:

```
{
    "username": "user@email.com",
    "password": "some_password"
}
```

Com as credenciais informadas corretamente, o resultado será:

```
{
    "token": "some_token"
}
```

Para realizar as requisições no projeto esse token recebido deve ser utilizado nos headers de cada requisição.

## Requisições POST/PUT

O corpo das requisições dos tipos __POST/PUT__ do projeto seguem os seguintes formatos:

- Exemplos de criação/edição de usuários:

```
- /account/accounts/

    {
        "username": "jon@email.com", 
        "email": "jon",
        "password": "123",
        "first_name": "Jon",
        "last_name": "Snow"
    }

- /account/accounts/1/

    {
        "username": "jon_snow@email.com", 
        "email": "jon_snow",
        "password": "1234",
        "first_name": "Jon",
        "last_name": "Snow",
        "is_active": "True"
    }
```

- Exemplos de criação/edição de empréstimos:

```
- /loans/

    {
        'nominal_value': 20000,
        'interest_rate': 5.5,
        'end_date': '20-10-20',
        'bank': 'BRB',
        'client': 'Jon',
        'interest_type': 1
    }

- /loans/1/

    {
        'nominal_value': 25000,
        'interest_rate': 7.5,
        'end_date': '20-11-20',
        'bank': 'BRB',
        'client': 'Jon Snow',
        'interest_type': 1
    }
```

- Exemplos de criação/edição de pagamentos:

```
- /payments/

    {
        'loan': 1, 
        'date': '2021-05-20',
        'value': 5000,
    }

- /payments/1/

    {
        'loan': 1, 
        'date': '2021-06-20',
        'value': 7000,
    }
```

## Bibliotecas Utilizadas

Para a realização desse projeto foram utilizadas as seguintes bibliotecas:

* [Django](https://www.djangoproject.com/)
* [DJango REST framework](https://www.django-rest-framework.org/)
* [Coverage](https://coverage.readthedocs.io/en/coverage-5.5/)
* [django-ipware](https://pypi.org/project/django-ipware/)