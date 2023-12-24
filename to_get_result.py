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

async def func_e(anum: int):
    print(int(anum))
    return "func_e: I am func_e and I am okay"

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            taskA = tg.create_task(func_a())
            taskB = tg.create_task(func_b())
            taskC = tg.create_task(func_c())
            taskD = tg.create_task(func_d())
            taskE = tg.create_task(func_e(anum = "10 "))
    except* SecretVaultServiceException as e:
        print("Errors:", *[str(e) for e in e.exceptions])
    except* Exception as e:
        print("Errors:", *[(str(e),e) for e in e.exceptions])
    finally:
        success = []
        for task in [taskA, taskB, taskC, taskD, taskE]:
            if task.exception():
                print(f"Task {task.get_name()} raised an exception: {task.exception()}")
            else:
                success.append(task.result())
        return success




ans = asyncio.run(main())
print(ans)
        
