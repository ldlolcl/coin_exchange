import telebot
bot = telebot.TeleBot('TOKEN')

G, answer = None, None
D = {0.01: '1 копейка',
	0.05: '5 копеек',
	0.1: '10 копеек',
	0.5: '50 копеек',
	1: '1 рубль',
	2: '2 рубля',
	5: '5 рублей',
	10: '10 рублей'}

def okonch_rub(n):
	n = int(n)
	if n > 10: return okonch_rub(n % 10)
	elif 1 <= n <= 10 or n == 0: 
		if int(n) in (0,5,6,7,8,9,10): return 'рублей'
		elif int(n) == 1: return 'рубль'
		elif int(n) in (2,3,4): return 'рубля'
	elif n < 1: return okonch_rub(n * 10)

def okonch_coin(n):
	if n > 14: return okonch_coin(n % 10)
	elif 1 <= n <= 14 or n == 0: 
		if int(n) in (0,5,6,7,8,9,10,11,12,13,14): return 'монет'
		elif int(n) == 1: return 'монета'
		elif int(n) in (2,3,4): return 'монеты'
	elif n < 1: return okonch_coin(n * 10)

def check(message):
	id = message.from_user.id
	with open('/Volumes/HDD/Python/coin_exchange/bd_coin_exchange.txt', 'r') as BD:
		wallet = dict()
		user_starus = False
		for line in BD:
			if str(id) in line:
				user_starus = True
				line = line.split('\t')[1][1:-2]
				for i in line.split(', '):
					if '.' in i.split(': ')[0]: k = float(i.split(': ')[0])
					else: k = int(i.split(': ')[0])
					v = int(i.split(': ')[1])
					wallet[k] = v
		if user_starus == False:
			print_bot = '‼️ Возникла ошибка. Начните заново с команды /start'
			bot.send_message(message.chat.id, print_bot)
			return False
		count = sum([v for k,v in wallet.items()])
		total = round(sum([k*v for k,v in wallet.items()]), 2)
		return (id, wallet, count, total)

@bot.message_handler(commands=['start'])
def Start(message):
	print_bot = '👋 Добро пожаловать в бот, который поможет избавиться от мелочи в карманах'
	bot.send_message(message.chat.id, print_bot)
	user_name = message.from_user.first_name
	id = message.from_user.id
	user_status = False
	markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	#item1 = telebot.types.KeyboardButton('🟢 Старт')
	item2 = telebot.types.KeyboardButton('💰 Кошелек')
	markup.add(item2)
	with open('/Volumes/HDD/Python/coin_exchange/bd_coin_exchange.txt', 'r') as BD:
		for line in BD:
			if str(id) in line:
				user_status = True
				id = int(line.split('\t')[0])
				check_info = check(message)
				print_bot = '👤 Пользователь '+user_name+' уже зарегистрирован в боте'
				print(print_bot)
				bot.send_message(message.chat.id, print_bot, reply_markup=markup)	
				#print_bot = '🪙 Внесено '+str(check_info[2])+' '+okonch_coin(check_info[2])+' на общую сумму '+str(check_info[3])+' '+okonch_rub(check_info[3])
				#bot.send_message(message.chat.id, print_bot, reply_markup=markup)	
	if user_status == False:
		with open('/Volumes/HDD/Python/coin_exchange/bd_coin_exchange.txt', 'a') as BD:
			BD.write(str(id)+'\t'+str({0.01:0, 0.05:0, 0.1:0, 0.5:0, 1:0, 2:0, 5:0, 10:0})+'\n')
			print_bot = '👤 Пользователь ' + user_name + ' был успешно зарегистрирован в боте'
			print(print_bot)
			bot.send_message(message.chat.id, print_bot, reply_markup=markup)	

@bot.message_handler(commands=['wallet'])
def Wallet(message):
	id = message.from_user.id
	check_info = check(message)
	if check_info == False:
		return
	print_bot = list()
	print_bot.append(str('🪙 Внесено '+str(check_info[2])+' '+okonch_coin(check_info[2])+' на общую сумму '+str(check_info[3])+' '+okonch_rub(check_info[3])+':\n\n'))
	for k,v in check_info[1].items():
		print_bot.append(D[k]+': '+str(v)+' '+okonch_coin(v)+'\n')
	markup = telebot.types.InlineKeyboardMarkup()
	item1 = telebot.types.InlineKeyboardButton('1 копейка', callback_data='0.01')
	item2 = telebot.types.InlineKeyboardButton('5 копеек', callback_data='0.05')
	item3 = telebot.types.InlineKeyboardButton('10 копеек', callback_data='0.1')
	item4 = telebot.types.InlineKeyboardButton('50 копеек', callback_data='0.5')
	item5 = telebot.types.InlineKeyboardButton('1 рубль', callback_data='1')
	item6 = telebot.types.InlineKeyboardButton('2 рубля', callback_data='2')
	item7 = telebot.types.InlineKeyboardButton('5 рублей', callback_data='5')
	item8 = telebot.types.InlineKeyboardButton('10 рублей', callback_data='10')
	markup.add(item1, item2, item3, item4, item5, item6, item7, item8)
	global answer
	answer = ''.join(print_bot)
	bot.send_message(message.chat.id, answer, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def Edit(call):
	if call.message:
		global G
		G = call.data
		if call.data == '0.01':
			bot.send_message(call.message.chat.id, 'Введите количество монет номиналом   <b>'+ D[0.01] +'</b>', parse_mode='HTML')
		elif call.data == '0.05':
			bot.send_message(call.message.chat.id, 'Введите количество монет номиналом   <b>'+ D[0.05] +'</b>', parse_mode='HTML')
		elif call.data == '0.1':
			bot.send_message(call.message.chat.id, 'Введите количество монет номиналом   <b>'+ D[0.1] +'</b>', parse_mode='HTML')
		elif call.data == '0.5':
			bot.send_message(call.message.chat.id, 'Введите количество монет номиналом   <b>'+ D[0.5] +'</b>', parse_mode='HTML')
		elif call.data == '1':
			bot.send_message(call.message.chat.id, 'Введите количество монет номиналом   <b>'+ D[1] +'</b>', parse_mode='HTML')
		elif call.data == '2':
			bot.send_message(call.message.chat.id, 'Введите количество монет номиналом   <b>'+ D[2] +'</b>', parse_mode='HTML')
		elif call.data == '5':
			bot.send_message(call.message.chat.id, 'Введите количество монет номиналом   <b>'+ D[5] +'</b>', parse_mode='HTML')
		elif call.data == '10':
			bot.send_message(call.message.chat.id, 'Введите количество монет номиналом   <b>'+ D[10] +'</b>', parse_mode='HTML')
		message = call.message
		bot.register_next_step_handler(message, vvod)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=None)

def vvod(message):
	try:
		n = int(message.text)
		if type(n) == int:
			id = message.from_user.id
			w = check(message)[1].copy()
			global G
			if '.' not in G: 
				w[int(G)] = n
			elif '.' in G:  
				w[float(G)] = n
	except:
		print_bot = '❌ Введено некорректное число'
		bot.send_message(message.chat.id, print_bot)
	else:
		with open('/Volumes/HDD/Python/coin_exchange/bd_coin_exchange.txt', 'r') as BD:
			file = BD.readlines()
		with open('/Volumes/HDD/Python/coin_exchange/bd_coin_exchange.txt', 'w') as BD:
			for line in file:
				if str(id) in line:
					line = str(id)+'\t'+str(w)+'\n'
				BD.write(line)
			print_bot = '👌 Данные обнолены'
			bot.send_message(message.chat.id, print_bot)
		Wallet(message)

@bot.message_handler(content_types=['text'])
def fun_exchange(message):
	if message.text == '🟢 Старт':
		Start(message)
	elif message.text == '💰 Кошелек':
		Wallet(message)
	else:
		try:
			exchange = str(message.text).replace(',', '.')
			exchange = float(exchange)
			id = message.from_user.id
			check_info = check(message)
			if check_info == False:
				return
			total = check_info[3]
			wallet = check_info[1]
			if exchange > total:
				print_bot = '🚫 У Вас недостаточно монет для обмена/оплаты'
				bot.send_message(message.chat.id, print_bot)
			else:
				answer = {0.01:0, 0.05:0, 0.10:0, 0.50:0, 1:0, 2:0, 5:0, 10:0}
				w = 0
				while w<1000:
					total_a = sum([k*v for k,v in answer.items()])
					if total_a == exchange:
						break
					elif total_a < exchange:
						for k,v in wallet.items():
							if total_a >= exchange:
								continue
							while v > 0:
								wallet[k] -= 1
								answer[k] += 1
								v -= 1
								total_a = sum([k*v for k,v in answer.items()])
								if total_a >= exchange:
									break
					elif total_a > exchange:
						for k,v in answer.items():
							if total_a <= exchange:
								continue
							while v > 0:
								wallet[k] += 1
								answer[k] -= 1
								v -= 1
								total_a = sum([k*v for k,v in answer.items()])
								if total_a == exchange:
									break
					w += 1
					if w >= 999:
						print_bot = '❗️ У Вас недостаточно нужных номиналов монет чтобы собрать '+str(exchange)+' '+okonch_rub(exchange)
						bot.send_message(message.chat.id, print_bot)
						print_bot = '❕ Получилось собрать только '+str(total_a)+' '+okonch_rub(total_a)+': '
						bot.send_message(message.chat.id, print_bot)
						break	
				for i in answer:
					if answer[i] > 0:
						print_bot = str(i)+' '+okonch_rub(i)+' x '+str(answer[i])
						bot.send_message(message.chat.id, print_bot)
		except ValueError:
			print_bot = '❌ Введено некорректное число для обмена/оплаты'
			bot.send_message(message.chat.id, print_bot)

#RUN
bot.polling(none_stop=True)