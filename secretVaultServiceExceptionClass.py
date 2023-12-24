import asyncio

class SecretVaultServiceException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


_400 = SecretVaultServiceException(400, "Bad Request")
_401 = SecretVaultServiceException(401, "Unauthorized")
_403 = SecretVaultServiceException(403, "Forbidden")
_404 = SecretVaultServiceException(404, "Not Found")


svs_exceptions = ExceptionGroup("secret_vault_service_exceptions",[_400, _401, _403, _404])

async def func_a():
    raise _400

async def func_b():
    raise _401

async def func_c():
    raise _403

async def func_d():
    raise _404  

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(func_a())
            tg.create_task(func_b())
            tg.create_task(func_c())
            tg.create_task(func_d())
        result = [task.result() for task in tg]
        print(result)
    except* SecretVaultServiceException as e:
        print("Errors:", *[str(e) for e in e.exceptions])


asyncio.run(main())

        
