import asyncio
#this is how we have been practicing python concurrency so far with python version 3.10.0 
async def primary_wheel():
    print( "Primary: I am the primary")

async def secondary_wheel():
    raise TypeError("Secondary: I am the secondary wheel and I am broken")

async def third_wheel():
    raise ValueError("Third: I am the third wheel and I am broken")

#case for cancellation:
async def longer_wheel():
    try:
        await asyncio.sleep(5)
        return "Longer:I am the longer wheel and am still running"
    except asyncio.CancelledError:
        print("Longer: I was cancelled")
        raise asyncio.CancelledError

async def pre_main():
    try:
        result = await asyncio.gather(primary_wheel(), secondary_wheel(), third_wheel())
        return result
    except TypeError as e:
        print("TypeError")
    except ValueError as e:
        print("ValueError")
    except Exception as e:
        print("Exception")


async def pre_pre_main():
    result = await asyncio.gather(primary_wheel(), secondary_wheel(), third_wheel(), return_exceptions=True)
    for exception in result:
        match exception:
            case TypeError():
                print("TypeError")
            case ValueError():
                print("ValueError")
            case Exception():
                print("Exception")
            case _:
                print("Unknown")
    return result


async def main():
    try:
        task1 = asyncio.create_task(primary_wheel())
        task2 = asyncio.create_task(secondary_wheel())
        task3 = asyncio.create_task(third_wheel())
        task4 = asyncio.create_task(longer_wheel())
        result = await asyncio.gather(*[task1, task2, task3, task4])
        print(f"result={result}")
    except TypeError as e:
        print("TypeError")
    except ValueError as e:
        print("ValueError")
    for task in [task1, task2, task3, task4]:
        if task.done() is False:
            task.cancel()
    print("DONE")


asyncio.run(main())

