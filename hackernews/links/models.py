from django.db import models
from django.contrib.auth.models import User as AuthUser


class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(
        AuthUser, null=True, on_delete=models.CASCADE)


class Vote(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, related_name='votes',
                             on_delete=models.CASCADE)
