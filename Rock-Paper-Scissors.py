"""
Изначальная формулировка:

    Создайте чат-бота для игры в "Камень-ножницы-бумага".
    Это должно быть консольное приложение, после запуска которого с ним можно общаться текстовыми командами.
    Например, начать или остановить игру, посмотреть текущий счет и пр.

    Предполагается, что Вы реализуете разные стратегии игры компьютера. Например, компьютер все время выдает
    один и тот же вариант, или каждый раз совершенно случайный. Но это не очень интересно. Хотелось бы, чтобы
    Вы придумали разные стратегии поведения компьютера, в зависимости от того, как были сделаны предыдущие ходы.

    Кроме того, правила самой игры также можно изменить: другой состав выбрасываемых фигур;
    ставки на каждый кон с подсчетом общего числа баллов и т.п.

Техническое задание:

    Консольное приложение/бот для игры в Камень-Ножницы-Бумага с классическими правилами.
    При запуске приложения пользователю выводится инструкция. После этого, пользователь может
    использовать команды, прописанные ниже, и играть в свое удовольствие.

    Все команды:
        /help - о программе и как ей пользоваться
        /game - начать партию
        /quit - закрыть программу
        /settings - настройки программы (можно установить кол-во ходов в одной партии)
        /stats - посмотреть всю статистику игры ( кол-во партий/побед/проигрышей/ничьих;процент побед;
                                                  наибольшее кол-во партий(побед) подряд; наигранное время )

    Сами игры проходят в виде партий, в каждой партии по три раунда, на вход принимается "камень", "ножницы", "бумагаr".
    Побеждает та сторона, которая выигрывает большее количество раундов в партии.

Пример:

 PRESS ENTER TO START

 Напишите /help, чтобы узнать о программе;
 если вы готовы начать, напишите нужную вам команду.

 .gdep

 Введите коректную команду
 /help

 Это программа/бот для игры в "Камень-Ножницы-Бумага с классическими правилами".
 Игры проходят партиями, в каждой партии три раунда. Побеждает та сторона, которая
 выигрывает большее количество раундов в партии.

 Доступные команды:
 /help - о программе и как ей пользоваться
 /game - начать партию
 /quit - закрыть программу
 /settings - настройки программы (можно установить кол-во ходов в одной партии)
 /stats - посмотреть всю статистику игры ( кол-во партий/побед/проигрышей/ничьих;процент побед;
                                           наибольшее кол-во партий(побед) подряд; наигранное время )

 /stats
 Сыграйте партию и тут появится больше статистики.
 Время проведенное в программе: 0.33мин

 /game

 ROUND 1 of 3
 Выберите фигуру: камень
 . . .
 КАМЕНЬ VS бумага
 бот победил

 ROUND 2 of 3
 Выберите фигуру: бумага
 . . .
 БУМАГА VS бумага
 ничья

 ROUND 3 of 3
 Выберите фигуру: rock
 Введите коректную фигуру: камень
 . . .
 КАМЕНЬ VS камень
 ничья

 ######### YOU LOST! #########

 *Партия закончилась. Напишите /game чтобы начать новый раунд или /stats; /settings; /quit...

 /stats
 Кол-во сыгранных партий: 1
 Кол-во выигранных партий: 0 (0.0%)
 Кол-во проигранных партий: 1 (100.0%)
 Кол-во ничьих: 0 (0.0%)
 Winstreak = 0
 Время проведенное в программе: 66.83890414237976

 /quit
"""

import time, sys, random #нужные для кода библиотеки
def slowprint(text, regulate):
    """ функция для печати с промежутком времени """
    for i in text:
        print(i, end='')
        sys.stdout.flush()  # очистка буфера, решает проблему вывода в консоли
        time.sleep(random.random()*regulate)  # время между выводом двух символов
        # 0.0 <= random,random < 1.0
def round_winner():
    global count_win #кол-во побед (счетчик)
    global count_lost #кол-во поражений (счетчик)
    global count_draw #кол-во ничьих (счетчик)
    global winstreak #кол-во побед подряд
    global last_winstreak
    if player_score_in_round>bot_score_in_round:
        count_win+=1
        winstreak+=1
        if winstreak>last_winstreak: #обновляем винстрик при условии если он больше чем предыдущий
            last_winstreak=winstreak #last_winstreak-винстрик который выводится в статистике
        slowprint(" ######### YOU WON! #########", 0.2)
    elif player_score_in_round<bot_score_in_round:
        count_lost+=1
        winstreak=0 #обнуляем винстрик тк пользователь не победил
        slowprint(" ######### YOU LOST! #########", 0.2)
    else:
        count_draw+=1
        winstreak=0 #обнуляем винстрик тк пользователь не победил
        slowprint(" ######### DRAW. #########", 0.2)
    print()
def bot_move():
    """ функция выбора лучшего хода,
         оченивается каждая фигура   """
    global bot_choice #фигура которую выбрала программа
    bot_choice="ага"
    if len(player_choices)>=15:
        rating_rock = 0
        rating_paper = 0
        rating_scissors = 0
        for i in range(0,len(player_choices)-2,3): #проходиться по всем закончиным раундам
            if len(player_choices)%3==1: #на данный момент прошел 1 раунд
                if player_choices[i]==player_choices[-1]:
                    if player_choices[i + 1] == "камень":
                        rating_rock += 1
                    elif player_choices[i + 1] == "ножницы":
                        rating_scissors += 1
                    elif player_choices[i + 1] == "бумага":
                        rating_paper += 1
            elif len(player_choices)%3==2: #на данный момент прошел 2 раунд
                if player_choices[-2]==player_choices[i] and player_choices[-1]==player_choices[i+1]:
                    if player_choices[i+2]=="камень":
                        rating_paper+=2
                    elif player_choices[i+2]=="ножницы":
                        rating_rock+=2
                    elif player_choices[i+2]=="бумага":
                        rating_scissors+=2
        #если кол-во фигуры меньше чем кол-во раундов - это значит что фигуру используют не в каждом раунде
        #остальные две или одна фигура поднимаются в рейтинге относильно нее
        #пример: игрок мало использует камень и у него низкий рейтинг, значит значит он выберет ножницы/бумагу;
        #бот выберает ножницы/бумагу, где шанс выиграть уже 50% вместо 33%
        if player_choices.count("камень")<len(player_choices)//3:
            rating_rock-=1
        if player_choices.count("ножницы")<len(player_choices)//3:
            rating_scissors-=1
        if player_choices.count("бумага")<len(player_choices)//3:
            rating_paper-=1
        #сравнение рейтинга и выбор хода:
        if rating_rock>(rating_paper or rating_scissors):
            bot_choice ="камень"
        if rating_paper>(rating_rock or rating_scissors):
            bot_choice = "бумага"
        if rating_scissors > (rating_paper or rating_rock):
            bot_choice = "ножницы"
        #print(rating_rock, rating_paper, rating_scissors)

        if rating_scissors == rating_paper == rating_rock:
            bot_choice = random.choice(["камень", "ножницы", "бумага"])
    else:
        bot_choice = random.choice(["камень", "ножницы", "бумага"])
def chose_winner_of_move(player_choice):
    global player_score_in_round #счет игрока в партии
    global bot_score_in_round #счет бота в партии
    global player_choices #фигура которую выбрал игрок
    global bot_choices #фигура которую выбрала программа
    bot_move()
    if player_choice == bot_choice:
        player_score_in_round+=1
        bot_score_in_round += 1
        print(f" {player_choice.upper()} VS {bot_choice}")
        player_choices.append(player_choice)
        bot_choices.append(bot_choice)
        print(" ничья")
        rating_choices.append(1)

    elif player_choice=="камень":
        if bot_choice=="ножницы":
            player_score_in_round+=1
            print(f" {player_choice.upper()} VS {bot_choice}")
            player_choices.append(player_choice)
            bot_choices.append(bot_choice)
            print(" вы победили")
            rating_choices.append(0)
        else:
            bot_score_in_round+=1
            print(f" {player_choice.upper()} VS {bot_choice}")
            player_choices.append(player_choice)
            bot_choices.append(bot_choice)
            print(" бот победил")
            rating_choices.append(2)

    elif player_choice=="ножницы":
        if bot_choice=="бумага":
            player_score_in_round += 1
            print(f" {player_choice.upper()} VS {bot_choice}")
            player_choices.append(player_choice)
            bot_choices.append(bot_choice)
            print(" вы победили")
            rating_choices.append(0)
        else:
            bot_score_in_round += 1
            print(f" {player_choice.upper()} VS {bot_choice}")
            player_choices.append(player_choice)
            bot_choices.append(bot_choice)
            print(" бот победил")
            rating_choices.append(2)

    elif player_choice=="бумага":
        if bot_choice=="камень":
            player_score_in_round += 1
            print(f" {player_choice.upper()} VS {bot_choice}")
            player_choices.append(player_choice)
            bot_choices.append(bot_choice)
            print(" вы победили")
            rating_choices.append(0)
        else:
            bot_score_in_round += 1
            print(f" {player_choice.upper()} VS {bot_choice}")
            player_choices.append(player_choice)
            bot_choices.append(bot_choice)
            print(" бот победил")
            rating_choices.append(2)

def game():
    global player_score_in_round #счет игрока в партии
    global bot_score_in_round #счет бота в партии
    bot_score_in_round=0
    player_score_in_round=0
    for i in range(moves_in_round):
        print()
        slowprint(" ROUND ", 0.25)
        print(i+1, end=" ")
        slowprint("of ", 0.25)
        print(moves_in_round)
        player_choice=input(" Выберите фигуру: ").lower()
        while player_choice not in ["камень", "ножницы", "бумага"]: #проверка на коректность ввода
            player_choice=input(" Введите коректную фигуру: ").lower()
        slowprint(" . . .", 0.5)
        print()
        chose_winner_of_move(player_choice)
    print()
    round_winner()
    print()
    print(" *Партия закончилась. Напишите /game чтобы начать новый раунд или /stats; /settings; /quit...")
    print()
def control_panel(command):
    """ основная функция для управления программой """
    if command=="/quit":
        return #выход из функции, а тк функция последняя консоль закрывается

    elif command=="/help":
        print()
        print(' Это программа/бот для игры в "Камень-Ножницы-Бумага с классическими правилами". \n'
                ' Игры проходят партиями, в каждой партии три раунда. Побеждает та сторона, которая \n'
                ' выигрывает большее количество раундов в партии.\n\n'
                ' Доступные команды: \n'
                ' /help - о программе и как ей пользоваться\n'
                ' /game - начать партию\n'
                ' /quit - закрыть программу\n'
                ' /settings - настройки программы (можно установить кол-во ходов в одной партии)\n'
                ' /stats - посмотреть всю статистику игры ( кол-во партий/побед/проигрышей/ничьих;процент побед;\n'
                '                                           наибольшее кол-во партий(побед) подряд; наигранное время )')
        print()
        control_panel(input(" "))

    elif command=="/settings":
        global moves_in_round #так функция game() увидит изменения
        moves_in_round=int(input(" Введите кол-во ходов в одном раунде (стандартное кол-во = 3): "))
        print()
        control_panel(input(" "))

    elif command=="/game":
        global count_game #кол-во партий (счетчик)
        count_game+=1
        game()
        control_panel(input(" "))
    elif command=="/stats":
        if count_game!=0:
            print(f" Кол-во сыгранных партий: {count_game}\n"
                  f" Кол-во выигранных партий: {count_win} ({count_win/count_game*100}%)\n"
                  f" Кол-во проигранных партий: {count_lost} ({count_lost/count_game*100}%)\n"
                  f" Кол-во ничьих: {count_draw} ({count_draw/count_game*100}%)\n"
                  f" Winstreak = {last_winstreak}\n"
                  f" Время проведенное в программе: {time.time()-start_time}")
        else:
            print((" Сыграйте партию и тут появится больше статистики.\n"
                   f" Время проведенное в программе: {round((time.time()-start_time)/60, 2)}мин"))
        print()
        control_panel(input(" "))
    else:
        print()
        print(" Введите коректную команду")
        control_panel(input(" "))



print()
input(" PRESS ENTER TO START ")
start_time=time.time() #время начала работы программы, для статисктики
print()
print(" Напишите /help, чтобы узнать о программе; \n"
      " если вы готовы начать, напишите нужную вам команду.")
print()

#factory settings
moves_in_round=3 #кол-во игр в одной партии
count_game, count_win, count_lost, count_draw, winstreak, last_winstreak=0,0,0,0,0,0 #счетчики
player_choices=[] #список в котором сохраняются все ходы игрока
bot_choices=[] #список в котором сохраняются все ходы бота
rating_choices=[]

control_panel(input(" "))