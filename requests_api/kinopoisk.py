from loguru import logger
import requests

from typing import Union, Dict, List

from config_data.config import RAPID_API_KEY


def get_movie(title_type: str = None,
              genre: str = None,
              year: str = None,
              rating_kp: str = None,
              name: str = None,
              id_movie: List[int] = None,
              limit: Union[str, int] = '5',
              page: Union[str, int] = '1'
              ) -> Union[None, Dict]:
    """
    Запрос фильмов из API.
    Поиск по названию фильма или другим параметрам.
    При поиске по названию не выдает трейлеры, поэтому формируется список id и делается повторный запрос.
    Подробная документация https://kinopoisk.dev/.
    :param title_type: str
    :param genre: str
    :param year: str
    :param rating_kp: str
    :param name: str
    :param id_movie: List[int]
    :param limit: Union[str, int]
    :param page: Union[str, int]
    :return: Union[None, Dict]
    """
    value_param = {'type': title_type,
                   'genres.name': genre,
                   'year': year,
                   'rating.kp': rating_kp,
                   'query': name,
                   'id': id_movie,
                   'limit': limit,
                   'page': page,
                   'sortField': ['rating.kp'],
                   'sortType': ['-1'],
                   'name': '!null',
                   'poster.previewUrl': '!null',
                   'videos.trailers.type': 'TRAILER',
                   'selectFields': ['name', 'id', 'type', 'countries.name', 'year', 'poster.previewUrl',
                                    'rating.kp', 'description', 'genres', 'videos.trailers']
                   }
    try:
        if name:    # Поиск по названию фильма
            response = requests.get(url='https://api.kinopoisk.dev/v1.2/movie/search',
                                    params=value_param,
                                    timeout=10,
                                    headers={'X-API-KEY': RAPID_API_KEY})
            data = response.json()
            if len(data['docs']) == 0:
                raise ValueError(f'По запросу "{name}" ничего не найдено')
            else:
                films_id = []
                for film in data.get('docs'):
                    films_id.append(film.get('id'))
                return get_movie(id_movie=films_id)
        else:   # Поиск по параметрам
            response = requests.get(url='https://api.kinopoisk.dev/v1.3/movie',
                                    params=value_param,
                                    timeout=10,
                                    headers={'X-API-KEY': RAPID_API_KEY})
            data = response.json()
            if len(data['docs']) == 0:
                raise ValueError(f'По запросу c параметрами:'
                                 f' Тип - {value_param["type"]},'
                                 f' Год - {value_param["year"]},'
                                 f' Жанр - {value_param["genres.name"]},'
                                 f' Рейтинг - {value_param["rating.kp"]}.'
                                 f'  Ничего не найдено')
            else:
                return data
    except (requests.exceptions.RequestException, ValueError) as error:
        logger.error('Ошибка при запросе данных {}.', error)
        return None


def get_random_movie() -> Union[None, Dict]:
    """
    Запрос рандомного фильма из API.
    :return: Union[None, Dict]
    """
    try:
        response = requests.get(url='https://api.kinopoisk.dev/v1.3/movie/random',
                                timeout=10,
                                headers={'X-API-KEY': RAPID_API_KEY})
        return {'docs': [response.json()]}
    except requests.exceptions.RequestException as error:
        logger.error('Ошибка при запросе данных {}', error)
        return None
