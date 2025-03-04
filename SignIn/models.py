from django.db import models


class UserSignIn(models.Model):
    user_id = models.BigIntegerField()
    point = models.BigIntegerField(default=0)
    last_signin = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user_id)


from django.db import models

# Create your models here.
