#telnet
import getpass
import sys
import telnetlib
import time
from switch import Switch
from c_2950_48_G import C_2950_48_G
from c_2950_24t import C_2950_24T
from snr_2962_24_T import SNR_2962_24T
from snr_s2960_48g import SNR_S2960_48G
from snr_s2960_24g import SNR_S2960_24G
from orion_a26 import ORION_A26
if __name__=="__main__":
    #---Cisco 2950-48G-----
    #cisco_2950_48_g=C_2950_48_G('10.3.3.0','python_config','10.3.0.1',2401,2448)
    #cisco_2950_48_g.config_switch('10.3.3.0','python_config','10.3.0.1',2401,2448)
    #---Cisco 2950-24T-----
    #cisco_2950_24_t=C_2950_24T('10.3.9.0','C_2950_24_T','10.3.0.1',2701,2724,2801,2824)
    #cisco_2950_24_t.config_switch()
    #---SNR S2962-24T-----------
    #snr_2962_24t=SNR_2962_24T('10.2.2.1','vost1-S2962-24T','10.2.0.1',201,250,timezone="5",ip_snmp_server='192.168.0.1')
    #snr_2962_24t.config_switch()
    #---SNR S2960-48G-----------
    #snr_s2960_48g=SNR_S2960_48G('10.3.6.0','practic_switch','10.3.0.1',2401,2448,2501,2548,timezone="5",ip_snmp_server='192.168.0.1')
    #snr_s2960_48g.config_switch()
    #---SNR S2960-24G-----------
    #snr_s2960_24g=SNR_S2960_24G('10.2.8.1','avt4-snr-s2960-24g','10.3.0.1',801,824,timezone="5",ip_snmp_server='192.168.0.1')
    #snr_s2960_24g.config_switch()
    #---Orion Alpha A26---------
    #orion_a26=ORION_A26('10.3.6.0','A26','10.3.0.1',2701,2724,timezone="5",ip_snmp_server='192.168.0.1')
    #orion_a26.config_switch()
    
