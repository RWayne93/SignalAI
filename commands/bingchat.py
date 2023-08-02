from signalbot import Command, Context
from ai import ChatModel

class BingCommand(Command):
    def __init__(self):
        self.bing = ChatModel('bing').api

    def describe(self) -> str:
        return "Bing Command: Interact with the Bing Chat model"
    
    async def handle(self, c: Context):
        command = c.message.text
    
        if command.startswith("!bingchat"):
            query = command[9:].strip()
            response = await self.bing.send(query)
            print(response)
            await c.send(response)
            return