from loguru import logger

from typing import Dict
from playhouse.shortcuts import model_to_dict

from database.models import *


def add_favourites(id_person: int, nickname_person: str, movie: Dict) -> None:
    """
    Добавляет фильм в БД (Избранное)
    :param id_person: int
    :param nickname_person: str
    :param movie: Dict
    информация о фильме
    :return: None
    """
    try:
        with db.atomic():
            Favourite(
                id_user=id_person,
                nickname=nickname_person,
                name=movie['name'],
                id_movie=movie['id'],
                rating=movie['rating'],
                description=movie['description'],
                year=movie['year'],
                poster=movie['poster'],
                genres=movie['genres'],
                countries=movie['countries'],
                type_movie=movie['type'],
                trailer=movie['trailer']
            ).save()
        logger.info('Пользователь {}, добавил фильма в БД', id_person)
    except Exception as error:
        logger.error('Пользователь {}, ошибка {} при добавлении фильма в БД', id_person, error)


def checking_movie(id_person: int, id_movie: int = None) -> bool:
    """
    Если передается параметр id_movie, проверяет наличие данного фильма в БД (Избранное) у  пользователя.
    Если предается только id_person, проверяет  наличие записей о фильмах в БД (Избранное) у пользователя.
    :param id_person: int
    :param id_movie: int = None
    :return: bool
    """
    try:
        with db.atomic():
            if id_movie:
                Favourite.get(Favourite.id_user == id_person and Favourite.id_movie == id_movie)
            else:
                Favourite.get(Favourite.id_user == id_person)
            return True
    except Exception:
        return False


def checking_number_movies(id_person: int) -> bool:
    """
    Проверяет чтобы количество записей в БД у пользователя было не больше допустимого (5).
    :param id_person: int
    :return: bool
    """
    try:
        if checking_movie(id_person):
            with db.atomic():
                results = (Favourite.select(Favourite.id_user, fn.Count(Favourite.id_user).alias('count'))
                           .where(Favourite.id_user == id_person)
                           .group_by(Favourite.id_user))
            for result in results:
                if result.count < 5:
                    return True
                else:
                    return False
        else:
            return True
    except Exception as error:
        logger.error('Пользователь {}, ошибка {} при проверке количества фильмов в БД', id_person, error)


def get_favourites(id_person: int) -> Dict:
    """
    Извлекает данные пользователя из БД (Избранное).
    :param id_person: int
    :return: Dict
    """
    logger.info('Пользователь {}, запросил избранное ', id_person)
    result = []
    with db.atomic():
        movies = Favourite.select().where(Favourite.id_user == id_person)
        for movie in movies:
            movie = model_to_dict(movie)
            movie['type'] = movie['type_movie']
            movie['countries'] = [{'name': movie['countries']}]
            movie['poster'] = {'previewUrl': movie['poster']}
            movie['rating'] = {'kp': movie['rating']}
            movie['genres'] = [{'name': movie['genres']}]
            movie['id'] = movie['id_movie']
            movie['videos'] = {'trailers': [{'url': movie['trailer']}]}
            result.append(movie)
    return {'docs': result}


def delete_favorite(id_person: int, id_movie: int) -> None:
    """
    Удаляет фильм из БД (Избранное).
    :param id_person: int
    :param id_movie: int
    :return: None
    """
    logger.info('Пользователь {}, удалил фильм с id {} из избранного БД', id_person, id_movie)
    try:
        with db.atomic():
            movie = Favourite.get(Favourite.id_user == id_person and Favourite.id_movie == id_movie)
            movie.delete_instance()
    except Exception as error:
        logger.error('Пользователь {}, ошибка {} при удалении фильма в БД', id_person, error)
