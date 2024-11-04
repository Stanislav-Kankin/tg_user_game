from tortoise import fields
from tortoise.models import Model


class User(Model):
    """
    Модель пользователя для хранения информации о пользователях.
    """
    i_id = fields.BigIntField(pk=True)
    s_username = fields.CharField(max_length=50, null=True)
    i_games_played = fields.IntField(default=0)  # Количество сыгранных игр
    i_total_score = fields.IntField(default=0)   # Общее число очков победы
