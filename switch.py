class Switch:
    def __init__(self,host_ip,hostname,ip_def_gateway,vlan_first,vlan_end,transit_vlan="none",transit_vlan_end="none",
                 ip_snmp_server="192.168.0.1",timezone="5"):
        self.host_ip=host_ip
        self.hostname=hostname
        self.ip_def_gateway=ip_def_gateway
        self.vlan_first=vlan_first
        self.vlan_end=vlan_end
        self.transit_vlan=transit_vlan
        self.transit_vlan_end=transit_vlan_end
        self.timezone=timezone
        self.ip_snmp_server=ip_snmp_server
    #Вывод атрибутов коммутатора
    def __str__(self):
        return '[host_ip: %s hostname: %s ip_def_gateway: %s vlan: %d - %d transit vlan: %s - %s timezone: %s]' % (self.host_ip, self.hostname, self.ip_def_gateway,self.vlan_first,self.vlan_end,self.transit_vlan,self.transit_vlan_end,self.timezone)
