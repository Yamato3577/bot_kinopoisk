from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    search_movie_param = State()
    search_movie_name = State()
    name = State()
    info_movie = State()
    my_movies = State()
    title_type = State()
    category = State()
    genres_name = State()
    year = State()
    rating_kp = State()
    temp = State()
    favourites = State()
    random_movie = State()
    start = State()
    help = State()
