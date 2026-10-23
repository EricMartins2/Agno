#Conta Corrente Bancária - FastAPI
#Gerenciar saques e depósitos de clientes

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field




#Instanciar o fastAPI
app = FastAPI(title="Conta Bancária - Conta Corrente")



#Adicionar clientes
db_clientes = {
    "Joao": 0,
    "Maria": 0,
    "Pedro": 0
}


#Criar uma classe para movimentações (saques e depósitos). OBS: Usar o pydantic (para não haver erros)
class Movimentacao(BaseModel):
    cliente: str = Field(..., description="Nome do cliente")
    valor: float = Field(..., gt=0, description="Valor da movimentação")





#Criar um endpoint HOME (raiz)
@app.get("/")
def read_root():
    return{"message": "Conta Bancária - Conta corrente"}




#Adicionar endpoints para consultar saldo
@app.post("/saldo")
def saldo(cliente: str):
    return {"message": f"Saldo do cliente {cliente} é {db_clientes[cliente]}"}




#Adicionar endpoints para realizar saques
@app.post("/saque")
def saque(movimentacao: Movimentacao):
    db_clientes[movimentacao.cliente] -= movimentacao.valor
    return {"message": {'cliente': movimentacao.cliente, "valor_movimentacao": -movimentacao.valor, "saldo": db_clientes[movimentacao.cliente]}}



#Adicionar endpoints para realizar depósitos
@app.post("/deposito")
def deposito(movimentacao: Movimentacao):
    db_clientes[movimentacao.cliente] += movimentacao.valor
    return {"message": {'cliente': movimentacao.cliente, "valor_movimentacao": movimentacao.valor, "saldo": db_clientes[movimentacao.cliente]}}




#RUN
if __name__ == "__main__":
    uvicorn.run("exemplo2:app", host="0.0.0.0", port=8000, reload=True)


