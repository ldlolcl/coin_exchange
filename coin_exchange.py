import telebot
bot = telebot.TeleBot('TOKEN')

def okonch_rub(n):
	if n > 10: return okonch_rub(n % 10)
	elif 1 <= n <= 10 or n == 0: 
		if int(n) in (0,5,6,7,8,9,10): return 'рублей'
		elif int(n) == 1: return 'рубль'
		elif int(n) in (2,3,4): return 'рубля'
	elif n < 1: return okonch_rub(n * 10)

def okonch_coin(n):
	if n > 10: return okonch_coin(n % 10)
	elif 1 <= n <= 10 or n == 0: 
		if int(n) in (0,5,6,7,8,9,10): return 'монет'
		elif int(n) == 1: return 'монета'
		elif int(n) in (2,3,4): return 'монеты'
	elif n < 1: return okonch_coin(n * 10)

def check(message):
	id = message.from_user.id
	with open('bd_coin_exchange.txt', 'r') as BD:
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
			print(print_bot)
			bot.send_message(message.chat.id, print_bot)
			return False
		count = sum([v for k,v in wallet.items()])
		total = sum([k*v for k,v in wallet.items()])
		return (id, wallet, count, total)

@bot.message_handler(commands=['start'])
def start(message):
	print_bot = '👋 Добро пожаловать в бот, который поможет избавиться от мелочи в карманах'
	print(print_bot)
	bot.send_message(message.chat.id, print_bot)
	user_name = message.from_user.first_name
	id = message.from_user.id
	user_status = False
	with open('bd_coin_exchange.txt', 'r') as BD:
		for line in BD:
			if str(id) in line:
				user_status = True
				id = int(line.split('\t')[0])
				check_info = check(message)
				print_bot = '👤 Пользователь '+user_name+' уже зарегистрирован в боте'
				print(print_bot)
				bot.send_message(message.chat.id, print_bot)	
				print_bot = '🪙 Внесено '+str(check_info[2])+' '+okonch_coin(check_info[2])+' на общую сумму '+str(check_info[3])+' '+okonch_rub(check_info[3])
				print(print_bot)
				bot.send_message(message.chat.id, print_bot)	
	if user_status == False:
		with open('bd_coin_exchange.txt', 'a') as BD:
			BD.write(str(id)+'\t'+str({0.01:0, 0.05:0, 0.1:0, 0.5:0, 1:0, 2:0, 5:0, 10:0})+'\n')
			print_bot = '👤 Пользователь ' + user_name + ' был успешно зарегистрирован в боте'
			print(print_bot)
			bot.send_message(message.chat.id, print_bot)

@bot.message_handler(commands=['wallet'])
def wallet(message):
	id = message.from_user.id
	check_info = check(message)
	if check_info == False:
		return
	print_bot = str('🪙 Внесено '+str(check_info[2])+' '+okonch_coin(check_info[2])+' на общую сумму '+str(check_info[3])+' '+okonch_rub(check_info[3]))
	print(print_bot)
	bot.send_message(message.chat.id, print_bot)
	for k,v in check_info[1].items():
		print_bot = str(k)+' '+okonch_rub(k)+': '+str(v)+' '+okonch_coin(v)
		bot.send_message(message.chat.id, print_bot)

@bot.message_handler(commands=['edit'])
def edit(message):
	id = message.from_user.id
	check_info = check(message)
	if check_info == False:
		return
	nominal = list(map(str, check_info[1].keys()))
	print_bot = f'💰 Пожалуйста подсчитайте всю свою мелочь и введите количество монет всех номиналов через пробел в следующем порядке:  \n{'\t\t\t'.join(nominal)}\n \nБыло внесено:'
	print(print_bot)
	bot.send_message(message.chat.id, print_bot)
	print_bot = ' '.join(list(map(str, check_info[1].values())))
	print(print_bot)
	bot.send_message(message.chat.id, print_bot)
	bot.register_next_step_handler(message, vvod)
def vvod(message):
	n = message.text
	try:
		n = list(map(int, n.split(' ')))
		if len(n) == 8:
			id = message.from_user.id
			check_info = check(message)
			if check_info == False:
				return
			nominal = list(check_info[1].keys())
			wallet = dict()
			for i in range(8):
				wallet[nominal[i]] = n[i]
			with open('bd_coin_exchange.txt', 'r') as BD:
				file = BD.readlines()
			with open('bd_coin_exchange.txt', 'w') as BD:
				for line in file:
					if str(id) in line:
						line = str(id)+'\t'+str(wallet)+'\n'
					BD.write(line)
			print_bot = '👌 Данные обнолены'
			print(print_bot)
			bot.send_message(message.chat.id, print_bot)
			id = message.from_user.id
			check_info = check(message)
			print_bot = str('🪙 Внесено '+str(check_info[2])+' '+okonch_coin(check_info[2])+' на общую сумму '+str(check_info[3])+' '+okonch_rub(check_info[3]))
			print(print_bot)
			bot.send_message(message.chat.id, print_bot)
		else:
			print_bot = '❌ Введено неверное количество номиналов'
			print(print_bot)
			bot.send_message(message.chat.id, print_bot)
	except:
		print_bot = '❌ Введены некорректные данные'
		print(print_bot)
		bot.send_message(message.chat.id, print_bot)

@bot.message_handler(content_types=['text'])
def fun_exchange(message):
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
			print(print_bot)
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
					print(print_bot)
					bot.send_message(message.chat.id, print_bot)
					print_bot = '❕ Получилось собрать только '+str(total_a)+' '+okonch_rub(total_a)+': '
					print(print_bot)
					bot.send_message(message.chat.id, print_bot)
					break	
			for i in answer:
				if answer[i] > 0:
					print_bot = str(i)+' '+okonch_rub(i)+' x '+str(answer[i])
					print(print_bot)
					bot.send_message(message.chat.id, print_bot)
	except ValueError:
		print_bot = '❌ Введено некорректное число для обмена/оплаты'
		print(print_bot)
		bot.send_message(message.chat.id, print_bot)

#RUN
bot.polling(none_stop=True)