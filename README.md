Luiza Labs Favorites API
---

Este projeto tem por finalidade criar e consumir uma API REST na qual é possível cadastrar e consultar usuários, produtos e adicionar produtos à uma lista de favoritos.

Necessita autenticação para alguns endpoints que deve ser feito por meio de um header "Authorization: Token <valor>" após requisitar acesso.

Documentação da api disponível em http://localhost:5000 via docker-compose, ou importando o arquivo "documentation/insomnia/insonmnia.json" no Insomnia REST Client.

## Quickstart

### Utilizando docker-compose
```
* Tenha instalado docker (ou docker desktop) e docker-compose (v1.13.0+)
* Certifique que as portas `8000`, `5432` e `5000` de seu computador estejam liberadas
* Clone o repositório
* Execute `docker-compose build && docker-compose up -d`
* A API será acessível via `http://localhost:8000`
* O Banco de dados será acessível via `http://localhost:5432`
* A documentação da API será acessível em `http://localhost:5000`
* Para cancelar a execução da stack, utilize `docker-compose down`
```


## Configurando Backend em Django

### Requisitos:
  - Python >= versão 3.6
  - PostgreSQL >= versão 10

### Como preparar o projeto
#### Postgres:

Criar uma base postgres com nome `luizalabsdb`. Em seguida alterar, dentro do arquivo `src/magalu_favorites/settings.py`, os valores do dicionário "DATABASES" de acordo com a necessidade.
Por padrão, são chamadas variáveis de ambiente, disponíveis em "setup/prod.env" para desenvolvimento local
É possível utilizá-las no pycharm por meio de um plugin chamado envfile.

As chaves e valores são as seguintes:
- **NAME**: nome da database em postgres (padrão: 'luizalabsdb')
- **USER**: nome do usuário dono da base (padrão: 'postgres')
- **PASSWORD**: senha do usuário dono da base postgres (padrão: 'labs2021')
- **HOST**:  URL do local da base (padrão: 'localhost')
- **PORT**:  porta alocada para acessar a database no host (padrão: '5432')

Lembrando que é possível iniciar uma base postgres já com as configurações padrões via docker seguindo as instruções do quickstart

#### Python/Django:

Instalar python versão igual ou superior a 3.6.
Verificar instalação do Pip, utilizando o comando `python3 -m pip --version`. 
Caso o pip não esteja instalado, instalar usando: `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` e após, `python3 get-pip.py`

Instale as dependências do projeto utilizando `python3 -m pip install -r setup/requirements.txt`.
Verifique se as dependências foram corretamente instaladas com `python3 -m pip freeze`. Caso os mesmos nomes do arquivo requirements.txt estejam na saída do comando executado acima, está tudo certo.

Execute `python3 src/manage.py migrate` para aplicar todas as mudanças no banco de dados necessário para rodar a aplicação.
Após aplicar os migrations, execute `python3 src/manage.py loaddata initial_data.json` para carregar no banco de dados, informações pré cadastradas. Por padrão é criado um superusuário do Django com:
 - **Username**: gabrielgomesnogueira@gmail.com
 - **Password**: gabrielgn

Com todos os passos realizados, execute o servidor django com `python3 src/manage.py runserver 0:8000`, que iniciará na máquina do usuário um servidor de rede interna na porta 8000 para ser consumido.

Para verificar as informações cadastradas no banco de dados, acesse `http://localhost:8000/admin` e forneça as credenciais acima (username: `gabrielgomesnogueira@gmail.com` password: `gabrielgn`).

Para criar dados falsos aleatórios na base, utilize `python3 src/generate_fake_data.py` 

## Para acessar a documentação da API via Insomnia

* Utilizar Insomnia Rest Client v2021.3.0+
* Na interface do programa, clique sobre o logo "Dashboard/Insomnia"
* Selecione Import/Export
* Na aba "Data" selecione "Import Data" e em seguida "From File"
* Escolha o arquivo `Insomnia.json` localizado em `documentation/insomnia`

Ao ter sucesso, as requisições devem estar disponíveis na barra lateral à esquerda.

Ao clicar sobre uma requisição, ela já estará montada, e a documentação dela pode ser acessada na aba "Docs", abaixo da barra de endereço da requisição.

**IMPORTANTE**: As chamadas que necessitam autenticação devem ter tokens válidos! Para isso, utilize a chamada "Token de autenticação" dentro da pasta "Autenticação" disponível no insomnia

## Últimas notas

Muito do desenvolvimento desta API poderia ter sido incrivelmente simplificada utilizando views, mixins e funções já prontas do framework Django Rest Framework.

A motivação de não utilizar apenas o rest framework foi mostrar como desenvolver lógica própria nas views, caso seja necessário personalizar as funções já prontas que o framework oferece.

Qualquer dúvida sobre lógica, código ou desenvolvimento estou à disposição!