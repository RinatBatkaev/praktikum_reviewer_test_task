# Импортировать библиотеку целиком не обязательно,
# можно воспользоваться конструкцией from .. import ..
import datetime as dt


# Желательно написать комментарии к каждому классу,
# оформленный в виде Docstrings. Более детальную информацию можно получить
# в соглашении Docstring Conventions (PEP 257).
# https://www.python.org/dev/peps/pep-0257
class Record:
    # Параметр date в конструкторе принимает пустую строку,
    # если данные не будут переданы. Лучше избегать такого рода поведения.
    # В таких случаях можно использовать None.
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Будет лучше, если не разбивать if на 3 строки,
        # чтобы сохранить читабельность кода.
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


# Docstrings
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Имена переменных чувствительны к регистру.
        # Переменная record и Record - это разные переменные.
        # Практически во всем файле используется стиль snake_case,
        # лучше исправить имя данной переменной в пользу общего стиля.
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Конструкцию можно упростить сокращенным оператором присвоения.
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Операции сравнения в Python имеют так же, как и в математике
            # общепринятую интерпретацию: a < b < c.
            # Поэтому данное условие можно упростить.
            # https://docs.python.org/3/reference/expressions.html#comparisons
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


# Docstrings
class CaloriesCalculator(Calculator):
    # Docstrings также относится и к функциям.
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Данное вычисление повторяется в калькуляторе денег,
        # можно вынести в родительский класс.
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Длинные строки можно описывать через тройные кавычки,
            # тем самым не переживать о переносе строки.
            # В данном случае можно как раз избежать применения бэкслеша.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # В данном случае else не обязательный оператор.
        # Можно упростить конструкцию в пользу читабельности.
        else:
            # Скобки лучше использовать при уточнении приоритета.
            return('Хватит есть!')


# Docstrings
class CashCalculator(Calculator):
    # 1) Лучше выводить константы для всех курсов.
    # 2) При вычислениях float может давать погрешность,
    # поэтому для хранения денег лучше использовать тип decimal.
    # Более подробно об этом можно прочитать по следующим ссылкам:
    # https://docs.python.org/3/library/decimal.html
    # https://otus.ru/nest/post/510/
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        # Данное вычисление повторяется в калькуляторе калорий,
        # можно вынести в родительский класс.
        cash_remained = self.limit - self.get_today_stats()
        # Для избежания роста конструкции if else
        # можно подумать в сторону словаря, где ключами могут быть курсы валют.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Данное утверждение скорее всего не будет иметь эффект.
            cash_remained == 1.00
            currency_type = 'руб'
        # Не будет лишним добавить пустые строки, для более удобного чтения кода
        if cash_remained > 0:
            # Про тройные кавычки и скобки выше упоминалось,
            # здесь это тоже можно исправить.
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Замечание про тройные кавычки в силе.
            # Также для форматирования текста лучше использовать f-строки,
            # а вычисления производить заранее.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Данная конструкция не будет иметь смысла.
    # Функция и так наследуется от родителя.
    def get_week_stats(self):
        super().get_week_stats()
