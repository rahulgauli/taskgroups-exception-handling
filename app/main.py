from fastapi import FastAPI
from setup.payload_categorization import RequestBodySchema, TaskGroup

class ServerLoud:
    app = FastAPI(title="ServerLoud", version="0.1.0")

app = ServerLoud.app

@app.middleware("http")
async def clean_global_task_group(request, call_next):
    TaskGroup.clean_task_group()
    response = await call_next(request)
    return response

@app.middleware("http")
async def add_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.get("/")
async def hello():
    print("hello")
    return {"message": "Hello World"}

@app.post("/namespaces")
async def create_hashicorp_vault_namespace(request_body: RequestBodySchema):
    print(request_body)
    print(TaskGroup.add_on_services_task_list)
    return {"message": "We have successfully created taskgroups"}

