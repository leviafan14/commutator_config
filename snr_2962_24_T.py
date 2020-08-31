import getpass
import sys
import telnetlib
import time
from switch import Switch
class SNR_2962_24T(Switch):
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
        tn.read_until(b"login:")
        tn.write(b'admin\n')
        tn.read_until(b"Password:")
        tn.write(b'admin\n')
        tn.write(b'conf t\n')
        #Настройка имени узла
        time.sleep(1)
        tn.write(b'hostname '+self.hostname.encode('ascii')+b'\n') #Настройка имени узла
        #------------------------------------
        #Настройка sntp и snmp
        time.sleep(1)
        tn.write(b'sntp server '+self.ip_snmp_server.encode('ascii')+b'\n')
        time.sleep(2)
        tn.write(b'snmp-server enable\n')
        time.sleep(2)
        tn.write(b'snmp-server securityip disable\n')
        time.sleep(2)
        tn.write(b'snmp-server community ro public\n')
        #-------------------------------------------------
        time.sleep(2)
        tn.write(b'clock timezone Yekaterinburg add '+self.timezone.encode('ascii')+b'\n')#Настройка времени
        time.sleep(2)
        tn.write(b'ip default-gateway '+self.ip_def_gateway.encode('ascii')+b'\n') #Настройка основного шлюза
        #----------------------------------
        time.sleep(1)
        #Отключение vlan 1
        tn.write(b'interface vlan 1\n')
        tn.write(b'no ip address\n')
        tn.write(b'shutdown\n')
        tn.write(b'exit\n')
        #------------------------------------------------
        #Настройка описаний 10, 11 vlan
        time.sleep(1)
        tn.write(b'interface vlan 10\n')
        tn.write(b'description manage\n')
        tn.write(b'exit\n')
        tn.write(b'interface vlan 11\n')
        tn.write(b'description trash\n')
        tn.write(b'exit\n')
        #-----------------------------------------------
        time.sleep(1)
        #Настройка loopback-detection interval
        tn.write(b'loopback-detection interval-time 10 3\n')
        time.sleep(1)
        tn.write(b'loopback-detection control-recovery timeout 60\n')
        time.sleep(1)
        #----------------------------------------------------
        #Настройка всех eth портов кроме 24 на абонентский доступ
        tn.write(b'interface ethernet1/0/1-24\n')
        tn.write(b'switchport mode access\n')
        time.sleep(3)
        tn.write(b'loopback-detection specified-vlan 1-4094\n')
        time.sleep(72)
        tn.write(b'loopback-detection control shutdown\n')
        tn.write(b'exit\n')
        #-------------------------------------------------
        #Настройка eth портов на vlan
        i=1
        numb_eth_port=1
        while i<=23:
            tn.write(b'interface ethernet1/0/'+str(numb_eth_port).encode('ascii')+b'\n')         
            tn.write(b'switchport access vlan '+str(self.vlan_first).encode('ascii')+b'\n')
            time.sleep(1)
            numb_eth_port+=1
            self.vlan_first+=1
            i+=1
        tn.write(b'exit\n')
        #------------------------------------------------
        #Настройка trunk портов
        print("Настрйока trunk портов")
        tn.write(b'interface ethernet1/0/25-28\n')
        tn.write(b'switchport mode trunk\n')
        print("Настрйока trunk vlan на портах")
        time.sleep(1)
        if (trunk_vlan!='none'):
            print(trunk_vlan)
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
        tn.write(b'speed-duplex force1g-full\n')
        tn.write(b'description rezerv\n')
        tn.write(b'exit\n')
        tn.write(b'interface ethernet1/0/28\n')
        tn.write(b'description uplink\n')
        tn.write(b'exit\n')
        time.sleep(1)
        #-----------------------------------------
        #Сохранение конфигурации и вывод новых настроек
        tn.write(b'exit\n')
        time.sleep(1)
        tn.write(b'wri\n')
        tn.read_until(b"Confirm to overwrite current startup-config configuration [Y/N]:")
        tn.write(b'y\n')
        tn.write(b'show run\n')
        time.sleep(2)
        all_result = tn.read_very_eager().decode('utf-8')
        time.sleep(5)
        print(all_result)
        tn.close()
