from django.db import models

class incoming(models.Model):

    update_id = models.CharField(max_length=60)
    message = models.TextField(default='NA', editable=False)

    def __str__(self):
        return self.name