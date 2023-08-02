# Signalbot Example

An example bot for Signal that uses the [signalbot](https://github.com/filipre/signalbot) Python package. With LLM integration insprired by https://github.com/cycneuramus/signal-aichat 

Big thanks to the following reversed engineered API libraries for hugchat, bard, bing, and claude. 
https://github.com/Soulter/hugging-chat-api
https://github.com/acheong08/Bard
https://github.com/AshwinPathi/claude-api-py
https://github.com/acheong08/EdgeGPT

## Getting Started

Please check out the example code to get an idea on how to develop your own bot or commands. Also see https://github.com/bbernhard/signal-cli-rest-api#getting-started to learn more about [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) and [signal-cli](https://github.com/AsamK/signal-cli). A good first step is to make the example bot work:

1. Run signal-cli-rest-api in `normal` mode first.
```bash
docker run -p 8080:8080 \
    -v $(PWD)/signal-cli-config:/home/.local/share/signal-cli \
    -e 'MODE=normal' bbernhard/signal-cli-rest-api:0.57
```

2. Open http://127.0.0.1:8080/v1/qrcodelink?device_name=local to link your account with the signal-cli-rest-api server

3. In your Signal app, open settings and scan the QR code. The server can now receive and send messages. The access key will be stored in `$(PWD)/signal-cli-config`.

4. Restart the server in `json-rpc` mode.
```bash
docker run -p 8080:8080 \
    -v $(PWD)/signal-cli-config:/home/.local/share/signal-cli \
    -e 'MODE=json-rpc' bbernhard/signal-cli-rest-api:0.57
```

5. The logs should show something like this. You can also confirm that the server is running in the correct mode by visiting http://127.0.0.1:8080/v1/about.
```
...
time="2022-03-07T13:02:22Z" level=info msg="Found number +491234567890 and added it to jsonrpc2.yml"
...
time="2022-03-07T13:02:24Z" level=info msg="Started Signal Messenger REST API"
```

6. The bot needs to listen to a group. Use the following snippet to get a group's `id` and `internal_id` the output of the below command needs to go in groups.json:
```bash
curl -X GET 'http://127.0.0.1:8080/v1/groups/+49123456789' | python -m json.tool
```

7. Install `signalbot` and start `bot.py`. You need to pass following environment variables to make the example run:
- `SIGNAL_SERVICE`: Address of the signal service without protocol, e.g. `127.0.0.1:8080`
- `PHONE_NUMBER`: Phone number of the bot, e.g. `+49123456789`
- `GROUP_ID`: Group that the bot should listen to. Prefixed with `group.`
- `GROUP_INTERNAL_ID`: Group's `internal_id`

```bash
export SIGNAL_SERVICE="127.0.0.1"
export PHONE_NUMBER="+49123456789"
export GROUP_ID="group.qwerqwerqwerqwerqwerqwerqweqwer=="
export GROUP_INTERNAL_ID="asdfasdfasdfasdf="

# If you use pip
pip install signalbot
python bot.py

# If you use poetry
poetry install
poetry run python bot.py
```

8. The logs should indicate that one "producer" and three "consumers" have started. The producer checks for new messages sent to the linked account using a web socket connection. It creates a task for every registered command and the consumers work off the tasks. In case you are working with many blocking function calls, you may need to adjust the number of consumers such that the bot stays reactive.
```
INFO:root:[Bot] Producer #1 started
INFO:root:[Bot] Consumer #1 started
INFO:root:[Bot] Consumer #2 started
INFO:root:[Bot] Consumer #3 started
```

9. Send the message `ping` (case sensitive) to the group that the bot is listening to. The bot (i.e. the linked account) should respond with a `pong`. Confirm that the bot received a raw message, that the consumer worked on the message and that a new message has been sent.
```
INFO:root:[Raw Message] {"envelope":{"source":"+49123456789","sourceNumber":"+49123456789","sourceUuid":"fghjkl-asdf-asdf-asdf-dfghjkl","sourceName":"René","sourceDevice":3,"timestamp":1646000000000,"syncMessage":{"sentMessage":{"destination":null,"destinationNumber":null,"destinationUuid":null,"timestamp":1646000000000,"message":"pong","expiresInSeconds":0,"viewOnce":false,"groupInfo":{"groupId":"asdasdfweasdfsdfcvbnmfghjkl=","type":"DELIVER"}}}},"account":"+49123456789","subscription":0}
INFO:root:[Bot] Consumer #2 got new job in 0.00046 seconds
INFO:root:[Bot] Consumer #2 got new job in 0.00079 seconds
INFO:root:[Bot] Consumer #2 got new job in 0.00093 seconds
INFO:root:[Bot] Consumer #2 got new job in 0.00106 seconds
INFO:root:[Bot] New message 1646000000000 sent:
pong
```

10. if you don't want to see all the logs across all chat rooms your signal account is tied to you can modify the produce function inside the signal bot library. This modification will only show you logs for signal rooms your bot is listening in. 

```
    async def _produce(self, name: int) -> None:
        logging.info(f"[Bot] Producer #{name} started")
        try:
            async for raw_message in self._signal.receive():
                # Parse the raw_message into a dictionary
                message_dict = json.loads(raw_message)

                # Skip processing of receipt messages
                if 'receiptMessage' in message_dict.get('envelope', {}):
                    continue

                try:
                    message = Message.parse(raw_message)
                except UnknownMessageFormatError:
                    continue

                # Check if the message is from the group chat you're interested in
                if self._is_group_id(message.group) and self._is_internal_id(message.group):
                    logging.info(f"[Raw Message] {raw_message}")

                if not self._should_react(message):
                    continue

                await self._ask_commands_to_handle(message)
```

## Example Commands

!hugchat (requires cookies file in a json format see config folder.)
!bard we (are using browser_cookie3 here https://github.com/borisbabic/browser_cookie3)
!claude (we are using browser_cookie3 here https://github.com/borisbabic/browser_cookie3)
!bingchat (requires cookies file in a json format see config folder.)

11. Shoutout to @cycneuramus for ai.py https://github.com/cycneuramus/signal-aichat had to make some slight modifications to the bard class to keep it from crashing some weird async stuff was happening... below 

```
loop = asyncio.get_event_loop()
class BardAPI:
    def __init__(self, token, secure_1psidts):
        #self.chat = Bard(token, secure_1psidts)
        
        self.chat = loop.run_until_complete(AsyncChatbot.create(token, secure_1psidts))
        #self.chat = asyncio.run(AsyncChatbot.create(token, secure_1psidts))
```
TODO move everything back to env variables and use either os or python-dotenv module