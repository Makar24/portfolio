import requests
from colorama import Fore, Style

api_key = 'k_asb5ej6y'
base_url = 'https://imdb-api.com/ru/API/'


def main():
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'поиск фильмов')

    while True:
        print(Fore.BLUE + Style.NORMAL + '1:НАЙТИ ФИЛЬМ\n2: ОЖИДАЕМЫЕ ФИЛЬМЫ')
        action = input(Fore.YELLOW + 'ВЫБЕРИТЕ НЕОБХОДИМОЕ ДЕЙСТВИЕ: ')

        match action:
            case '1':  # if 1
                film = input('ВВЕДИТЕ НАЗВАНИЕ ФИЛЬМА: ')
                search_film(film)
            case '2':  # if 2
                get_commingsoon()

        if input(Fore.YELLOW + 'ВЫЙТИ? ').title() == 'ДА':
            break


def search_film(film):
    id = None
    r = requests.get(f'{base_url}SearchMovie/{api_key}/{film}')

    if r.status_code == 200:
        films = r.json()

        for i in range(len(films['results'])):
            title = films['results'][i]['title']
            description = films['results'][i]['description']
            print(Fore.RED + f'{i + 1}.{title}')
            print(Fore.YELLOW + description)
            print('__________')

    review = input(Fore.RED + 'ВВЕДИТЕ НОМЕР ФИЛЬМА ДЛЯ ВЫВОДА ОЦЕНКИ И РЕЦЕНЗИЙ: ')

    if review.isdigit():
        review = int(review)
        try:
            id = films['results'][review - 1]['id']
        except IndexError as err:
            print('ВЫ ВВЕЛИ НЕВЕРНЫЙ НОМЕР')

        if id:
            get_review(id)
    else:
            print('ВЫ НЕ ВВЕЛИ ЧИСЛО')
def get_review(id):
    r = requests.get(f'{base_url}Ratings/{api_key}/{id}')
    rate = r.json()
    r = requests.get(f'{base_url}Reviews/{api_key}/{id}')
    reviews = r.json()['items']
    print(Fore.BLUE + f"ОЦЕНКА ФИЛЬМА: imDB: {rate['imDB']}")
    print(Fore.YELLOW + 'РЕЦЕНЗИИ: ')
    for i in range(len(reviews)):
        print(Fore.YELLOW + f"ПОЛЬЗОВАТЕЛЬ{reviews[i]['username']}{reviews[i]['date']} написал")
        print(Fore.BLUE + reviews[i]['content'])
        print('_____________')
def get_commingsoon():
    r = requests.get(f'{base_url}CommingSoon/{api_key}')
    films = r.json()['items']
    for i in range(len(films)):
        title = films[i]['title']
        date_release = films[i]['releaseState']
        genre = films[i]['genres']
        print(Fore.YELLOW + f'НАЗВАНИЕ: {title}\n{Fore.BLUE}ДАТА ВЫХОДА: {date_release}\n ЖАНH{genre}')
        print('__________________________________')

if __name__ == '__main__':
    main()



