from dataclasses import dataclass
from environs import Env




@dataclass
class TgBot:
    token: str

@dataclass
class Database:
    url: str

@dataclass
class Config:
    tg_bot: TgBot
    db_engine: Database




def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    db_url = f"{env('DATABASE')}+{env('DB_DRIVER')}://{env('DB_USER')}:{env('DB_PSWD')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                db_engine=Database(url=db_url))