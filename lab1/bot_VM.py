import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from tracker import Tracker
from TOKEN import API_TOKEN

logging.basicConfig(level=logging.INFO)

tr = Tracker(['ethereum', 'bitcoin'])

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class StatesSet(StatesGroup):
	price = State()
	volume = State()

@dp.message_handler(state=None,commands=['btc', 'eth'])
async def cmd_not_mode(message: types.Message):
	await message.reply("no operating mode selected, please select a mode (/price or /volume):")

@dp.message_handler(state='*',commands='price')
async def cmd_price(message: types.Message):
	await StatesSet.price.set()
	await message.reply("choose crypto currency name (/eth or /btc):")

@dp.message_handler(state='*',commands='volume')
async def cmd_volume(message: types.Message):
	await StatesSet.volume.set()
	await message.reply("choose crypto currency name (/eth or /btc):")

@dp.message_handler(state=StatesSet.price,commands='btc')
async def cmd_btcprice(message: types.Message):
	await message.reply(f"Price of btc: {tr.get_data()['btc'][0]} $")

@dp.message_handler(state=StatesSet.price,commands='eth')
async def cmd_ethprice(message: types.Message):
	await message.reply(f"Price of eth: {tr.get_data()['eth'][0]} $")

@dp.message_handler(state=StatesSet.volume,commands='btc')
async def cmd_btcvolume(message: types.Message):
	await message.reply(f"Volume of btc: {tr.get_data()['btc'][1]} $")

@dp.message_handler(state=StatesSet.volume,commands='eth')
async def cmd_ethvolume(message: types.Message):
	await message.reply(f"Volume of eth: {tr.get_data()['eth'][1]} $")

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
