from django.db import models


class Games(models.Model):
    name = models.CharField(max_length=200)
    instance = models.TextField(default="{}")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "games"


class Players(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "players"


class Questions(models.Model):
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    answer = models.CharField(max_length=20)

    class Meta:
        db_table = "questions"
