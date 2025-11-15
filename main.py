import os
import telebot
from telebot import types
import sqlite3
import random
import threading
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
# ЗАМЕНИТЕ НА ВАШ ТОКЕН
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

CASES = [
    "Уехал жить в лондон",
    "Насрал в лоток кота",
    "Отобрал у соседа слева носок и выставил на аукцион",
    "Должен соседу справа наследство и не отдает",
    "Обзывал Дуэйна Скалу Джонсона",
    "Ушел в баню один и никого не позвал",
    "Выкурил весь табак в Новосибирске",
    "Разработал MAX",
    "Не поставил лайк на видео с котиками",
    "Переставил всю мебель в спальне на 5 см влево",
    "Создал инсту домашнему кактусу и накрутил 10к подписчиков",
    "Научил гпт отвечать только рэпом",
    "Съел последнюю шаурму в холодильнике",
    "Переименовал все контакты в телефоне на 'Серега заправщик'",
    "Заменил все зеркала в доме на портреты себя",
    "Научил попугая материться на трёх языках",
    "Покрасил соседскую машину в коралловый",
    "Заказал 100 пицц на чужой адрес",
    "Создал фейковый профиль и начал встречаться сам с собой",
    "Поставил на рингтон стон вомбата",
    "Перевел все часы в доме на час назад",
    "Подписал соседа на 50 рассылок про йогу",
    "Съел чужой обед и оставил записку 'Было вкусно'",
    "Запустил слух что отменили пятницу",
    "Заменил фото в паспорте на фотку мактрахера",
    "Продал NFT скриншота чужого мема",
    "Организовал движение 'Ходить задом наперёд'",
    "Заказал 500 резиновых уточек в универ",
]

CHARACTERS = [
    "Макан в армии",
    "Гадалка в отставке"
    "Непьющий пират",
    "Тиктокер-философ",
    "Фитнес модель с дипломом по квантовой физике",
    "Ученый, изучающий природу тупости",
    "Ярый поклонник теорий заговора",
    "Робот доставщик Яндекса",
    "Спецагент под прикрытием в образе мамы судьи",
    "Эксперт по культуре свэга",
    "Охотник за привидениями",
    "Коллекционер дикпиков",
    "Телепат неудачник",
    "Агент по недвижимости на марсе",
    "Критик современного искусства",
    "Бывший ютубер с 5 подписчиками",
    "Астролог который не верит в гороскопы",
    "Веган который тайно ест шаурму",
    "Геймер с психологическим образованием",
    "Коуч по тайм-менеджменту который всегда опаздывает",
    "Профессиональный прокрастинатор",
    "Сомелье энергетиков",
    "Эксперт по мемам при правительстве",
    "Переводчик с собачьего на человеческий",
    "Спидранер жизни",
    "NFT-художник который не понимает что такое NFT",
    "Специалист по древним мемам",
    "Консультант по выбору носков",
    "Профессиональный спорщик в интернете",
]

WORDS = [
	"Завоз", "Айсгергерт", "Банан", "Водка", "Лабуба",
	"Скуф", "Стрим", "Хинкали", "Абстрактный", "Артефакт",
	"Летопись", "Эволюция", "Книга", "Аллергия", "Бытие",
	"Свобода", "Ответственность", "Торнадо", "Затмение",
	"Радуга", "Портал", "Лабиринт", "Кристалл", "Моргенштерн",
	"Зеркало", "Лес", "Звезда", "Часы", "Дождь", "Футбол",
	"Утка", "Носок", "Гравитация", "Блогер", "Майонез",
	"Теория заговора", "Космос", "Бабушка", "Крипта", "Ведро",
	"Любовь", "Робот", "Подушка", "Пришелец", "Сковорода", "Велосипед",
	"Зубная фея", "Супергерой", "Ананас", "Кофе", "Единорог", "Интернет",
	"Пицца", "Телепорт", "Носорог", "Вафля", "Магнит", "Селфи", "Хомяк",
  	"Джокер",  "Флекс", "Хайп", "Скам", "Абьюз""Буллинг", "Токсик",
   	"Драма","Баг", "Дроп", "Лаг", "Скилл", "Читер", "Спидран", "Легенда",
    "Борщ", "Шашлык", "Самогон", "Балалайка", "Медведь", "Ушанка",
]

SECRET_GOALS = [
    "Доказать, что преступление совершено по наивысшей тупости",
    "Обвинить в сговоре с инопланетянами",
    "Свалить всё на домашнее животное",
    "Утверждать, что мотив - зависть к знаменитости",
    "Настаивать, что это был ритуал для вступления в ...",
    "Доказать, что преступник вдохновлялся аниме",
    "Обвинить в попытке стать инфоцыганом",
    "Утверждать, что это месть за старую обиду",
    "Связать преступление с лунными фазами",
    "Утверждать, что это социальный эксперимент",
    "Связать с квантовой физикой",
    "Обвинить в зависимости от инстаграма",
    "Утверждать, что это было сделано ради популярности",
    "Свалить на сбой в матрице",
    "Настаивать что это часть тренда из тиктока",
    "Связать с теорией плоской земли",
    "Доказать что это было предсказано в симпсонах",
    "Обвинить в том что хотел стать мемом",
    "Утверждать что действовал по советам чатгпт",
    "Утверждать что это было во сне",
    "Доказать что виноват т9",
    "Связать с кармой из прошлой жизни",
]

CHAOS_CARDS = [
    "Новый свидетель! (указать на любого зрителя, он дает показания)",
    "30 секунд никто не может говорить, только мычать!",
    "Обвиняемый плачет и хочет всё признать!",
    "Улика найдена! (достать любой предмет)",
    "Адвокат подкуплен! (адвокат поддерживает обвинение 1 минуту)",
    "Свидетель обвинения меняет показания!",
    "Прокурор забыл о чём говорил!",
    "В зал врывается неизвестный!"
    "Обвиняемый должен петь свои аргументы",
    "Прокурор получает анонимку и меняет стратегию",
    "Появляется эксперт (случайный зритель) и дает заключение",
    "Кто-то из судебных чихает и все теряют мысль",
]

SPECIAL_EFFECTS = [
    "Все следующую минуту говорят как пираты!",
    "Обвиняемый может отвечать только 'Да' или 'Нет'",
    "Прокурор должен говорить с французским акцентом",
    "Свидетель должен использовать в речи движения танца",
    "Адвокат должен ссылаться только на сказки",
    "Пафос в речи каждого +200",
    "Адвокат защищается только мемами",
    "Прокурор должен использовать научные термины",
    "Обвиняемый может говорить только вопросами",
    "Судья требует говорить максимально драматично",
    "Адвокат защищает обвиняемого через философию",
    "Прокурор обвиняет как политик на дебатах",
]

ROLES = {
    'judge': '🤵 СУДЬЯ',
    'prosecutor': '👨‍⚖️ ПРОКУРОР',
    'witness': '🕵️‍♂️ СВИДЕТЕЛЬ ОБВИНЕНИЯ',
    'lawyer': '👨‍💻 АДВОКАТ',
    'accused': '😎 ОБВИНЯЕМЫЙ',
    'journalist': '📢 ЖУРНАЛИСТ',
    'jury': '👥 ПРИСЯЖНЫЙ'
}

# Хранилище активных игр (в памяти)
active_games = {}  # {game_id: {'admin_id': ..., 'players': [], 'status': ...}}

# Режим отладки
DEBUG_MODE = os.getenv('DEBUG_MODE') == 'True'
MIN_PLAYERS = 1 if DEBUG_MODE else 6  # Всегда 10 игроков в реальной игре
MAX_PLAYERS = 10
ROUND_TIME = 2 * 60 if DEBUG_MODE else 15 * 60
VOTE_TIME = 1 * 60 if DEBUG_MODE else 3 * 60

# Инициализация БД
def init_db():
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS games
                 (game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  admin_id INTEGER,
                  players_count INTEGER DEFAULT 0,
                  current_round INTEGER DEFAULT 0,
                  total_rounds INTEGER DEFAULT 5,
                  status TEXT DEFAULT 'setup',
                  current_case TEXT,
                  game_code TEXT UNIQUE,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS players
                 (player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  game_id INTEGER,
                  user_id INTEGER,
                  username TEXT,
                  display_name TEXT,
                  current_role TEXT,
                  score INTEGER DEFAULT 0,
                  FOREIGN KEY (game_id) REFERENCES games(game_id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS user_names
                 (user_id INTEGER PRIMARY KEY,
                  display_name TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS rounds
                 (round_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  game_id INTEGER,
                  round_number INTEGER,
                  case_text TEXT,
                  winner_team TEXT,
                  started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (game_id) REFERENCES games(game_id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS group_games
                 (game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  chat_id INTEGER UNIQUE,
                  admin_id INTEGER,
                  players_count INTEGER DEFAULT 0,
                  current_round INTEGER DEFAULT 0,
                  total_rounds INTEGER DEFAULT 5,
                  status TEXT DEFAULT 'setup',
                  current_case TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()


# Генерация уникального кода игры (4 символа)
def generate_game_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))

# Получение или запрос имени пользователя
def get_user_display_name(user_id):
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT display_name FROM user_names WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def save_user_display_name(user_id, display_name):
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO user_names (user_id, display_name) VALUES (?, ?)",
              (user_id, display_name))
    conn.commit()
    conn.close()

# Команда /start
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat_type = message.chat.type

    # Если команда в группе - создаём игру в группе
    if chat_type in ['group', 'supergroup']:
        create_game_in_group(message)
    else:
        # Проверяем, есть ли параметр (например: /start group_123)
        args = message.text.split()

        display_name = get_user_display_name(user_id)

        if not display_name:
            # Если имени нет - сначала запрашиваем имя
            bot.send_message(user_id,
                "👋 Привет! Добро пожаловать в игру *'Судный День: Битва Носков'*!\n\n"
                "Сначала представьтесь - как вас называть в игре?\n"
                "_(Введите своё игровое имя)_",
                parse_mode='Markdown'
            )
            # Передаем параметр дальше через register_next_step_handler
            if len(args) > 1:
                bot.register_next_step_handler(message, lambda m: process_user_name_with_param(m, args[1]))
            else:
                bot.register_next_step_handler(message, process_user_name)
        else:
            # Если имя уже есть - проверяем параметр
            if len(args) > 1 and args[1].startswith('group_'):
                # Автоматически присоединяем к групповой игре
                game_id = int(args[1].split('_')[1])
                auto_join_group_game(user_id, game_id, display_name)
            else:
                show_main_menu(user_id, display_name)

def create_game_in_group(message):
    chat_id = message.chat.id
    admin_id = message.from_user.id

    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    # Проверяем, есть ли активная игра в этой группе
    c.execute("SELECT game_id, status FROM group_games WHERE chat_id = ?", (chat_id,))
    existing = c.fetchone()

    if existing and existing[1] != 'finished':
        bot.send_message(chat_id, "❗️ В этой группе уже есть активная игра! Используйте /cancelgroup чтобы отменить её.")
        conn.close()
        return

    # Создаем игру в группе
    c.execute("INSERT INTO group_games (chat_id, admin_id) VALUES (?, ?)", (chat_id, admin_id))
    game_id = c.lastrowid
    conn.commit()
    conn.close()

    # Инициализируем в памяти с префиксом 'group_'
    active_games[f'group_{game_id}'] = {
        'admin_id': admin_id,
        'chat_id': chat_id,
        'players': [],
        'status': 'setup',
        'votes': {'guilty': 0, 'innocent': 0}
    }

    # Кнопка для присоединения
    markup = types.InlineKeyboardMarkup()
    bot_username = bot.get_me().username
    btn_join = types.InlineKeyboardButton("➕ Я играю!", url=f"https://t.me/{bot_username}?start=group_{game_id}")
    btn_start = types.InlineKeyboardButton("🎬 Начать раунд 1", callback_data=f"start_group_round_{game_id}")
    markup.row(btn_join)
    markup.row(btn_start)

    debug_info = f"\n\n🔧 *Режим отладки* (мин. {MIN_PLAYERS} игроков)" if DEBUG_MODE else ""

    bot.send_message(chat_id,
        f"🎮 *СПИДРАН ПО СУДИМОСТИ*\n\n"
        f"Игра создана в группе!\n\n"
        f"👥 Нужно игроков: {MIN_PLAYERS}-{MAX_PLAYERS}\n"
        f"📝 Присоединившихся: 0\n\n"
        f"❗️ *ВАЖНО:* Перед тем как нажать кнопку, напишите боту в личку /start и представьтесь!\n\n"
        f"Нажмите '➕ Я играю!' чтобы присоединиться!{debug_info}",
        parse_mode='Markdown',
        reply_markup=markup
    )

def join_group_game(call, game_id):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Проверяем есть ли имя у пользователя
    display_name = get_user_display_name(user_id)

    if not display_name:
        bot.answer_callback_query(call.id,
            "❗️ Сначала напишите мне в личку /start и представьтесь!",
            show_alert=True)
        return

    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT status, players_count FROM group_games WHERE game_id = ?", (game_id,))
    game = c.fetchone()

    if not game:
        bot.answer_callback_query(call.id, "❗️ Игра не найдена", show_alert=True)
        conn.close()
        return

    status, players_count = game

    if status != 'setup':
        bot.answer_callback_query(call.id, "❗️ Игра уже началась", show_alert=True)
        conn.close()
        return

    if players_count >= MAX_PLAYERS:
        bot.answer_callback_query(call.id, f"❗️ Игра полна ({MAX_PLAYERS} игроков)", show_alert=True)
        conn.close()
        return

    # Проверяем, не добавлен ли уже
    c.execute("SELECT player_id FROM players WHERE game_id = ? AND user_id = ?", (game_id, user_id))
    if c.fetchone():
        bot.answer_callback_query(call.id, "✅ Вы уже в игре!")
        conn.close()
        return

    # Добавляем игрока
    c.execute("INSERT INTO players (game_id, user_id, username, display_name) VALUES (?, ?, ?, ?)",
              (game_id, user_id, '', display_name))
    c.execute("UPDATE group_games SET players_count = players_count + 1 WHERE game_id = ?", (game_id,))

    c.execute("SELECT players_count FROM group_games WHERE game_id = ?", (game_id,))
    new_count = c.fetchone()[0]

    # Получаем список всех игроков
    c.execute("SELECT display_name FROM players WHERE game_id = ?", (game_id,))
    all_players = c.fetchall()
    players_list = ", ".join([p[0] for p in all_players])

    conn.commit()
    conn.close()

    # Обновляем в памяти
    if f'group_{game_id}' in active_games:
        active_games[f'group_{game_id}']['players'].append({'user_id': user_id, 'display_name': display_name})

    bot.answer_callback_query(call.id, f"✅ Вы присоединились как {display_name}!")

    # Обновляем сообщение в группе
    markup = types.InlineKeyboardMarkup()
    btn_join = types.InlineKeyboardButton("➕ Я играю!", callback_data=f"join_group_{game_id}")
    btn_start = types.InlineKeyboardButton("🎬 Начать раунд 1", callback_data=f"start_group_round_{game_id}")
    markup.row(btn_join)
    markup.row(btn_start)

    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"🎮 *СУДНЫЙ ДЕНЬ: БИТВА НОСКОВ*\n\n"
                 f"Игра создана в группе!\n\n"
                 f"👥 Игроков: {new_count}/{MAX_PLAYERS}\n"
                 f"📝 Присоединились: {players_list}\n\n"
                 f"❗️ *ВАЖНО:* Новым игрокам нужно сначала написать боту /start в личку!\n\n"
                 f"Когда все готовы - админ нажимает 'Начать раунд 1'",
            parse_mode='Markdown',
            reply_markup=markup
        )
    except:
        pass

    # Отправляем подтверждение в личку
    try:
        bot.send_message(user_id,
            f"✅ Вы присоединились к групповой игре!\n"
            f"👥 Игроков: {new_count}/{MAX_PLAYERS}\n\n"
            f"Ожидайте начала раунда."
        )
    except:
        pass

def start_group_round(game_id, admin_id, chat_id):
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    # Проверяем права
    c.execute("SELECT admin_id, players_count, current_round, total_rounds FROM group_games WHERE game_id = ?", (game_id,))
    game = c.fetchone()

    if not game:
        conn.close()
        return

    db_admin_id, players_count, current_round, total_rounds = game

    if db_admin_id != admin_id:
        try:
            bot.answer_callback_query(admin_id, "❗️ Только создатель игры может начать раунд", show_alert=True)
        except:
            pass
        conn.close()
        return

    if players_count < MIN_PLAYERS:
        try:
            bot.send_message(chat_id, f"❗️ Недостаточно игроков! Нужно {MIN_PLAYERS}, есть: {players_count}")
        except:
            pass
        conn.close()
        return

    # Обновляем раунд
    new_round = current_round + 1
    if new_round > total_rounds:
        end_group_game(game_id, chat_id)
        conn.close()
        return

    # Выбираем дело
    case = random.choice(CASES)

    c.execute("UPDATE group_games SET current_round = ?, status = 'playing', current_case = ? WHERE game_id = ?",
              (new_round, case, game_id))

    # Получаем игроков
    c.execute("SELECT player_id, user_id, display_name FROM players WHERE game_id = ?", (game_id,))
    players = c.fetchall()

    # Раздаём роли
    available_roles = ['judge', 'prosecutor', 'witness', 'lawyer', 'accused', 'journalist']
    jury_count = max(0, len(players) - len(available_roles))
    available_roles.extend(['jury'] * jury_count)

    random.shuffle(available_roles)

    # Сохраняем раунд
    c.execute("INSERT INTO rounds (game_id, round_number, case_text) VALUES (?, ?, ?)",
              (game_id, new_round, case))

    # Раздаём карточки
    roles_assignment = []
    for i, (player_id, user_id, display_name) in enumerate(players):
        role = available_roles[i]
        c.execute("UPDATE players SET current_role = ? WHERE player_id = ?", (role, player_id))

        roles_assignment.append(f"{ROLES[role]}: {display_name}")

        # Отправляем карточки
        try:
            send_role_card(user_id, role, case, new_round, total_rounds)
        except Exception as e:
            print(f"Ошибка отправки карточки {display_name}: {e}")

    conn.commit()

    # Сброс голосов
    if f'group_{game_id}' in active_games:
        active_games[f'group_{game_id}']['votes'] = {'guilty': 0, 'innocent': 0}
        active_games[f'group_{game_id}']['status'] = 'playing'

    conn.close()

    # Объявляем начало раунда в группе
    markup = types.InlineKeyboardMarkup()
    btn_end = types.InlineKeyboardButton("⏱ Закончить раунд", callback_data=f"end_group_round_{game_id}")
    markup.add(btn_end)

    time_info = f"{ROUND_TIME//60} мин" if ROUND_TIME >= 60 else f"{ROUND_TIME} сек"

    bot.send_message(chat_id,
        f"🎬 *РАУНД {new_round}/{total_rounds} НАЧАЛСЯ!*\n\n"
        f"⚖️ *ДЕЛО:*\n_{case}_\n\n"
        f"*РОЛИ:*\n" + "\n".join(roles_assignment) + "\n\n"
        f"⏰ Рекомендованное время: {time_info}\n\n"
        f"Карточки отправлены всем игрокам в личку.",
        parse_mode='Markdown',
        reply_markup=markup
    )

def end_group_round_voting(game_id, admin_id, chat_id):
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT admin_id FROM group_games WHERE game_id = ?", (game_id,))
    game = c.fetchone()

    if not game or game[0] != admin_id:
        try:
            bot.send_message(chat_id, "❗️ Только создатель игры может завершить раунд")
        except:
            pass
        conn.close()
        return

    # Получаем всех игроков с их ролями
    c.execute("SELECT user_id, display_name, current_role FROM players WHERE game_id = ?", (game_id,))
    players = c.fetchall()
    conn.close()

    # Отправляем голосование только ПРИСЯЖНЫМ
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_guilty = types.InlineKeyboardButton("✅ ВИНОВЕН", callback_data=f"vote_group_guilty_{game_id}")
    btn_innocent = types.InlineKeyboardButton("❌ НЕ ВИНОВЕН", callback_data=f"vote_group_innocent_{game_id}")
    markup.add(btn_guilty, btn_innocent)

    voting_players = []
    for user_id, display_name, role in players:
        if role == 'jury':
            voting_players.append(display_name)
            try:
                bot.send_message(user_id,
                    "⏰ *ВРЕМЯ ГОЛОСОВАНИЯ!*\n\n"
                    "👥 Вы - присяжный. Принимайте решение:",
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            except:
                pass

    # Кнопка для показа результатов в группе
    admin_markup = types.InlineKeyboardMarkup()
    btn_show = types.InlineKeyboardButton("📊 Показать результаты", callback_data=f"show_group_results_{game_id}")
    admin_markup.add(btn_show)

    voters_list = ", ".join(voting_players) if voting_players else "нет присяжных"

    bot.send_message(chat_id,
        f"⏰ *ГОЛОСОВАНИЕ!*\n\n"
        f"👥 Голосуют присяжные: {voters_list}\n\n"
        f"Когда все проголосуют - админ нажимает кнопку ниже:",
        parse_mode='Markdown',
        reply_markup=admin_markup
    )


def show_group_results(game_id, chat_id):
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    if f'group_{game_id}' not in active_games:
        active_games[f'group_{game_id}'] = {'votes': {'guilty': 0, 'innocent': 0}}

    votes = active_games[f'group_{game_id}']['votes']
    guilty_votes = votes.get('guilty', 0)
    innocent_votes = votes.get('innocent', 0)

    if guilty_votes > innocent_votes:
        verdict = "ВИНОВЕН"
        winner_team = "prosecution"
        emoji = "⚖️"
    elif innocent_votes > guilty_votes:
        verdict = "НЕ ВИНОВЕН"
        winner_team = "defense"
        emoji = "🎉"
    else:
        verdict = "НИЧЬЯ"
        winner_team = "tie"
        emoji = "🤝"

    # Обновляем очки
    if winner_team == "prosecution":
        c.execute("""UPDATE players SET score = score + 2
                     WHERE game_id = ? AND current_role IN ('prosecutor', 'witness', 'judge')""",
                  (game_id,))
    elif winner_team == "defense":
        c.execute("""UPDATE players SET score = score + 2
                     WHERE game_id = ? AND current_role IN ('lawyer', 'accused')""",
                  (game_id,))

    c.execute("""UPDATE rounds SET winner_team = ?
                 WHERE game_id = ? AND round_number = (SELECT current_round FROM group_games WHERE game_id = ?)""",
              (winner_team, game_id, game_id))

    c.execute("SELECT current_round, total_rounds FROM group_games WHERE game_id = ?", (game_id,))
    current_round, total_rounds = c.fetchone()

    conn.commit()
    conn.close()

    # Сброс голосов
    active_games[f'group_{game_id}']['votes'] = {'guilty': 0, 'innocent': 0}

    # Результаты
    result_text = (
        f"{emoji} *ВЕРДИКТ: {verdict}!*\n\n"
        f"📊 Голосов 'Виновен': {guilty_votes}\n"
        f"📊 Голосов 'Не виновен': {innocent_votes}\n\n"
    )

    if winner_team != "tie":
        result_text += f"✨ Команда {'обвинения' if winner_team == 'prosecution' else 'защиты'} получает +2 очка!"
    else:
        result_text += "🤝 Ничья! Очки не начисляются."

    # Кнопки для следующего раунда
    markup = types.InlineKeyboardMarkup(row_width=1)

    if current_round < total_rounds:
        btn_next = types.InlineKeyboardButton(f"➡️ Начать раунд {current_round + 1}", callback_data=f"start_group_round_{game_id}")
        btn_end = types.InlineKeyboardButton("🏁 Завершить игру", callback_data=f"end_group_game_{game_id}")
        markup.add(btn_next, btn_end)

        bot.send_message(chat_id,
            result_text + f"\n\n📊 Раунд {current_round}/{total_rounds} завершён.",
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        end_group_game(game_id, chat_id)


def end_group_game(game_id, chat_id):
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT display_name, score FROM players WHERE game_id = ? ORDER BY score DESC", (game_id,))
    players = c.fetchall()

    c.execute("UPDATE group_games SET status = 'finished' WHERE game_id = ?", (game_id,))
    conn.commit()
    conn.close()

    if players:
        leaderboard = "\n".join([f"{i+1}. {p[0]}: {p[1]} 🏆" for i, p in enumerate(players)])
        winner = players[0]

        result_text = (
            f"🏆 *ИГРА ЗАВЕРШЕНА!*\n\n"
            f"*ИТОГОВАЯ ТАБЛИЦА:*\n{leaderboard}\n\n"
            f"🎉 *ПОБЕДИТЕЛЬ: {winner[0]}* с {winner[1]} очками!\n\n"
            f"Спасибо за игру!"
        )

        bot.send_message(chat_id, result_text, parse_mode='Markdown')

    # Удаляем из памяти
    if f'group_{game_id}' in active_games:
        del active_games[f'group_{game_id}']

@bot.message_handler(commands=['cancelgroup'])
def cancel_group_command(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_type = message.chat.type

    if chat_type not in ['group', 'supergroup']:
        bot.send_message(user_id, "❗️ Эта команда работает только в группах")
        return

    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT game_id, admin_id FROM group_games WHERE chat_id = ? AND status != 'finished'", (chat_id,))
    game = c.fetchone()

    if not game:
        bot.send_message(chat_id, "❗️ Нет активной игры в этой группе")
        conn.close()
        return

    game_id, admin_id = game

    if admin_id != user_id:
        bot.send_message(chat_id, "❗️ Только создатель игры может её отменить")
        conn.close()
        return

    c.execute("DELETE FROM players WHERE game_id = ?", (game_id,))
    c.execute("DELETE FROM rounds WHERE game_id = ?", (game_id,))
    c.execute("DELETE FROM group_games WHERE game_id = ?", (game_id,))
    conn.commit()
    conn.close()

    if f'group_{game_id}' in active_games:
        del active_games[f'group_{game_id}']

    bot.send_message(chat_id, "✅ Групповая игра отменена.")


def process_user_name(message):
    user_id = message.from_user.id
    display_name = message.text.strip()[:30]  # Ограничение 30 символов

    if len(display_name) < 2:
        bot.send_message(user_id, "❗️ Имя слишком короткое. Введите минимум 2 символа:")
        bot.register_next_step_handler(message, process_user_name)
        return

    save_user_display_name(user_id, display_name)
    bot.send_message(user_id, f"✅ Отлично, {display_name}!")
    show_main_menu(user_id, display_name)

def process_user_name_with_param(message, param):
    """Обработка имени с последующим автоприсоединением"""
    user_id = message.from_user.id
    display_name = message.text.strip()[:30]

    if len(display_name) < 2:
        bot.send_message(user_id, "❗️ Имя слишком короткое. Введите минимум 2 символа:")
        bot.register_next_step_handler(message, lambda m: process_user_name_with_param(m, param))
        return

    save_user_display_name(user_id, display_name)
    bot.send_message(user_id, f"✅ Отлично, {display_name}!")

    # Автоматически присоединяем к игре
    if param.startswith('group_'):
        game_id = int(param.split('_')[1])
        auto_join_group_game(user_id, game_id, display_name)


def auto_join_group_game(user_id, game_id, display_name):
    """Автоматическое присоединение к групповой игре"""
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT chat_id, status, players_count FROM group_games WHERE game_id = ?", (game_id,))
    game = c.fetchone()

    if not game:
        bot.send_message(user_id, "❗️ Игра не найдена или уже завершена")
        conn.close()
        return

    chat_id, status, players_count = game

    if status != 'setup':
        bot.send_message(user_id, "❗️ Игра уже началась")
        conn.close()
        return

    if players_count >= MAX_PLAYERS:
        bot.send_message(user_id, f"❗️ Игра полна ({MAX_PLAYERS} игроков)")
        conn.close()
        return

    # Проверяем, не добавлен ли уже
    c.execute("SELECT player_id FROM players WHERE game_id = ? AND user_id = ?", (game_id, user_id))
    if c.fetchone():
        bot.send_message(user_id, "✅ Вы уже в этой игре!")
        conn.close()
        return

    # Добавляем игрока
    c.execute("INSERT INTO players (game_id, user_id, username, display_name) VALUES (?, ?, ?, ?)",
              (game_id, user_id, '', display_name))
    c.execute("UPDATE group_games SET players_count = players_count + 1 WHERE game_id = ?", (game_id,))

    c.execute("SELECT players_count FROM group_games WHERE game_id = ?", (game_id,))
    new_count = c.fetchone()[0]

    conn.commit()
    conn.close()

    # Обновляем в памяти
    if f'group_{game_id}' in active_games:
        active_games[f'group_{game_id}']['players'].append({'user_id': user_id, 'display_name': display_name})

    bot.send_message(user_id,
        f"✅ Вы автоматически присоединились к игре!\n"
        f"👥 Игроков: {new_count}/{MAX_PLAYERS}\n\n"
        f"Ожидайте начала раунда.",
        parse_mode='Markdown'
    )

    # Уведомляем группу
    try:
        bot.send_message(chat_id, f"➕ *{display_name}* присоединился к игре! ({new_count}/{MAX_PLAYERS})", parse_mode='Markdown')
    except:
        pass

def show_main_menu(user_id, display_name):
    # Reply клавиатура (постоянная внизу)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_create = types.KeyboardButton("🎮 Создать игру")
    btn_join = types.KeyboardButton("➕ Присоединиться")
    btn_status = types.KeyboardButton("📋 Статус игры")
    btn_cancel = types.KeyboardButton("❌ Отмена")  # Быстрый доступ к cancel
    markup.add(btn_create, btn_join, btn_status, btn_cancel)

    bot.send_message(user_id,
        f"🎮 *СПИДРАН ПО СУДИМОСТИ*\n\n"
        f"Ваше имя: *{display_name}*\n\n"
        f"Используйте кнопки ниже для управления:",
        parse_mode='Markdown',
        reply_markup=markup
    )

# Обработка текстовых команд с Reply клавиатуры
@bot.message_handler(func=lambda message: message.text in ["🎮 Создать игру", "➕ Присоединиться", "📋 Статус игры", "❌ Отмена"])
def handle_keyboard_buttons(message):
    user_id = message.from_user.id
    text = message.text

    # Проверяем, есть ли имя пользователя
    display_name = get_user_display_name(user_id)
    if not display_name:
        bot.send_message(user_id, "❗️ Сначала введите своё имя. Используйте /start")
        return

    if text == "🎮 Создать игру":
        create_game(user_id, display_name, message)

    elif text == "➕ Присоединиться":
        bot.send_message(user_id, "Введите код игры (4 символа):")
        bot.register_next_step_handler(message, process_join_code)

    elif text == "📋 Статус игры":
        status_command(message)

    elif text == "❌ Отмена":
        # Вызываем логику /cancel
        cancel_command(message)

# Обработка callback кнопок (для inline кнопок в игре)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id

    if call.data == "rules":
        bot.answer_callback_query(call.id)
        show_rules(call.message)

    elif call.data == "roles":
        bot.answer_callback_query(call.id)
        show_roles(call.message)

    elif call.data.startswith("start_round_"):
        bot.answer_callback_query(call.id)
        game_id = int(call.data.split("_")[2])
        start_round(game_id, user_id)

    elif call.data.startswith("end_round_"):
        bot.answer_callback_query(call.id)
        game_id = int(call.data.split("_")[2])
        end_round_voting(game_id, user_id)

    elif call.data.startswith("vote_"):
        bot.answer_callback_query(call.id, "✅ Голос учтён!")
        handle_vote(call)

    elif call.data.startswith("next_round_"):
        bot.answer_callback_query(call.id)
        game_id = int(call.data.split("_")[2])
        start_round(game_id, user_id)

    elif call.data.startswith("end_game_"):
        bot.answer_callback_query(call.id)
        game_id = int(call.data.split("_")[2])
        end_game(game_id, user_id)

    elif call.data.startswith("join_group_"):
        game_id = int(call.data.split("_")[2])
        join_group_game(call, game_id)

    elif call.data.startswith("start_group_round_"):
        bot.answer_callback_query(call.id)
        game_id = int(call.data.split("_")[3])
        start_group_round(game_id, user_id, call.message.chat.id)

    elif call.data.startswith("end_group_round_"):
        bot.answer_callback_query(call.id)
        game_id = int(call.data.split("_")[3])
        end_group_round_voting(game_id, user_id, call.message.chat.id)

    elif call.data.startswith("vote_group_"):
        bot.answer_callback_query(call.id, "✅ Голос учтён!")
        game_id = int(call.data.split("_")[3])
        vote_type = call.data.split("_")[2]  # guilty или innocent

        if f'group_{game_id}' not in active_games:
            active_games[f'group_{game_id}'] = {'votes': {'guilty': 0, 'innocent': 0}}

        active_games[f'group_{game_id}']['votes'][vote_type] += 1
        bot.send_message(user_id, f"✅ Ваш голос '{vote_type.upper()}' учтён!")

    elif call.data.startswith("show_group_results_"):
        bot.answer_callback_query(call.id)
        game_id = int(call.data.split("_")[3])
        show_group_results(game_id, call.message.chat.id)

    elif call.data.startswith("end_group_game_"):
        bot.answer_callback_query(call.id)
        game_id = int(call.data.split("_")[3])
        end_group_game(game_id, call.message.chat.id)

# Создание игры
def create_game(admin_id, display_name, message):
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    # Проверяем, нет ли у админа активной игры
    c.execute("SELECT game_id FROM games WHERE admin_id = ? AND status != 'finished'", (admin_id,))
    existing = c.fetchone()

    if existing:
        bot.send_message(admin_id, "❗️ У вас уже есть активная игра! Используйте /cancel чтобы отменить её.")
        conn.close()
        return

    # Создаем игру
    game_code = generate_game_code()
    c.execute("INSERT INTO games (admin_id, game_code) VALUES (?, ?)", (admin_id, game_code))
    game_id = c.lastrowid

    # Админ автоматически становится игроком
    c.execute("INSERT INTO players (game_id, user_id, username, display_name) VALUES (?, ?, ?, ?)",
              (game_id, admin_id, '', display_name))
    c.execute("UPDATE games SET players_count = 1 WHERE game_id = ?", (game_id,))

    conn.commit()
    conn.close()

    # Инициализируем в памяти
    active_games[game_id] = {
        'admin_id': admin_id,
        'players': [{'user_id': admin_id, 'display_name': display_name}],
        'status': 'setup',
        'votes': {'guilty': 0, 'innocent': 0}
    }

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_start = types.InlineKeyboardButton("🎬 Начать раунд 1", callback_data=f"start_round_{game_id}")
    btn_rules = types.InlineKeyboardButton("📖 Правила", callback_data="rules")
    btn_roles = types.InlineKeyboardButton("🎭 Роли", callback_data="roles")
    # добавим кнопку отмены сюда тоже (инлайн-удобство для админа)
    btn_cancel_inline = types.InlineKeyboardButton("❌ Отменить игру", callback_data=f"end_game_{game_id}")
    markup.add(btn_start, btn_rules, btn_roles, btn_cancel_inline)

    debug_info = f"\n\n🔧 *Режим отладки*\nМин. игроков: {MIN_PLAYERS}" if DEBUG_MODE else ""

    bot.send_message(admin_id,
        f"✅ *ИГРА СОЗДАНА!*\n\n"
        f"🔑 *КОД ИГРЫ:* `{game_code}`\n\n"
        f"Отправьте этот код другим игрокам.\n"
        f"Они должны:\n"
        f"1. Открыть бота\n"
        f"2. Нажать 'Присоединиться'\n"
        f"3. Ввести код: `{game_code}`\n\n"
        f"👥 Игроков: 1/{MAX_PLAYERS}\n\n"
        f"Когда все готовы - нажмите 'Начать раунд 1'{debug_info}",
        parse_mode='Markdown',
        reply_markup=markup
    )

# Присоединение к игре
def process_join_code(message):
    user_id = message.from_user.id
    display_name = get_user_display_name(user_id)
    game_code = message.text.strip().upper()

    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    # Ищем игру по коду
    c.execute("SELECT game_id, status, admin_id, players_count FROM games WHERE game_code = ?", (game_code,))
    game = c.fetchone()

    if not game:
        bot.send_message(user_id, "❗️ Игра с таким кодом не найдена. Проверьте код и попробуйте снова.")
        conn.close()
        return

    game_id, status, admin_id, players_count = game

    if status != 'setup' and status != 'playing':
        bot.send_message(user_id, "❗️ Эта игра уже завершена.")
        conn.close()
        return

    if players_count >= MAX_PLAYERS:
        bot.send_message(user_id, f"❗️ Игра полна! Максимум {MAX_PLAYERS} игроков.")
        conn.close()
        return

    # Проверяем, не добавлен ли уже
    c.execute("SELECT player_id FROM players WHERE game_id = ? AND user_id = ?", (game_id, user_id))
    if c.fetchone():
        bot.send_message(user_id, "✅ Вы уже в этой игре!")
        conn.close()
        return

    # Добавляем игрока
    c.execute("INSERT INTO players (game_id, user_id, username, display_name) VALUES (?, ?, ?, ?)",
              (game_id, user_id, '', display_name))
    c.execute("UPDATE games SET players_count = players_count + 1 WHERE game_id = ?", (game_id,))

    # Получаем обновлённое количество
    c.execute("SELECT players_count FROM games WHERE game_id = ?", (game_id,))
    new_players_count = c.fetchone()[0]

    conn.commit()
    conn.close()

    # Обновляем в памяти
    if game_id in active_games:
        active_games[game_id]['players'].append({'user_id': user_id, 'display_name': display_name})

    bot.send_message(user_id,
        f"✅ Вы присоединились к игре!\n\n"
        f"🔑 Код игры: `{game_code}`\n"
        f"👥 Игроков: {new_players_count}/{MAX_PLAYERS}\n\n"
        f"Ожидайте начала раунда от администратора.",
        parse_mode='Markdown'
    )

    # Уведомляем админа
    bot.send_message(admin_id,
        f"➕ *{display_name}* присоединился к игре!\n"
        f"👥 Всего игроков: {new_players_count}/{MAX_PLAYERS}",
        parse_mode='Markdown'
    )

# Начало раунда
def start_round(game_id, admin_id):
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    # Проверяем права
    c.execute("SELECT admin_id, players_count, current_round, total_rounds FROM games WHERE game_id = ?", (game_id,))
    game = c.fetchone()

    if not game:
        bot.send_message(admin_id, "❗️ Игра не найдена")
        conn.close()
        return

    db_admin_id, players_count, current_round, total_rounds = game

    if db_admin_id != admin_id:
        bot.send_message(admin_id, "❗️ Только создатель игры может начать раунд")
        conn.close()
        return

    if players_count < MIN_PLAYERS:
        bot.send_message(admin_id, f"❗️ Недостаточно игроков! Нужно минимум {MIN_PLAYERS}, сейчас: {players_count}")
        conn.close()
        return

    # Обновляем раунд
    new_round = current_round + 1
    if new_round > total_rounds:
        end_game(game_id, admin_id)
        conn.close()
        return

    # Выбираем дело
    case = random.choice(CASES)

    c.execute("UPDATE games SET current_round = ?, status = 'playing', current_case = ? WHERE game_id = ?",
              (new_round, case, game_id))

    # Получаем игроков
    c.execute("SELECT player_id, user_id, display_name FROM players WHERE game_id = ?", (game_id,))
    players = c.fetchall()

    # Раздаём роли (всегда одинаковый набор для 10 игроков)
    available_roles = ['judge', 'prosecutor', 'witness', 'lawyer', 'accused', 'journalist']
    jury_count = max(0, len(players) - len(available_roles))
    available_roles.extend(['jury'] * jury_count)

    random.shuffle(available_roles)

    # Сохраняем раунд
    c.execute("INSERT INTO rounds (game_id, round_number, case_text) VALUES (?, ?, ?)",
              (game_id, new_round, case))

    # Раздаём карточки
    roles_assignment = []
    for i, (player_id, user_id, display_name) in enumerate(players):
        role = available_roles[i]
        c.execute("UPDATE players SET current_role = ? WHERE player_id = ?", (role, player_id))

        roles_assignment.append(f"{ROLES[role]}: {display_name}")

        # Отправляем карточки
        try:
            send_role_card(user_id, role, case, new_round, total_rounds)
        except Exception as e:
            print(f"Ошибка отправки карточки {display_name}: {e}")

    conn.commit()

    # Сброс голосов
    if game_id in active_games:
        active_games[game_id]['votes'] = {'guilty': 0, 'innocent': 0}
        active_games[game_id]['status'] = 'playing'

    conn.close()

    # Уведомляем админа
    markup = types.InlineKeyboardMarkup()
    btn_end = types.InlineKeyboardButton("⏱ Закончить раунд", callback_data=f"end_round_{game_id}")
    markup.add(btn_end)

    time_info = f"{ROUND_TIME//60} мин" if ROUND_TIME >= 60 else f"{ROUND_TIME} сек"

    bot.send_message(admin_id,
        f"🎬 *РАУНД {new_round}/{total_rounds} НАЧАЛСЯ!*\n\n"
        f"⚖️ *ДЕЛО:*\n_{case}_\n\n"
        f"*РОЛИ:*\n" + "\n".join(roles_assignment) + "\n\n"
        f"⏰ Рекомендованное время: {time_info}\n\n"
        f"Карточки отправлены всем игрокам.\n"
        f"Когда закончите обсуждение - нажмите кнопку ниже.",
        parse_mode='Markdown',
        reply_markup=markup
    )

    # Уведомляем всех игроков о начале
    for player_id, user_id, display_name in players:
        if user_id != admin_id:
            try:
                bot.send_message(user_id,
                    f"🎬 *РАУНД {new_round} НАЧАЛСЯ!*\n\n"
                    f"Карточка выше 👆\nНачинайте игру!",
                    parse_mode='Markdown'
                )
            except:
                pass

# Отправка карточки роли
def send_role_card(user_id, role, case, round_num, total_rounds):
    if role == 'judge':
        effect = random.choice(SPECIAL_EFFECTS)
        text = (
            f"🎬 *РАУНД {round_num}/{total_rounds}*\n\n"
            f"🤵 *ВЫ - СУДЬЯ!*\n\n"
            f"⚖️ *ДЕЛО:*\n_{case}_\n\n"
            f"🎭 *СПЕЦЭФФЕКТ (используйте в любой момент):* {effect}\n"
            f"💡 Ваша задача: вести процесс и объявить вердикт!"
        )

    elif role == 'prosecutor':
        character = random.choice(CHARACTERS)
        words = random.sample(WORDS, min(2, len(WORDS)))
        goal = random.choice(SECRET_GOALS)
        text = (
            f"🎬 *РАУНД {round_num}/{total_rounds}*\n\n"
            f"👨‍⚖️ *ВЫ - ПРОКУРОР!*\n\n"
            f"⚖️ *ДЕЛО:* _{case}_\n"
            f"🎭 *ВАШ ОБРАЗ:* {character}\n"
            f"📝 *ВАШИ СЛОВА:* {', '.join(words)}\n"
            f"🎯 *СЕКРЕТНАЯ ЦЕЛЬ:* {goal}\n\n"
            f"💡 Стройте обвинение, используйте свои слова!"
        )

    elif role == 'witness':
        character = random.choice(CHARACTERS)
        word = random.choice(WORDS)
        text = (
            f"🎬 *РАУНД {round_num}/{total_rounds}*\n\n"
            f"🕵️ *ВЫ - СВИДЕТЕЛЬ ОБВИНЕНИЯ!*\n\n"
            f"⚖️ *ДЕЛО:* _{case}_\n"
            f"🎭 *ВАШ ОБРАЗ:* {character}\n"
            f"📝 *ВАШЕ СЛОВО:* {word}\n"
            f"🎯 *СЕКРЕТНАЯ ЦЕЛЬ:* {goal}\n\n"
            f"💡 Подтверждайте версию прокурора!"
        )

    elif role == 'lawyer':
        character = random.choice(CHARACTERS)
        words = random.sample(WORDS, min(2, len(WORDS)))
        goal = random.choice(SECRET_GOALS)
        text = (
            f"🎬 *РАУНД {round_num}/{total_rounds}*\n\n"
            f"👨‍💻 *ВЫ - АДВОКАТ!*\n\n"
            f"⚖️ *ДЕЛО:* _{case}_\n"
            f"🎭 *ВАШ ОБРАЗ:* {character}\n"
            f"📝 *ВАШИ СЛОВА:* {', '.join(words)}\n"
            f"🎯 *СЕКРЕТНАЯ ЦЕЛЬ:* {goal}\n\n"
            f"💡 Защищайте обвиняемого любой ценой!"
        )

    elif role == 'accused':
        character = random.choice(CHARACTERS)
        word = random.choice(WORDS)
        text = (
            f"🎬 *РАУНД {round_num}/{total_rounds}*\n\n"
            f"😎 *ВЫ - ОБВИНЯЕМЫЙ!*\n\n"
            f"⚖️ *ДЕЛО:* _{case}_\n"
            f"🎭 *ВАШ ОБРАЗ:* {character}\n"
            f"📝 *ВАШЕ СЛОВО:* {word}\n"
            f"🎯 *СЕКРЕТНАЯ ЦЕЛЬ:* {goal}\n\n"
            f"💡 Оправдывайтесь и используйте своё слово!"
        )

    elif role == 'journalist':
        chaos = random.choice(CHAOS_CARDS)
        text = (
            f"🎬 *РАУНД {round_num}/{total_rounds}*\n\n"
            f"📢 *ВЫ - ЖУРНАЛИСТ!*\n\n"
            f"⚖️ *ДЕЛО:* _{case}_\n\n"
            f"💥 *КАРТА БАБАХ!:* {chaos}\n"
            f"💡 Создавайте хаос в любой момент!"
        )

    else:  # jury
        text = (
            f"🎬 *РАУНД {round_num}/{total_rounds}*\n\n"
            f"👥 *ВЫ - ПРИСЯЖНЫЙ!*\n\n"
            f"⚖️ *ДЕЛО:* _{case}_\n\n"
            f"💡 Задавайте вопросы, наблюдайте и голосуйте!\n"
            f"В конце раунда вы решите: ВИНОВЕН или НЕТ?"
        )

    bot.send_message(user_id, text, parse_mode='Markdown')

# Завершение раунда и голосование
def end_round_voting(game_id, admin_id):
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT admin_id FROM games WHERE game_id = ?", (game_id,))
    game = c.fetchone()

    if not game or game[0] != admin_id:
        bot.send_message(admin_id, "❗️ Только создатель игры может завершить раунд")
        conn.close()
        return

    # Получаем всех игроков с их ролями
    c.execute("SELECT user_id, display_name, current_role FROM players WHERE game_id = ?", (game_id,))
    players = c.fetchall()
    conn.close()

    # Отправляем голосование только ПРИСЯЖНЫМ (не судье и не заинтересованным сторонам)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_guilty = types.InlineKeyboardButton("✅ ВИНОВЕН", callback_data=f"vote_guilty_{game_id}")
    btn_innocent = types.InlineKeyboardButton("❌ НЕ ВИНОВЕН", callback_data=f"vote_innocent_{game_id}")
    markup.add(btn_guilty, btn_innocent)

    voting_players = []
    for user_id, display_name, role in players:
        # Голосуют только присяжные (не судья, не прокурор, не адвокат, не обвиняемый, не свидетель)
        if role == 'jury':
            voting_players.append(display_name)
            try:
                bot.send_message(user_id,
                    "⏰ *ВРЕМЯ ГОЛОСОВАНИЯ!*\n\n"
                    "👥 Вы - присяжный. Принимайте решение:",
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            except:
                pass
        else:
            # Остальным просто уведомление
            try:
                bot.send_message(user_id,
                    "⏰ *ГОЛОСОВАНИЕ НАЧАЛОСЬ!*\n\n"
                    "Присяжные принимают решение...",
                    parse_mode='Markdown'
                )
            except:
                pass

    # Админу отдельная кнопка для показа результатов
    admin_markup = types.InlineKeyboardMarkup()
    btn_show = types.InlineKeyboardButton("📊 Показать результаты", callback_data=f"next_round_{game_id}")
    admin_markup.add(btn_show)

    voters_list = ", ".join(voting_players) if voting_players else "нет присяжных"

    bot.send_message(admin_id,
        f"✅ Голосование отправлено присяжным!\n\n"
        f"👥 Голосуют: {voters_list}\n\n"
        f"Когда все проголосуют - нажмите кнопку:",
        parse_mode='Markdown',
        reply_markup=admin_markup
    )

# Обработка голосования
def handle_vote(call):
    game_id = int(call.data.split("_")[2])
    vote_type = call.data.split("_")[1]

    if game_id not in active_games:
        active_games[game_id] = {'votes': {'guilty': 0, 'innocent': 0}}

    active_games[game_id]['votes'][vote_type] += 1

    bot.send_message(call.from_user.id, f"✅ Ваш голос '{vote_type.upper()}' учтён!")

# Показ результатов и переход к следующему раунду
def show_results_and_next(game_id, admin_id):
    if game_id not in active_games:
        active_games[game_id] = {'votes': {'guilty': 0, 'innocent': 0}}

    votes = active_games[game_id]['votes']
    guilty_votes = votes.get('guilty', 0)
    innocent_votes = votes.get('innocent', 0)

    if guilty_votes > innocent_votes:
        verdict = "ВИНОВЕН"
        winner_team = "prosecution"
        emoji = "⚖️"
    elif innocent_votes > guilty_votes:
        verdict = "НЕ ВИНОВЕН"
        winner_team = "defense"
        emoji = "🎉"
    else:
        verdict = "НИЧЬЯ"
        winner_team = "tie"
        emoji = "🤝"

    # Обновляем очки
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    if winner_team == "prosecution":
        c.execute("""UPDATE players SET score = score + 2
                     WHERE game_id = ? AND current_role IN ('prosecutor', 'witness', 'judge')""",
                  (game_id,))
    elif winner_team == "defense":
        c.execute("""UPDATE players SET score = score + 2
                     WHERE game_id = ? AND current_role IN ('lawyer', 'accused')""",
                  (game_id,))

    c.execute("""UPDATE rounds SET winner_team = ?
                 WHERE game_id = ? AND round_number = (SELECT current_round FROM games WHERE game_id = ?)""",
              (winner_team, game_id, game_id))

    # Получаем всех игроков и текущий раунд
    c.execute("SELECT user_id FROM players WHERE game_id = ?", (game_id,))
    players = c.fetchall()

    c.execute("SELECT current_round, total_rounds FROM games WHERE game_id = ?", (game_id,))
    current_round, total_rounds = c.fetchone()

    conn.commit()
    conn.close()

    # Сброс голосов
    active_games[game_id]['votes'] = {'guilty': 0, 'innocent': 0}

    # Уведомляем всех о результате
    result_text = (
        f"{emoji} *ВЕРДИКТ: {verdict}!*\n\n"
        f"📊 Голосов 'Виновен': {guilty_votes}\n"
        f"📊 Голосов 'Не виновен': {innocent_votes}\n\n"
    )

    if winner_team != "tie":
        result_text += f"✨ Команда {'обвинения' if winner_team == 'prosecution' else 'защиты'} получает +2 очка!"
    else:
        result_text += "🤝 Ничья! Очки не начисляются."

    for user_id_tuple in players:
        try:
            bot.send_message(user_id_tuple[0], result_text, parse_mode='Markdown')
        except:
            pass

    # Админу кнопки управления
    markup = types.InlineKeyboardMarkup(row_width=1)

    if current_round < total_rounds:
        btn_next = types.InlineKeyboardButton(f"➡️ Начать раунд {current_round + 1}", callback_data=f"start_round_{game_id}")
        btn_end = types.InlineKeyboardButton("🏁 Завершить игру", callback_data=f"end_game_{game_id}")
        markup.add(btn_next, btn_end)

        bot.send_message(admin_id,
            result_text + "\n\n"
            f"📊 Раунд {current_round}/{total_rounds} завершён.\n"
            "Выберите действие:",
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        end_game(game_id, admin_id)

# Завершение игры
def end_game(game_id, admin_id):
    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT display_name, score, current_role FROM players WHERE game_id = ? ORDER BY score DESC", (game_id,))
    players = c.fetchall()

    c.execute("SELECT user_id FROM players WHERE game_id = ?", (game_id,))
    all_players = c.fetchall()

    c.execute("UPDATE games SET status = 'finished' WHERE game_id = ?", (game_id,))
    conn.commit()
    conn.close()

    if players:
        leaderboard = "\n".join([f"{i+1}. {p[0]}: {p[1]} 🏆" for i, p in enumerate(players)])
        winner = players[0]

        result_text = (
            f"🏆 *ИГРА ЗАВЕРШЕНА!*\n\n"
            f"*ИТОГОВАЯ ТАБЛИЦА:*\n{leaderboard}\n\n"
            f"🎉 *ПОБЕДИТЕЛЬ: {winner[0]}* с {winner[1]} очками!\n\n"
            f"Спасибо за игру!"
        )

        # Отправляем всем игрокам
        for user_id_tuple in all_players:
            try:
                bot.send_message(user_id_tuple[0], result_text, parse_mode='Markdown')
            except:
                pass

    # Удаляем из памяти
    if game_id in active_games:
        del active_games[game_id]

# Команда /cancel
@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT game_id FROM games WHERE admin_id = ? AND status != 'finished'", (user_id,))
    game = c.fetchone()

    if not game:
        bot.send_message(user_id, "❗️ У вас нет активных игр")
        conn.close()
        return

    game_id = game[0]

    # Получаем всех игроков для уведомления
    c.execute("SELECT user_id FROM players WHERE game_id = ?", (game_id,))
    players = c.fetchall()

    c.execute("DELETE FROM players WHERE game_id = ?", (game_id,))
    c.execute("DELETE FROM rounds WHERE game_id = ?", (game_id,))
    c.execute("DELETE FROM games WHERE game_id = ?", (game_id,))
    conn.commit()
    conn.close()

    # Уведомляем всех игроков
    for user_id_tuple in players:
        try:
            bot.send_message(user_id_tuple[0], "❌ Игра отменена администратором.")
        except:
            pass

    if game_id in active_games:
        del active_games[game_id]

    bot.send_message(user_id, "✅ Игра отменена.")

# Команда /score (оставлена как команда, но больше нет кнопки в меню)
@bot.message_handler(commands=['score'])
def score_command(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    # Ищем игру, в которой участвует пользователь
    c.execute("""SELECT g.game_id FROM games g
                 JOIN players p ON g.game_id = p.game_id
                 WHERE p.user_id = ? AND g.status != 'finished'""", (user_id,))
    game = c.fetchone()

    if not game:
        bot.send_message(user_id, "❗️ Вы не участвуете в активной игре")
        conn.close()
        return

    game_id = game[0]

    c.execute("SELECT username, score, current_role FROM players WHERE game_id = ? ORDER BY score DESC", (game_id,))
    players = c.fetchall()
    conn.close()

    if players:
        scores = "\n".join([f"{i+1}. {p[0]} ({ROLES.get(p[2], 'Нет роли')}): {p[1]} 🏆"
                           for i, p in enumerate(players)])
        bot.send_message(user_id, f"📊 *ТЕКУЩИЙ СЧЁТ:*\n\n{scores}", parse_mode='Markdown')

# Команда /status
@bot.message_handler(commands=['status'])
def status_command(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('judgment_day.db', check_same_thread=False)
    c = conn.cursor()

    # Ищем игру
    c.execute("""SELECT g.game_id, g.players_count, g.current_round, g.total_rounds,
                 g.status, g.current_case, g.game_code
                 FROM games g
                 JOIN players p ON g.game_id = p.game_id
                 WHERE p.user_id = ? AND g.status != 'finished'""", (user_id,))
    game = c.fetchone()

    if not game:
        bot.send_message(user_id, "❗️ Вы не участвуете в активной игре")
        conn.close()
        return

    game_id, players_count, current_round, total_rounds, status, current_case, game_code = game

    c.execute("SELECT display_name, current_role FROM players WHERE game_id = ?", (game_id,))
    players = c.fetchall()
    conn.close()

    status_emoji = {"setup": "⏸ Ожидание", "playing": "▶️ Играем", "finished": "🏁 Завершена"}.get(status, "❓")

    players_list = "\n".join([f"• {p[0]} - {ROLES.get(p[1], 'Ожидание')}" for p in players]) if players else "Нет игроков"

    case_info = f"\n\n⚖️ *Текущее дело:*\n_{current_case}_" if current_case else ""

    bot.send_message(user_id,
        f"📊 *СТАТУС ИГРЫ*\n\n"
        f"🔑 Код: `{game_code}`\n"
        f"{status_emoji}\n"
        f"👥 Игроков: {players_count}\n"
        f"🔄 Раунд: {current_round}/{total_rounds}\n"
        f"{case_info}\n\n"
        f"*ИГРОКИ:*\n{players_list}",
        parse_mode='Markdown'
    )

# Показ правил
def show_rules(message):
    bot.send_message(message.chat.id,
        "📖 *ПРАВИЛА ИГРЫ*\n\n"
        "1️⃣ Каждый раунд игроки получают роли\n"
        "2️⃣ Судья читает дело, прокурор обвиняет, адвокат защищает\n"
        "3️⃣ Используйте свои секретные слова и цели\n"
        "4️⃣ Журналист создаёт хаос картами БАБАХ!\n"
        "5️⃣ Присяжные голосуют: виновен или нет?\n"
        "6️⃣ Команда-победитель получает очки!\n\n"
        "🎯 Цель: набрать максимум очков за все раунды",
        parse_mode='Markdown'
    )

# Показ ролей
def show_roles(message):
    bot.send_message(message.chat.id,
        "🎭 *РОЛИ В ИГРЕ*\n\n"
        "🤵 *СУДЬЯ* - ведёт процесс, объявляет вердикт\n"
        "👨‍⚖️ *ПРОКУРОР* - обвиняет (2 слова + секретная цель)\n"
        "🕵️ *СВИДЕТЕЛЬ* - подтверждает обвинение (1 слово)\n"
        "👨‍💻 *АДВОКАТ* - защищает (2 слова + секретная цель)\n"
        "😎 *ОБВИНЯЕМЫЙ* - оправдывается (1 слово)\n"
        "📢 *ЖУРНАЛИСТ* - создаёт хаос (2 карты БАБАХ!)\n"
        "👥 *ПРИСЯЖНЫЕ* - голосуют и задают вопросы",
        parse_mode='Markdown'
    )

# Показ помощи (функция оставлена; кнопки убраны из меню)
def show_help(message):
    mode_info = "\n\n🔧 *РЕЖИМ ОТЛАДКИ*\nМин. игроков: 2" if DEBUG_MODE else ""

    bot.send_message(message.chat.id,
        "🎮 *КОМАНДЫ БОТА*\n\n"
        "*Для всех:*\n"
        "/start - Главное меню\n"
        "/score - Показать текущий счёт\n"
        "/status - Информация о текущей игре\n"
        "/help - Эта справка\n\n"
        "*Для администратора:*\n"
        "/cancel - Отменить игру\n\n"
        "📖 Используйте кнопки для управления!" + mode_info,
        parse_mode='Markdown'
    )

# Обработка callback для показа результатов
@bot.callback_query_handler(func=lambda call: call.data.startswith("next_round_"))
def next_round_callback(call):
    bot.answer_callback_query(call.id)
    game_id = int(call.data.split("_")[2])
    show_results_and_next(game_id, call.from_user.id)

# Запуск бота
if __name__ == '__main__':
    print("=" * 50)
    print("🎮 Бот запущен!")
    print("=" * 50)

    if DEBUG_MODE:
        print("🔧 РЕЖИМ ОТЛАДКИ АКТИВЕН!")
        print(f"   • Минимум игроков: {MIN_PLAYERS}")
        print(f"   • Время раунда: {ROUND_TIME//60} мин")
        print(f"   • Время голосования: {VOTE_TIME//60} мин")
        print("-" * 50)

    print("⏳ Инициализация базы данных...")
    init_db()
    print("✅ База данных готова!")
    print("🚀 Бот работает... Нажмите Ctrl+C для остановки")
    print("\n📱 Как использовать:")
    print("   1. Админ создаёт игру и получает код")
    print("   2. Игроки вводят код и присоединяются")
    print("   3. Админ начинает раунды")
    print("   4. Все получают карточки в личку")
    print("=" * 50)

    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")
