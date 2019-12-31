from django.contrib import admin
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.html import format_html
from django.urls import path
from django.urls import reverse
from wifi.models import Device, Client
from wifi.API_Helper import RouterApiHelper
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.functional import cached_property
import socket


class Custom_device(admin.ModelAdmin):
    # change_list_template = "change_list.html"
    router_connection = False

    def update(self, request, device_id, *args, **kwargs):
        device = get_object_or_404(Device, pk=device_id)
        val = RouterApiHelper(device.static_ip, device.port,
                              device.login_user, device.login_password)
        dev = val.Connect()
        fact = dev.get_facts()
        device.hostname = fact['hostname']
        device.model = fact['model']
        device.serial_number = fact['serial_number']
        device.vendor = fact['vendor']
        if not device.location:
            device.location = dev.get_snmp_information()['location']
        device.save()
        dev.close()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def view(self, request, device_id, *args, **kwargs):
        device = get_object_or_404(Device, pk=device_id)
        val = RouterApiHelper(device.static_ip, device.port,
                              device.login_user, device.login_password)
        dev = val.Connect()
        arp_table = dev.get_arp_table()
        for arpc in arp_table:
            count = Client.objects.filter(MAC=arpc['mac']).count()
            if count > 0:
                clnt = Client.objects.get(MAC=str(arpc['mac']))
                clnt.current_ip = arpc['ip']
                clnt.save()
            else:
                clnt = Client()
                clnt.name = self.host_name(arpc['ip'])
                clnt.MAC = arpc['mac']
                clnt.current_ip = arpc['ip']
                clnt.age = arpc['age']
                clnt.current_interface = arpc['interface']
                clnt.device_id = device_id
                clnt.save()

        context = dict(
            self.admin_site.each_context(request),
            something="test",
            arp_table=arp_table,
        )
        return redirect('/admin/wifi/client/')
        # return TemplateResponse(request, "admin/wifi/device/details.html", context)

    def host_name(self, ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return 'Not Found'

    @cached_property
    def crumbs(self):
        return super(Custom_device, self).crumbs + [
            (self.object.name, reverse(
                'details-view', kwargs={'pk': self.object.pk})),
        ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'sync/<int:device_id>',
                self.admin_site.admin_view(self.update),
                name='sync',
            ),
            path(
                'device-view/<int:device_id>',
                self.admin_site.admin_view(self.view),
                name='details-view',
            ),
        ]
        return custom_urls + urls

    def Util_Action(self, obj):
        if self.router_connection:
            return format_html(
                '<a class="button" href="{}">Sync</a>&nbsp;'
                '<a class="button" href="{}">Update</a>&nbsp;',
                reverse('admin:sync', args=[obj.id]),
                reverse('admin:details-view', args=[obj.id])
            )

    def is_online(self, obj):

        try:
            device = get_object_or_404(Device, pk=obj.id)
            val = RouterApiHelper(device.static_ip, device.port,
                                  device.login_user, device.login_password)
            dev = val.Connect()
            status = dev.is_alive()
            if status['is_alive']:
                self.router_connection = True
                return 'Online'
            else:
                self.router_connection = False
                return 'Offline'
        except:
            self.router_connection = False
            return 'Offline'

    list_display = ['name', 'static_ip', 'is_online',
                    'vendor', 'model', 'serial_number', 'hostname', 'location', 'Util_Action']
    list_filter = ('vendor', 'location', 'hostname')
    search_fields = ('static_ip', 'name', 'location')
    fieldsets = [
        ('Basic Information',               {'fields': [
         'name', 'static_ip', 'port', 'MAC', 'login_user', 'login_password', 'location']}),
        ('Router Factory Information', {
         'fields': ['vendor', 'model', 'serial_number', 'hostname']}),
    ]


admin.site.register(Device, Custom_device)


class Custom_Client(admin.ModelAdmin):
    list_display = ['device_name', 'name', 'accepted', 'MAC',
                    'current_ip', 'age', 'current_interface', 'data_usage']
    list_filter = ('device_id', 'current_interface', 'accepted')
    search_fields = ('MAC', 'current_ip', 'name', 'current_interface')
    fieldsets = [
        ('Basic Information',               {'fields': [
         'device', 'name', 'phone', 'MAC', 'age', 'current_ip', 'current_interface', 'accepted', 'data_usage']}),
    ]

    def active(self, request, queryset):
        rows_updated = queryset.update(accepted=True)
        if rows_updated == 1:
            message_bit = "1 client was"
        else:
            message_bit = "%s clients were" % rows_updated
        self.message_user(
            request, "%s successfully marked as accepted." % message_bit)
    active.short_description = "Mark selected clients as active"
    actions = [active]

    def device_name(self, obj):
        return obj.device.name+'('+obj.device.static_ip+')'


admin.site.register(Client, Custom_Client)
admin.site._wrapped
