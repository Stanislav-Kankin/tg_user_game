from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=50, null=True)
    games_played = fields.IntField(default=0)  # Количество сыгранных игр
    total_score = fields.IntField(default=0)   # Общее число очков победы
