import os
from dotenv import load_dotenv
import yfinance as yf
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_core.tools import Tool

# --- 1. Configuração Inicial ---
load_dotenv() # Carrega a API Key do .env

# --- 2. Definição das Funções (Lógica de Mercado) ---

def get_stock_price(symbol: str):
    """Consulta o preço atual de um ativo via Yahoo Finance."""
    ticker = yf.Ticker(symbol.upper().strip())
    price = ticker.fast_info.last_price
    
    # Fallback para histórico se fast_info falhar
    if price is None:
        hist = ticker.history(period="1d")
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            
    return f"R$ {price:.2f}" if price else "Preço não disponível."

def get_stock_fundamentals(symbol: str):
    """Retorna indicadores fundamentalistas principais."""
    info = yf.Ticker(symbol.upper().strip()).info
    return (
        f"Setor: {info.get('sector', 'N/A')}\n"
        f"P/L: {info.get('trailingPE', 'N/A')}\n"
        f"Div. Yield: {info.get('dividendYield', 0)*100:.2f}%\n"
        f"Recomendação: {info.get('recommendationKey', 'N/A')}"
    )

# --- 3. Configuração das Ferramentas (LangChain) ---
tools = [
    Tool(
        name="Consultar_Preco",
        func=get_stock_price,
        description="Retorna o preço atual de uma ação (ex: PETR4.SA)."
    ),
    Tool(
        name="Consultar_Fundamentos",
        func=get_stock_fundamentals,
        description="Retorna dados como P/L e Dividendos (ex: VALE3.SA)."
    )
]

# --- 4. Inicialização do Agente ---
# Modelo LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Prompt ReAct (Raciocínio + Ação)
prompt = hub.pull("hwchase17/react")

# Criação do Executor
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- 5. Loop Principal ---
print("Price Trader Check Iniciado. (Digite 'sair' para encerrar)")
print("Ex: 'Preço da VALE3.SA' ou 'Analise BBAS3.SA' ")

while True:
    user_input = input("\nVocê: ")
    if user_input.lower() in ['sair', 'x']:
        break
        
    agent_executor.invoke({"input": user_input})