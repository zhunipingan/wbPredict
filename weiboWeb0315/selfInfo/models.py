# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse

class Observer(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    my_id = models.IntegerField(blank=True, null=True)
    add_time = models.DateTimeField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    crawl_count = models.BigIntegerField(blank=True, null=True)
    is_exist = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'observer'

    def get_absolute_url(self):
        return reverse('self:deleteObserver', kwargs={'id': self.id})

    def get_absolute_url2(self):
        return reverse('index:userInfo', kwargs={'userId': self.user_id})


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    register_time = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user'