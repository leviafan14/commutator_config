import getpass
import sys
import telnetlib
import time
from switch import Switch
class C_2950_24T(Switch):
    def __init__(self,host_ip,hostname,ip_def_gateway,vlan_first,vlan_end,transit_vlan="none",transit_vlan_end="none",
                 ip_snmp_server="192.168.0.1",timezone="5"):
        Switch.__init__(self,host_ip,hostname,ip_def_gateway,vlan_first,vlan_end,
                        transit_vlan,transit_vlan_end,ip_snmp_server,timezone)
    #Настройка коммутатора "из коробки" 
    def config_switch(self):
        trunk_vlan='none'
        if (self.transit_vlan!='none' or self.transit_vlan_end!='none'):
            transit_vlan_diapazone=str(self.transit_vlan)+'-'+str(self.transit_vlan_end)
            vlan_diapazone=str(self.vlan_first)+'-'+str(self.vlan_end)
            trunk_vlan=vlan_diapazone+','+transit_vlan_diapazone
        vlan_diapazone=str(self.vlan_first)+'-'+str(self.vlan_end)
        time.sleep(3)
        tn = telnetlib.Telnet(self.host_ip)
        tn.read_until(b"Username: ")
        tn.write(b'admin\n')
        tn.read_until(b"Password: ")
        tn.write(b'admin\n')
        tn.write(b'conf t\n')
        time.sleep(1)
        tn.write(b'vtp mode transparent\n') #Настройка vtp mode
        time.sleep(1)
        tn.write(b'hostname '+self.hostname.encode('ascii')+b'\n') #Настройка имени узла
        time.sleep(1)
        tn.write(b'no ip domain-lookup\n') #Отключение поиска по доменам в консоли
        time.sleep(1)
        tn.write(b'no cdp run\n') #Отключение протокола Cisco
        time.sleep(1)
        tn.write(b'snmp-server community public ro\n') #Настройка snmp
        time.sleep(1)
        tn.write(b'no spanning-tree vlan 1-4094\n') #Отключение просмотра по дереву vlan 1-4094
        time.sleep(1)
        tn.write(b'ip default-gateway '+self.ip_def_gateway.encode('ascii')+b'\n') #Настройка основного шлюза
        #-------------------------------------------
        #Настройка времени
        tn.write(b'clock timezone Yekaterinburg +'+self.timezone.encode('ascii')+b'\n')
        time.sleep(1)
        tn.write(b'ntp server '+self.ip_snmp_server.encode('ascii')+b'\n')
        #-----------------------------------------
        #Отключение vlan 1
        tn.write(b'interface vlan 1\n')
        time.sleep(1)
        tn.write(b'no ip address\n')
        time.sleep(1)
        tn.write(b'shutdown\n')
        time.sleep(1)
        tn.write(b'exit\n')
        #---------------------------
        #Настройка описаний vlan 10, 11
        tn.write(b'interface vlan 10\n')
        tn.write(b'description manage\n')
        tn.write(b'exit\n')
        time.sleep(1)
        tn.write(b'interface vlan 11\n')
        tn.write(b'description trash\n')
        tn.write(b'exit\n')
        #-----------------------------------------------
        #Настройка eth портов кроме 24 на абонентский доступ
        tn.write(b'interface range fastethernet 0/1 - 23\n')
        time.sleep(1)
        tn.write(b'switchport mode access\n')
        time.sleep(1)
        tn.write(b'spanning-tree portfast\n')
        time.sleep(1)
        tn.write(b'exit\n')
        #--------------------------------------------
        time.sleep(1)
        tn.write(b'interface FastEthernet 0/24\n') # Настройка fiber портов
        time.sleep(1)
        tn.write(b'switchport mode trunk\n')
        time.sleep(1)
        if (trunk_vlan!='none'):
            time.sleep(1)
            tn.write(b'switchport trunk allowed vlan 10,'+trunk_vlan.encode('ascii')+b'\n')
        else:
            pass
        if trunk_vlan=='none':
            time.sleep(1)
            tn.write(b'switchport trunk allowed vlan 10,'+vlan_diapazone.encode('ascii')+b'\n')
        else:
            pass
        time.sleep(1)
        tn.write(b'switchport trunk native vlan 11\n')
        time.sleep(1)
        tn.write(b'switchport nonegotiate\n')
        time.sleep(1)
        tn.write(b'description uplink\n')
        time.sleep(1)
        tn.write(b'exit\n')
        time.sleep(1)
        #------------------------------------------
        #Настройка eth портов на vlan
        i=1
        numb_eth_port=1
        while i<23:
            tn.write(b'interface fastethernet 0/'+str(numb_eth_port).encode('ascii')+b'\n')
            time.sleep(0.5)
            tn.write(b'switchport access vlan '+str(self.vlan_first).encode('ascii')+b'\n')
            tn.write(b'exit\n')
            time.sleep(1)
            numb_eth_port+=1
            self.vlan_first+=1
            i+=1
        #--------------------------------------------
        #Сохранение конфигруации и вывод ее на экран
        time.sleep(1)
        tn.write(b'exit\n')
        time.sleep(1)
        tn.write(b'wri\n')
        time.sleep(5)
        tn.write(b'show run\n')
        time.sleep(2)
        all_result = tn.read_very_eager().decode('utf-8')
        time.sleep(5)
        print(all_result)
        tn.close()
