from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=122)
    msg = models.TextField()
    date = models.DateField()

    def __str__(self) -> str:
        return self.name