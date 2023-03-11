from datetime import date

def info(name: str, birthday: date) -> str:
    return f'У {name} день рождения: {birthday}'


print(info('BACR', date(1999, 1, 1)))
