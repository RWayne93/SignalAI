#import os
from signalbot import SignalBot
from commands import PingCommand, FridayCommand, TypingCommand, TriggeredCommand, BardCommand, LlamaCommand, ClaudeCommand, BingCommand, WelcomeCommand
import logging
from utils import get_group_info, update_timestamp

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

config_path = r"C:\Users\ryant\signal-cli-config\data\901595"
update_timestamp(config_path)
print("Updated timestamp", )

#group_name = 'THE REAL NERD TALK'
group_name = 'test'
#group_name = 'IrregularChat: Data,Research,&ML'
def main():

    signal_service = '127.0.0.1:8080'
    phone_number = '+phone_number'
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
    #bot.register(ClaudeCommand())
    bot.register(BardCommand())
    bot.register(BingCommand())
    bot.register(WelcomeCommand())

    bot.start()


if __name__ == "__main__":
    main()
