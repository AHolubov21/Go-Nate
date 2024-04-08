from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.aiohttp import SocketModeHandler

slack_token = "xoxb-2130371976770-6066452493427-fMtngLOwJZ4OFvz82jQ3vx2e"
client = SocketModeClient(
    app_token=slack_token,
    logger=logger,
)

# Функция для обработки событий
async def process_events(event):
    # Обработка событий здесь
    pass

# Запуск клиента
handler = SocketModeHandler(client, process_events)
handler.start()
