import json

from typing import Optional

from fastapi import FastAPI, HTTPException

app = FastAPI()

# Listas para teste até a conecçao com DB
notas = []
checks = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/nota")
def create_nota(text: str):
    # Connectar com banco e salvar a nota
    notas.append(text)
    return 201

@app.get("/nota/{nota_id}")
def read_nota(nota_id: int):
    # Conectar no banco e recuperar a nota
    if nota_id < len(notas):
        return {"nota_id": nota_id, "text": notas[nota_id]} 

    else:
        raise HTTPException(status_code=404, detail="Item not found")
    

@app.post("/checklist")
def create_checklist(lista: str):
    print(lista)
    return 200

@app.get("/checklist/{check_id}")
def read_checklist(check_id: int):
    if check_id < len(checks):
        return {"check_id": check_id, "lista": checks[check_id]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
