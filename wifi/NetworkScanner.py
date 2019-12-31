#!/usr/bin/env python

import scapy.all as scapy
import argparse


class NetworkScanner:
    def __init__(self, ip):
        self.ip = ip

    def scan(self):
        ip = self.ip
        arp_request = scapy.ARP(pdst=ip)
        broadcust = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcust = broadcust / arp_request
        answer_list = scapy.srp(arp_request_broadcust,
                                timeout=3)[0]
        client_list = []
        for elements in answer_list:
            client_dict = {"ip": elements[1].psrc, "mac": elements[1].hwsrc}
            client_list.append(client_dict)
        return client_list

    def test(self):
        return 'test'
