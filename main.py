import json

from typing import Optional

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel


class Nota(BaseModel):
    conteudo: str
    nome: str
    projeto: str


class QueryNota(BaseModel):
    projeto: str
    nome: str


app = FastAPI()

# Listas para teste até a conecçao com DB
notas = [
    {"projeto": "Projeto 01", "nome": "Nota 01", "conteudo": "lorem ipsum dolum amet"},
    {"projeto": "Projeto 01", "nome": "Nota 02", "conteudo": "lorem ipsum dolum amet"},
    {"projeto": "Projeto 02", "nome": "Nota 01", "conteudo": "lorem ipsum dolum amet"},
    {"projeto": "Projeto 02", "nome": "Nota 02", "conteudo": "lorem ipsum dolum amet"},
    {"projeto": "Projeto 03", "nome": "Nota 01", "conteudo": "lorem ipsum dolum amet"},
    {"projeto": "Projeto 03", "nome": "Nota 02", "conteudo": "lorem ipsum dolum amet"},
    {"projeto": "Projeto 04", "nome": "Nota 01", "conteudo": "lorem ipsum dolum amet"},
    {"projeto": "Projeto 04", "nome": "Nota 02", "conteudo": "lorem ipsum dolum amet"},
    {"projeto": "Projeto 05", "nome": "Nota 01", "conteudo": "lorem ipsum dolum amet"},
    {"projeto": "Projeto 05", "nome": "Nota 02", "conteudo": "lorem ipsum dolum amet"},
]
checks = []
projetos = [
    {"nome": "Projeto 01"},
    {"nome": "Projeto 02"},
    {"nome": "Projeto 03"},
    {"nome": "Projeto 04"},
    {"nome": "Projeto 05"},
]


def projeto_existe(projeto: str):
    for item in projetos:
        if item["nome"] == projeto:
            return True
    return False


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/projetos")
async def read_projetos():
    return projetos


@app.post("/notas/")
async def create_nota(item: Nota):
    # Connectar com banco e salvar a nota
    if projeto_existe(item.projeto):
        notas.append(
            {"projeto": item.projeto, "nome": item.nome, "conteudo": item.conteudo}
        )
        return 201

    raise HTTPException(status_code=400, detail="Project not found")


@app.get("/notas/")
async def read_nota(query: QueryNota):
    # Conectar no banco e recuperar a nota
    for item in notas:
        if query.nome == item["nome"] and query.projeto == item["projeto"]:
            return item

    raise HTTPException(status_code=404, detail="Note not found")


@app.get("/notas/{projeto}")
async def search_by_project(projeto: str):
    retorno = []
    for item in notas:
        if projeto == item["projeto"]:
            retorno.append(item)

    if len(retorno) != 0:
        return retorno
    raise HTTPException(status_code=404, detail="Note not found")


@app.post("/checklists")
async def create_checklist(lista: str):
    lista_json = json.loads(lista)
    checks.append(lista_json["itens"])
    return 201


@app.get("/checklists/{check_id}")
async def read_checklist(check_id: int):
    if check_id < len(checks):
        return {"check_id": check_id, "lista": checks[check_id]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
