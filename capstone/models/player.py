from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



class Player(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    zip_code = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(5)])



    class Meta:
        verbose_name = ("player")
        verbose_name_plural = ("players")


