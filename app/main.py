import asyncio
from fastapi import FastAPI
from setup.payload_categorization import RequestBodySchema, TaskGroup
from setup.to_get_result import SecretVaultServiceException
from internal.namespace import create_vault_namespace

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
    try:
        
        async with asyncio.TaskGroup() as primary:
            taskNamespace = primary.create_task(create_vault_namespace())

        async with asyncio.TaskGroup() as add_on_services:
            for key, value in TaskGroup.add_on_services_task_list.items():
                for a_task in value:
                    add_on_services.create_task(a_task())
    
        print("All the tasks were done")

    except* SecretVaultServiceException as e:
        print("Errors:", *[str(e) for e in e.exceptions])

    except* Exception as e:
        print("Errors:", *[(str(e),e) for e in e.exceptions])

    finally:
        return "We have successfully created namespaces"


