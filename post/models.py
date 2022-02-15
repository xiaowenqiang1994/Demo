from django.db import models
from user.models import User

# Create your models here.

class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=64)
    content = models.TextField()
    create = models.DateTimeField(auto_now_add=True)

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(id=self.uid)
            return self._auth




