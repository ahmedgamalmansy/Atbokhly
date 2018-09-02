from django.db import models

# Create your models here.
class Contact(models.Model):
    from_email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    state   = models.NullBooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'From '+self.from_email + ' about '+self.subject
