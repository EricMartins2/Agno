from agno import vectordb
from agno.db.sqlite import SqliteDb
from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge.reader.pdf_reader import PDFReader
from dotenv import load_dotenv
from agno.os import AgentOS



from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb




load_dotenv()


vector_db = ChromaDb(collection="pdf_agent", path="tmp/chromadb", persistent_client=True)
knowledge = Knowledge(vector_db=vector_db)


db = SqliteDb(session_table='agent_session', db_file='tmp/agent.db')



agent = Agent(
    id="agente_pdf",
    name='Agente_de_PDF',
    model=Groq(id='openai/gpt-oss-120b'),
    db=db,
    description='',
    add_memories_to_context=True,
    instructions='Você sempre deve chamar o usuário de Senhor e busque informações no PDF',
    knowledge=knowledge,
    search_knowledge=True,
    num_history_runs=3,
    debug_mode=True

)

#AGENT OS
agent_os = AgentOS(
    name = "Agente de PDF",
    agents=[agent],
)


app = agent_os.get_app()


#RUN
if __name__ == "__main__":
    knowledge.insert(
        url="https://s3.sa-east-1.amazonaws.com/static.grendene.aatb.com.br/releases/2588_PR_2T26.pdf",
        metadata={"source": "Grandne", "type": "pdf", "description": "Relatório do 2T26"},
        skip_if_exists=True,
        reader=PDFReader()
    )
    agent_os.serve(app="exemplo10:app", host="0.0.0.0", port=10000, reload=True)



