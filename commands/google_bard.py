from signalbot import Command, Context
from ai import ChatModel

class BardCommand(Command):
    def __init__(self):
        self.bard = ChatModel('bard').api

    def describe(self) -> str:
        return "Bard Command: Interact with the Bard model"

    async def handle(self, c: Context):
        command = c.message.text

        if command.startswith("!bard"):
            query = command[5:].strip()  # remove "!bard" from the command
            response = await self.bard.send(query)
            #print(response)
            response_text = response['content']
            await c.send(response_text)
            return

