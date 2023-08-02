#import os
from signalbot import SignalBot
from commands import PingCommand, FridayCommand, TypingCommand, TriggeredCommand, BardCommand, LlamaCommand, ClaudeCommand, BingCommand
import logging
from utils import get_group_info

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)


group_name = 'test'

def main():

    signal_service = '127.0.0.1:8080'
    phone_number = '+phonenumber'
    group_id, internal_id = get_group_info(group_name)

    config = {
        "signal_service": signal_service,
        "phone_number": phone_number,
        "storage": None,
    }
    bot = SignalBot(config)

    bot.listen(group_id, internal_id)

    bot.register(PingCommand())
    bot.register(FridayCommand())
    bot.register(TypingCommand())
    bot.register(TriggeredCommand())
    bot.register(LlamaCommand())
    bot.register(ClaudeCommand())
    bot.register(BardCommand())
    bot.register(BingCommand())

    bot.start()


if __name__ == "__main__":
    main()
