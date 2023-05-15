import requests  # Импорт модуля requests для выполнения HTTP-запросов
from colorama import Fore, Style  # Импорт модуля colorama для цветного вывода

api_key = 'k_asb5ej6y'  # API-ключ для доступа к IMDb API
base_url = 'https://imdb-api.com/ru/API/'  # Базовый URL для API-запросов


# Основная функция программы
def main():
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'Поиск фильмов')  # Вывод заголовка программы

    while True:
        print(
            Fore.BLUE + Style.NORMAL + '1: Найти фильм\n2: Ожидаемые фильмы\n3: Популярные фильмы ')  # Вывод меню действий
        action = input(Fore.YELLOW + 'Выберите необходимое действие: ')  # Запрос выбранного действия

        # Проверка выбранного действия
        match action:
            case '1':
                film = input('Введите название фильма: ')  # Запрос названия фильма
                search_film(film)  # Вызов функции поиска фильма
            case '2':
                get_commingsoon()  # Вызов функции получения списка ожидаемых фильмов
            case '3':
                get_popular()
        # Проверка запроса на выход из программы
        if input(Fore.YELLOW + 'Выйти? ').title() == 'Да':
            break


# Функция поиска фильма
def search_film(film):
    id = None
    r = requests.get(f'{base_url}SearchMovie/{api_key}/{film}')  # Выполнение запроса на поиск фильма

    if r.status_code == 200:
        films = r.json()

        # Вывод результатов поиска
        for i in range(len(films['results'])):
            title = films["results"][i]["title"]
            description = films["results"][i]["description"]
            print(Fore.BLUE + f'{i + 1}.{title}')  # Вывод номера и названия фильма
            print(Fore.YELLOW + description)  # Вывод описания фильма
            print('_______________________')

    review = input(Fore.YELLOW + 'Введите номер фильма для вывода оценки и рецензий: ')

    if review.isdigit():
        review = int(review)
        try:
            id = films['results'][review - 1]['id']
        except IndexError as err:
            print('Вы ввели неверный номер')

        if id:
            get_review(id)
    else:
        print('Вы ввели не число')


# Функция получения оценки и рецензий фильма
def get_review(id):
    r = requests.get(f'{base_url}Ratings/{api_key}/{id}')  # Выполнение запроса на получение оценки фильма
    rate = r.json()
    r = requests.get(f'{base_url}Reviews/{api_key}/{id}')  # Выполнение запроса на получение рецензий фильма
    reviews = r.json()["items"]
    print(Fore.BLUE + f'Оценка фильма: imDb: {rate["imDb"]}')
    print(Fore.YELLOW + 'Рецензии: ')
    for i in range(len(reviews)):  # Вывод рецензий
        print(Fore.YELLOW + f'Пользователь {reviews[i]["username"]} {reviews[i]["date"]} написал:')
        print(Fore.BLUE + reviews[i]["content"])
        print('_______________________')


def get_commingsoon():  # Функция получения списка ожидаемых фильмов

    r = requests.get(f'{base_url}ComingSoon/{api_key}')
    films = r.json()["items"]
    for i in range(len(films)):  # Вывод информации о фильмах

        title = films[i]["title"]
        date_release = films[i]["releaseState"]
        genre = films[i]["genres"]
        print(Fore.YELLOW + f'Название: {title}\n{Fore.BLUE}Дата выхода: {date_release}\nЖанр: {genre}')
        print('_______________________')


def get_popular():
    r = requests.get(f'{base_url}MostPopularMovies/{api_key}')
    films = r.json()['items']
    for i in range(len(films)):
        title = films[i]['title']
        year = films[i]['year']
        print(f'{i}, Название: {title}\n Год выхода: {year} г.')
        print('_________________')


if __name__ == '__main__':
    main()
