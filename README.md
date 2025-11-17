# APS rag 17/11/2025
## ALUNOS:
- JOAO VITOR APARECIDO SILVA
- LUCAS HENRIQUE FERREIRA AMARAL

## Criar e ativar o venv
- python3 -m venv .venv
- source .venv/bin/activate
## Instalar as dependencias
- pip install -r requirements.txt
## Executar o agente
- python agente.py
## Perguntas de exemplos
- Qual o preço da VALE3
- Faça uma analise da PETR4

## Configurar chave de api e git-ignore
- echo "GOOGLE_API_KEY= ->CHAVE_AQUI<- " > .env
- echo ".env" > .gitignore
- echo ".venv" >> .gitignore
- echo ".env.swp" >> .gitignore
