# Como executar

É recomendado utilizar um ambiente virtual para executar o projeto. Passos para criar e começar a usar um ambiente virtual com Python:

1. Criar o ambiente
    > py -m venv .venv

2. Ativar o ambiente virtual
    - Se windows:
        > .venv/Scripts/activate

    - Se unix:
        > source .venv/bin/activate

## Projeto

1. Rodar 
    > make

2. Rodar 
    > make run_server

3. Em um novo terminal, rodar: 
    > make run_app

O aplicativo será executado no seguinte endereço: http://127.0.0.1:5000

**OBS**: Se estiver utilizando o ambiente virtual, lembrar de ativar o ambiente virtual em ambos os terminais