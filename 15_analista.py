from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
import os

load_dotenv()

db = SqliteDb(db_file="tmp/data.db")


agent = Agent(
    model=Groq(id="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY")),
    name="analista_financeiro",
    tools=[YFinanceTools()],
    instructions="Você é um analista e tem diferentes clientes. Lembre-se de cada cliente, suas informações e preferências.",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    update_memory_on_run=True,
    add_memories_to_context=True,
    enable_agentic_memory=True
)


#agent.print_response("Olá, prefiro respostas em formato de tabela, gosto de poucas informações.", session_id="apple_session_1", user_id="analista_apple")
#agent.print_response("Olá, prefiro respostas em formato de textos, gosto de bastante detalhes.", session_id="petrobras_session_1", user_id="analista_petrobras")


agent.print_response("Qual é a cotação atual da Apple?", session_id="apple_session", user_id="analista_apple")
agent.print_response("Qual é a cotação atual da Petrobras?", session_id="petrobras_session", user_id="analista_petrobras")
#agent.print_response("Quais empresas já consultamos a cotação?", session_id="petrobras_session", user_id="analista_petrobras")





