from django.db import models

from django.db import models
from django.urls import reverse
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from usrhome.test import generate_order_id
import time


class Notice(models.Model):
    head = models.CharField(max_length=30)
    desc = models.CharField(max_length=300)
    viewed = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        Notice.objects.create(user=kwargs.get('instance'),
                              head="Welcome to the Family",
                              desc="Lets move forward")
        Rent.objects.create(user=kwargs.get('instance'),
                            head="Maintenance Fee",
                            desc="Monthly Fee",
                            amount="5250",)


class Rent(models.Model):
    head = models.CharField(max_length=30)
    desc = models.CharField(max_length=300, null=True, blank=True)
    paid = models.BooleanField(default=False)
    amount = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(default=generate_order_id, editable=False, max_length=20)
    paid_on = models.DateTimeField(null=True,max_length=20)

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('usrhome:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
