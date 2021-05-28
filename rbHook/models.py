from django.db import models

class incoming(models.Model):

    update_id = models.IntegerField(unique=True)
    message = models.TextField(max_length=4096)

    def __str__(self):
        return f'{self.update_id}'