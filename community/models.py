from django.db import models

class JoinUs(models.Model):
    email = models.EmailField(unique=True,error_messages ={"unique":"Person with this Email already exists."})
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
