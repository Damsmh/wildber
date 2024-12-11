from aiogram import Router, F, Bot
import uuid
from middlware.middlware import BanCheckMiddleware
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from keyboards.keyboard import keyboard_logged

from states.states import Registration, BuyPrime
from db.functions import addPrime
from config_data.config import load_config

router = Router()
router.message.middleware(BanCheckMiddleware())
bot = Bot(token=load_config().tg_bot.token)


@router.message(StateFilter(Registration.logged), Command(commands='prime'))
async def process_buy_command(message: Message, state: FSMContext):
    await state.set_state(BuyPrime.buy)
    payment_id = str(uuid.uuid4())
    config = load_config()
    ptoken = config.tg_bot.provider_token
    print(ptoken)
    await message.answer_invoice(
        title='Подписка Prime',
        description='Срок действия: бесконечная',
        payload=payment_id,
        provider_token=ptoken,
        currency='RUB',
        prices=[
            LabeledPrice(label='Оплатить', amount=2999),
        ]
    )

@router.pre_checkout_query()
async def process_pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(ok=True)

@router.message(F.ContentType == ContentType.SUCCESSFUL_PAYMENT)
async def success_payment_handler(message: Message, state: FSMContext):
    await message.answer(text="Спасибо за покупку prime подписки!\nТеперь вы можете добавлять в корзину больше 5 товаров.",
                         reply_markup=keyboard_logged)
    await addPrime(username=message.from_user.username)
    await state.set_state(Registration.logged)
    

