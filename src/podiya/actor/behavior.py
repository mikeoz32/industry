class Behavior:
    async def __call__(self, msgbox):
        async for message in msgbox:
            print(message)
