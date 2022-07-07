from django.db import models


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    creation = models.CharField(max_length=200)
    expiration = models.CharField(max_length=200)

    def __str__(self):
        return self.user_id + " " + self.username + " " + self.password

