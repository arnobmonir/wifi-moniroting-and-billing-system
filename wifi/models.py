from django.db import models
from wifi.API_Helper import RouterApiHelper


class Device(models.Model):
    name = models.CharField('Name', max_length=50)
    vendor = models.CharField(default=None, blank=True, max_length=50)
    model = models.CharField(default=None, blank=True, max_length=50)
    serial_number = models.CharField(default=None, blank=True, max_length=50)
    hostname = models.CharField(default=None, blank=True, max_length=50)
    MAC = models.CharField('MAC',
                           default=None, blank=True, max_length=50)
    static_ip = models.CharField('IP', max_length=50)
    port = models.CharField('Router Port  ', default=8728, max_length=15)
    login_user = models.CharField('Router Admin Name  ', max_length=100)
    login_password = models.CharField('Password  ', max_length=50)
    location = models.TextField(default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    name = models.CharField(
        'Client Name', max_length=100, default='No Name', blank=True)
    phone = models.CharField(max_length=100, default='No Phone', blank=True)
    MAC = models.CharField('MAC',
                           default=None, blank=True, max_length=50)
    current_ip = models.CharField(
        'IP', default=None, blank=True, max_length=50)
    age = models.CharField(
        'AGE', default=None, blank=True, max_length=50)
    current_interface = models.CharField(
        'Interface', default=None, blank=True, max_length=50)
    data_usage = models.CharField(
        default=0, blank=True, max_length=50)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
