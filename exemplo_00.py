from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import FastUI, prebuilt_html, components as c

app = FastAPI()


@app.get(
    "/api/",
    response_model=FastUI,
    response_model_exclude_none=True
    )
def api():
    return [
        c.Page(components=[
                c.Navbar(title="FastUI"),
                c.Heading(text="Olá Mundo", level=1),
                c.Paragraph(text="Este é um exemplo de uso do FastUI."),
                c.Button(text="Clique aqui"),
            ],
        )
    ]


@app.get('/{path:path}')
def root():
    return HTMLResponse(prebuilt_html())
