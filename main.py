class RegisterGuest:
    '''Создание пользователя. Принимает на вход имя и уникальный id
    история, которая используется для undo изначально пустая'''

    def __init__(self, name, user_id):
        self.user_id = user_id
        self.name = name
        self.history = []

class AddRoom:
    '''Создание комната. Принимает на вход только номер комнаты.
    Изначально комната свободна и не привязана к пользователю'''

    def __init__(self, number):
        self.number = number
        self.status = "свободно"
        self.current_user = None

class Command:
    '''Родительский класс для всех команд'''

    def execute(self, user, room):
        pass

    def undo(self, user, room):
        pass

class CreateBooking(Command):
    '''Бронирование комнаты'''

    def execute(self, user, room):
        '''На вход получает два объекта: пользователя и комнату'''
        if room.status == "свободно":
            room.status = 'забронировано'
            room.current_user = user.user_id
            user.history.append((room.status, user.user_id))
            print(f'Комната {room.number} забронирована {user.name}')
        else:
            print('Вы не можете забронировать этот номер')

    def undo(self, user, room):
        '''Отмена брони на вход также получает два объекта: пользователя и комнату
        Работает только если последняя операция была бронь, причём той же комнаты'''
        stat, us_id = user.history[-1]
        if stat == room.status and user.user_id == us_id:
            room.status = "свободно"
            room.current_user = None
            print("Бронь отменена (с помощью UNDO)")
        else:
            print("Вы не можете снять бронь (с помощью UNDO)")

class CancelBooking(Command):
    '''Отмена брони не зависимо от последней операции(в любой момент)'''

    def execute(self, user, room):
        '''На вход получает два объекта: пользователя и комнату'''
        if room.current_user == user.user_id and room.status == 'забронировано':
            room.status = 'свободно'
            room.current_user = None
            user.history.append((room.status, user.user_id))
            print(f'Комната {room.number} разбронирована {user.name}')
        else:
            print("Вы не можете снять бронь")

    def undo(self, user, room):
        '''Отмена отмены брони! на вход также получает два объекта: пользователя и комнату
        Работает только если последняя операция была отмена брони, причём той же комнаты'''
        stat, us_id = user.history[-1]
        if stat == room.status and user.user_id == us_id:
            room.status = "забронировано"
            room.current_user = user.user_id
            print("Бронь востановленна (с помощью UNDO)")
        else:
            print("Вы не можете востановить бронь (с помощью UNDO)")

class CheckIn(Command):
    '''Заезд в номер'''

    def execute(self, user, room):
        '''На вход получает два объекта: пользователя и комнату'''
        if room.status == 'свободно':
            room.status = 'занят'
            room.current_user = user.user_id
            user.history.append((room.status, user.user_id))
            print(f'Комната {room.number} занята {user.name}')
        elif room.status == 'забронировано' and user.user_id == room.current_user:
            room.status = 'занят'
            user.history.append((room.status, user.user_id))
            print(f'Комната {room.number} занята {user.name}')
        else:
            print('Вы не можете заехать в этот номер')

    def undo(self, user, room):
        '''Отмена въезда в номер. На вход также получает два объекта: пользователя и комнату
        Работает только если последняя операция была въезд, причём в ту же комнату '''
        stat, us_id = user.history[-1]
        if stat == room.status and user.user_id == us_id:
            room.status = "свободно"
            room.current_user = None
            print("Въезд отменён (с помощью UNDO)")
        else:
            print("Вы не можете отменить въезд (с помощью UNDO)")

class CheckOut(Command):
    '''Выезд из номера'''
    def execute(self, user, room):
        '''На вход получает два объекта: пользователя и комнату'''
        if room.status == 'занят' and user.user_id == room.current_user:
            room.status = 'свободно'
            room.current_user = None
            user.history.append((room.status, user.user_id))
            print(f'Комната {room.number} освобождена {user.name}')
        else:
            print('Вы не сможете выехать! :)')

    def undo(self, user, room):
        '''Отмена отмены выезда! На вход также получает два объекта: пользователя и комнату
        Работает только если последняя операция была выезд, причём из той же комнаты'''
        stat, us_id = user.history[-1]
        if stat == room.status and user.user_id == us_id:
            room.status = "занята"
            room.current_user = user.user_id
            print("Выезд отменён (с помощью UNDO)")
        else:
            print("Вымитайтесь! Вам тут не рады! (с помощью UNDO)")

class HotelBookingSystem:
    def cmd(self, command, user, room):
        command.execute(user, room)

#Создаём процессор
proces = HotelBookingSystem()

# Создание пользователей
user1 = RegisterGuest('Марк', '0001')
user2 = RegisterGuest('Нина', '0002')

# Создание комнта
room1 = AddRoom('1')
room2 = AddRoom('2')
room3 = AddRoom('3')

#Пример брони и её снятий
print("БРОНЬ И ЕЁ ОТМЕНА:")
proces.cmd(CreateBooking(), user1, room1)
proces.cmd(CreateBooking(), user2, room1)
proces.cmd(CancelBooking(), user2, room1)
proces.cmd(CancelBooking(), user1, room1)
print("--------------------------------------------")

#Въезд и выезд
print("ВЫЕЗДЫ И ВЪЕЗДЫ:")
proces.cmd(CheckIn(), user1, room1)
proces.cmd(CheckIn(), user2, room1)
proces.cmd(CheckOut(), user1, room1)
proces.cmd(CheckIn(), user2, room1)
print("--------------------------------------------")

#UNDO
print("ПРИМЕРЫ РАБОТЫ UNDO:")
print("ОТМЕНА БРОНИ UNDO")
proces.cmd(CreateBooking(), user1, room3)
CreateBooking().undo(user1, room3)
print("--------------------------------------------")

print("ПРИМЕРЫ РАБОТЫ UNDO:")
print("ОТМЕНА ОТМЕНЫ БРОНИ UNDO")
proces.cmd(CreateBooking(), user1, room3)
proces.cmd(CancelBooking(), user1, room3)
CancelBooking().undo(user1, room3)
print("--------------------------------------------")

print("ПРИМЕРЫ РАБОТЫ UNDO:")
print("ОТМЕНА ЗАНЯТИЯ КОМНАТЫ UNDO")
proces.cmd(CheckIn(), user1, room3)
CheckIn().undo(user1, room3)
print("--------------------------------------------")

print("ПРИМЕРЫ РАБОТЫ UNDO:")
print("ОТМЕНА ОТМЕНЫ ОСВОБОЖДЕНИЯ КОМНАТЫ UNDO")
proces.cmd(CheckIn(), user1, room3)
proces.cmd(CheckOut(), user1, room3)
CheckOut().undo(user1, room3)
print("--------------------------------------------")
