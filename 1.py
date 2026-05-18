import  asyncio


async def task():
    print("开始协程")
    await asyncio.sleep(3)
    print("结束协程")

async def main():
    t1=asyncio.create_task(task())
    t2 = asyncio.create_task(task())
    t3 = asyncio.create_task(task())

    await t1
    await t2
    await t3
asyncio.run(task())
asyncio.run(task())
asyncio.run(task())

asyncio.run(main())
