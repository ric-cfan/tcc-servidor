1. Criar um ambiente virtual (recomendado)
Antes de começar, é uma boa prática criar um ambiente virtual para o projeto. Abra o terminal na pasta do projeto e execute o seguinte comando:

python -m venv venv

2. Ativar o ambiente virtual
Para ativar o ambiente virtual:

.\venv\Scripts\activate

3. Instalar dependências
Com o ambiente virtual ativado, instale as dependências necessárias com o comando:

pip install -r requirements.txt

4. Rodar a aplicação
Agora que as dependências estão instaladas, você pode rodar a aplicação. Execute o seguinte comando no terminal:

uvicorn app.main:app --reload