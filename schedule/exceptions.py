class AddToDataBaseError(Exception):
    def __str__(self):
        return 'Ошибка записи в базу данных'
