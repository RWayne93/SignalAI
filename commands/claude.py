from signalbot import Command, Context
from ai import ChatModel

class ClaudeCommand(Command):
    def __init__(self):
        self.claude = ChatModel('claude').api

    def describe(self) -> str:
        return "Claude Command: Interact with the Claude model"

    async def handle(self, c: Context):
        command = c.message.text

        if command.startswith("!claude"):
            query = command[7:].strip()
            response = await self.claude.send(query)
            print(response)
            await c.send(response['completion'])
            return
