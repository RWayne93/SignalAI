from signalbot import Command, Context
from ai import ChatModel

class LlamaCommand(Command):
    def __init__(self):
        self.hugchat = ChatModel('hugchat').api
        # Check if a conversation already exists, if not create a new one
        if not self.hugchat.chat.conversation_id_list:
            self.conversation_id = self.hugchat.chat.new_conversation()
        else:
            self.conversation_id = self.hugchat.chat.conversation_id_list[0]
        self.hugchat.chat.change_conversation(self.conversation_id)

    def describe(self) -> str:
        return "hugchat Command: Interact with the huggingface model LLama 2"
    
    async def handle(self, c: Context):
        command = c.message.text

        if command.startswith("!hugchat"):
            query = command[7:].strip()
            response = await self.hugchat.send(query)
            print(response)
            await c.send(response)
            return
