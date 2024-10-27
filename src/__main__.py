
from typing import Callable, Awaitable, Any

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, WebAppInfo, Update
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.web_app import safe_parse_webapp_init_data

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from tortoise import Tortoise
import uvicorn

from models import User
from config_reader import config


class UserMiddleware(BaseMiddleware):
    """
    Middleware для обработки пользовательских данных.
    """
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        """
        Обработчик middleware для добавления пользовательских
        данных в контекст события.

        :param handler: Обработчик события.
        :param event: Событие.
        :param data: Данные события.
        :return: Результат выполнения обработчика.
        """
        if not event.from_user.username:
            return await event.answer(
                "Нужно задать имя пользователя чтобы использовать бот."
                )

        user = await User.get_or_create(
            id=event.from_user.id, username=event.from_user.username
            )
        data["user"] = user[0]
        return await handler(event, data)


async def lifespan(app: FastAPI):
    """
    Функция для управления жизненным циклом FastAPI приложения.

    :param app: Экземпляр FastAPI приложения.
    """
    await bot.set_webhook(
        url=f"{config.WEBAPP_URL}/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )

    await Tortoise.init(
        db_url=config.DB_URL.get_secret_value(),
        modules={"models": ["models"]}
        )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
    await bot.session.close()

bot = Bot(
    token=config.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=config.TEMPLATES_PATH)

dp.message.middleware(UserMiddleware())
app.mount("/static", StaticFiles(directory=config.STATIC_PATH), name="static")


@dp.message(CommandStart())
async def start(message: Message, user: User):
    dict_markup = (
        InlineKeyboardBuilder()
        .button(
            text="🎮 Играть!",
            web_app=WebAppInfo(url=config.WEBAPP_URL))
    ).as_markup()

    await message.answer(
        "Привет, мы можем поиграть, если хочешь!",
        reply_markup=dict_markup
        )


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def main():
    """
    Основная функция для запуска бота и инициализации базы данных.
    """
    await bot.set_webhook(
        url=f"{config.WEBAPP_URL}/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )

    await Tortoise.init(
        db_url=config.DB_URL.get_secret_value(),
        modules={"models": ["models"]}
        )
    await Tortoise.generate_schemas()

    await bot.session.close()


@app.post("/webhook")
async def webhook(request: Request):
    """
    Обработчик вебхука для бота.

    :param request: Запрос.
    """
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
