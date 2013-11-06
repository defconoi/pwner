#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# author: @090h
from subprocess import Popen

class DHCPServer:
    dhcpd_cfg = """option domain-name-server %s;
default-lease-time 60;
max-lease-time 72;
ddns-update-style none;
authoritative;
log-facility local7;

subnet %s.0 netmask %s {
  range %s.100 %s.254;
  option routers %s;
  option domain-name-server %s;
}"""

    def __init__(self, ip="192.168.1.1", mask="255.255.255.0", config='/etc/dhcp/dhcpd.conf'):
        self.ip, self.mask, self.config = ip, mask, config

    def __str__(self):
        ip = self.ip
        sip = '.'.join(ip.split('.')[:3])
        return self.dhcpd_cfg % (ip, sip, self.mask, sip, sip, ip, ip)

    def run(self):
        f = open(self.config, 'w+')
        f.write(self.__str__())
        f.close()
        Popen(['killall', '-9', 'dhcpd'], stderr=None).wait()
        print("Staring DHCPD")
        Popen(['dhcpd', '-cf', self.config, 'at0']).wait()