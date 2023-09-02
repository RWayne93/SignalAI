from signalbot import Command, Context
import re

class WelcomeCommand(Command):
    def __init__(self):
        pass 

    def describe(self) -> str:
        return "Welcome Command: Generates a welcome message for a given username"

    async def handle(self, c: Context):
        command = c.message.text

       
        if command.startswith("!welcome"):
            welcome_message, mentions = self.get_welcome_message_from_command(command)

            if welcome_message:  # ensure welcome_message is not None
                # Check if the content is a phone number format
                content_after_command = command[len('!welcome'):].lstrip()
                phone_number_pattern = re.compile(r'^\+?[0-9]+$')  # basic check for a phone number
                
                # Check if the provided input isn't a phone number, then clear mentions
                if content_after_command.endswith('.') and not phone_number_pattern.match(content_after_command[:-1]):  # check without the period
                    mentions = []

                await c.send(welcome_message, mentions=mentions)
            else:
                await c.send("Error: Please end the username with a period.")
            return

    def get_welcome_message_from_command(self, command: str) -> (str, list):
        # Remove the command part and then strip extra spaces only at the beginning
        content_after_command = command[len('!welcome'):].lstrip()

        # Check if username ends with a period
        if content_after_command.endswith('.'):
            username = content_after_command[:-1]  # just remove the period, do not strip spaces now
            
            welcome_message = self.get_welcome_message(username)

            # Construct mentions for Signal API
            start_position = welcome_message.find(username)
            mentions = [{
                "author": username,
                "start": start_position,
                "length": len(username) # +1 for the "@" character
            }]
            print(mentions)
            
            return welcome_message, mentions
        return None, []  # returns None and empty list if there's an error

    def get_welcome_message(self, username: str) -> str:
        with open("welcome_template.txt", "r") as file:
            template = file.read()
            welcome_message = template.format(username=username)
        return welcome_message