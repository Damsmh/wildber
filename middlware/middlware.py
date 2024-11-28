from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import *

class ButtonMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        return await handler(event, data)