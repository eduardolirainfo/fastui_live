from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastui import FastUI, prebuilt_html, components as c
from fastui import AnyComponent
from fastui import events as e
from fastui.components.display import DisplayLookup
from pydantic import BaseModel

app = FastAPI()

form_string = Annotated[str, Form()]


class User(BaseModel):
    id: int
    nome: str
    telefone: str


database: list[User] = [
    User(id=1, nome="Alice", telefone="123456"),
    User(id=2, nome="Bob", telefone="789012")
]

navbar = c.Navbar(title="APP!!!", start_links=[
                    c.Link(
                        on_click=e.GoToEvent(url="/"),
                        components=[
                            c.Text(text="Home"),
                        ]),
                    c.Link(
                        on_click=e.GoToEvent(url="/about"),
                        components=[
                            c.Text(text="About"),
                        ]),
                    c.Link(
                        on_click=e.GoToEvent(url="/cadastro"),
                        components=[
                            c.Text(text="Cadastro"),
                        ]),
                    c.Link(
                        on_click=e.GoToEvent(url="/listagem"),
                        components=[
                            c.Text(text="Listagem")
                        ]),
                ])


@app.get(
    "/api/",
    response_model=FastUI,
    response_model_exclude_none=True
    )
def api() -> list[AnyComponent]:
    return [
        c.Page(components=[
                navbar
            ],
        )
    ]


@app.get(
    "/api/cadastro",
    response_model=FastUI,
    response_model_exclude_none=True
    )
def api_cadastro() -> list[AnyComponent]:
    return [
            
           c.Page(components=[
              navbar,
              c.Form(
                submit_url="/cadastro",
                form_fields=[
                     c.forms.FormFieldInput(
                         name="nome",
                         title="Nome :",
                         ),
                     c.forms.FormFieldInput(
                         name="telefone",
                         title="Telefone :",
                         ),
                ])
            ])
        ]


@app.get(
    "/api/listagem",
    response_model=FastUI,
    response_model_exclude_none=True
    )
def api_listagem() -> list[AnyComponent]:
    return [
          c.Page(components=[
              navbar,
              c.Heading(text="Listagem!"),
              c.Table(
                     data=database,
                     data_model=User,
                     columns=[
                        DisplayLookup(
                            field="id",
                            on_click=e.GoToEvent(url="/detalhes/{id}")
                            ),
                        DisplayLookup(field="nome"),
                        DisplayLookup(field="telefone")
                        ]
                ),
              c.Button(text='Criar', on_click=e.GoToEvent(url="/cadastro"))
            ])
        ]


@app.get(
    "/api/detalhes/{user_id}",
    response_model=FastUI,
    response_model_exclude_none=True
    )
def api_detalhes(user_id: int) -> list[AnyComponent]:
    user = database[user_id-1]
    return [
            c.Page(components=[
                navbar,
                c.Heading(text=f"Nome: {user.nome}", level=3),
                c.Details(data=user),
                c.Button(
                    text='Editar',
                    on_click=e.GoToEvent(url=f"/editar/{user.id}"),
                    named_style="primary"
                    ),
                c.Button(
                    text='Voltar',
                    on_click=e.GoToEvent(url="/listagem"),
                    named_style="secondary"
                ),
                c.Button(
                    text='Excluir',
                    on_click=e.GoToEvent(url=f"/excluir/{user.id}"),
                    named_style="warning"
                    )
            ])
        ]


@app.get(
    "/api/editar/{user_id}",
    response_model=FastUI,
    response_model_exclude_none=True
    )
def api_editar(user_id: int) -> list[AnyComponent]:
    user = database[user_id-1]
    return [
            c.Page(components=[
                navbar,
                c.Heading(text=f"Editar: {user.nome}", level=3),
                c.Form(
                    submit_url=f"/editar/{user.id}",
                    form_fields=[
                        c.FormFieldInput(
                            name="id",
                            title="ID :",
                            initial=user.id,
                            locked=True
                            ),
                        c.FormFieldInput(
                            name="nome",
                            title="Nome :",
                            initial=user.nome
                            ),
                        c.FormFieldInput(
                            name="telefone",
                            title="Telefone :",
                            initial=user.telefone
                            ),
                    ]),
                c.Button(
                    text='Voltar',
                    on_click=e.GoToEvent(url=f"/detalhes/{user.id}"),
                    named_style="secondary"
                ),
            ])
        ]


@app.post("/cadastro")
def cadastro(nome: form_string, telefone: form_string) -> list[AnyComponent]:
    database.append(
        User(
            id=len(database)+1,
            nome=nome,
            telefone=telefone
            )
        )
    return [
            c.FireEvent(event=e.GoToEvent(url="/listagem"))
        ]


@app.get(
    "/api/excluir/{user_id}",
    response_model=FastUI,
    response_model_exclude_none=True
    )
def api_excluir(user_id: int) -> list[AnyComponent]:
    del database[user_id-1]
    return [
            c.FireEvent(event=e.GoToEvent(url="/listagem"))
        ]


@app.post("/editar/{user_id}")
def editar(user_id: int, nome: form_string, telefone: form_string):
    database[user_id-1] = User(
        id=user_id,
        nome=nome,
        telefone=telefone
        )
    return [
            c.FireEvent(event=e.GoToEvent(url=f"/detalhes/{user_id}"))
        ]



@app.get('/{path:path}')
def root():
    return HTMLResponse(prebuilt_html(title="APP!!!", ))
