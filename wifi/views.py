from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from wifi.API_Helper import RouterApiHelper
from django.contrib.auth.models import User
from .models import Device


def index(request):
    user = User.email
    contex = {
        'device': user
    }
    return render(request, 'wifi/index.html')


def RouterData(request):
    devices = Device.objects.all()
    # for device in devices:
    #     val = RouterApiHelper(device.static_ip, device.port,
    #                           device.login_user, device.login_password)
    #     dev = val.Connect()
    #     fact = dev.get_facts()
    #     device.hostname = fact['hostname']
    #     device.model = fact['model']
    #     device.serial_number = fact['serial_number']
    #     device.vendor = fact['vendor']
    #     device.save()
    #     dev.close()

    context = {
        'devices': devices
    }
    return render(request, 'wifi/index.html', context=context)


def router_data_update(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    val = RouterApiHelper(device.static_ip, device.port,
                          device.login_user, device.login_password)
    dev = val.Connect()
    fact = dev.get_facts()
    device.hostname = fact['hostname']
    device.model = fact['model']
    device.serial_number = fact['serial_number']
    device.vendor = fact['vendor']
    device.save()
    dev.close()
    return render(request, 'wifi/index.html')
