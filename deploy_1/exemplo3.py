#IMPORTS ======================
import requests
import json
from pprint import pprint

AGENT_ID = "agente_pdf"
ENDPOINT = f"http://localhost:7777/agents/{AGENT_ID}/runs"

#CONEXÃO COM O AGNO (SERVER)
def get_response_stream(message: str):
    response = requests.post(
        url=ENDPOINT,
        data={
            "message": message,
            "stream": "true"
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            #Parse Server-Sent Events
            if line.startswith(b'data: '):
                data = line[6:] #Remove 'data: ' prefix
                try:
                    event = json.loads(data)
                    yield event
                except json.JSONDecodeError:
                    continue


#PRINTA A RESPOSTA =============

"""
RunStarted
ModelRequestStarted
RunContent
ModelRequestCompleted
ToolCallStarted
ToolCallCompleted
RunContentCompleted
RunCompleted
"""




def print_streaming_response(message: str):
    for event in get_response_stream(message):
        event_type = event.get("event", "")
        
        #INÍCIO DA EXECUÇÃO
        if event_type == "RunStarted":
            print('Execução iniciada...')
            print("="*50)
        
        #CONTEÚDO DA RESPOSTA
        elif event_type == "RunContent":
            content = event.get("content", "")
            if content:
                print(content, end="", flush=True)
        
        #TOOL CALL INICIADO
        elif event_type == "ToolCallStarted":
            tool = event.get("tool", {})
            tool_name = tool.get("tool_name", "Unknown")
            tool_args = tool.get("tool_args", {})
            print(f"TOOL INICIADA: {tool_name}")
            print(f"ARGUMENTOS: {json.dumps(tool_args, indent=2)}")
        

        elif event_type == "ToolCallCompleted":
            tool_name = event.get("tool", {}).get("tool_name")
            print(f"TOOL CONCLUÍDA: {tool_name}")
            print("="*50)
        
        elif event_type == "RunCompleted":
            print(f"Execução concluída!")
            metrics = event.get("metrics", {})
            if metrics:
                print(f"MÉTRICAS: {json.dumps(metrics, indent=2)}")
            print("="*50)






#RUN ================
if __name__ == "__main__":
    message = input("Digite uma mensagem: ")
    print_streaming_response(message)
    
    while True:
        message = input("Digite uma mensagem: ")
        print_streaming_response(message)
        

