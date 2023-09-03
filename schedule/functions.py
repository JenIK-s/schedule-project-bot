import json

from exceptions import AddToDataBaseError

week_days = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье'
]

schedule_path = 'DATABASES/schedule.json'
users_path = 'DATABASES/users.json'


def forming_string(week: str, group: str, day_of_the_week: int) -> str:
    """
    Формирование строки с расписанием

    :param week: Вид недели (Числитель / Знаменатель)
    :param group: Подгруппа (1 / 2)
    :param day_of_the_week: День недели
    :return: Сформированая строка расписания
    """
    global week_days

    with open(schedule_path, 'r') as f:
        schedule: dict = json.load(f)

    if day_of_the_week == 6:
        day_of_the_week: str = week_days[day_of_the_week]
        return f'{day_of_the_week} / {week}\n\n---------- Выходной ----------'
    day_of_the_week: str = week_days[day_of_the_week]
    day_from_the_schedule: dict = schedule\
        .get(week)\
        .get(group)\
        .get(day_of_the_week)
    result = f'{day_of_the_week} / {week}\n\n'
    for couple, subjects_data in day_from_the_schedule.items():
        if couple.split()[0] == '1':
            result += f'---------- {couple} ----------\n'
        else:
            result += f'\n---------- {couple} ----------\n'
        for subject_data, subject_value in subjects_data.items():
            if subject_value == '':
                result += 'Окно\n'
                break
            result += f'{subject_data}: {subject_value}\n'
    return result


def add_user_to_database(user_id: int, button_data: str):
    """
    Добавляется ID пользователя и его группу в базу данных

    :param user_id: ID пользователя
    :param button_data: Выбор подгруппы (1 / 2)
    :return: Запись в базу данных
    """
    users_id = []
    with open(users_path, 'r') as f:
        users = json.load(f)
    for user in users:
        users_id.append(user.get('ID'))
    if user_id not in users_id:
        with open(users_path, 'w') as f:
            if button_data == 'one':
                users.append(
                    {
                        'ID': user_id,
                        'Group': '1 подгруппа',
                    }
                )
                json.dump(users, f, indent=4)
            elif button_data == 'two':
                users.append(
                    {
                        'ID': user_id,
                        'Group': '2 подгруппа',
                    }
                )
                json.dump(users, f, indent=4)
    else:
        raise AddToDataBaseError


def get_group(user_id: int) -> str:
    """
    Получает группу пользователя по его ID

    :param user_id: ID пользователя
    :return: Group пользователя
    """
    with open(users_path, 'r') as f:
        users = json.load(f)
        for user in users:
            if user.get('ID') == user_id:
                return user.get('Group')
