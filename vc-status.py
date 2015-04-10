#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import getpass

print "\n"
host_name = raw_input("Please enter an IP or Hostname of EX-Series:")
ssh_port = raw_input("Please enter SSH Port[22]:") or "22"
username = raw_input("Please enter your EX-Series Username:")
pw = getpass.getpass()


dev = Device(user=username, host=host_name, password=pw,port=ssh_port)
dev.open()

vc = dev.rpc.get_virtual_chassis_port_information()
stats = dev.rpc.get_virtual_chassis_port_statistics(extensive=True)

print "=================================================="
print ('{0:5} {1:>4} {2:>6} {3:>6} {4:>12} {5:>12}'.format('FPC', 'Port', 'Speed', 'State', 'Input', 'Output'))
print ('{0:5} {1:>4} {2:>6} {3:>6} {4:>12} {5:>12}'.format('', '', 'Gbps', '', 'Kbps', 'Kbps'))
#print ('{} {}'.format('            Gbps       Kbps', '        Kbps'))
print "=================================================="
for vc_fpcName in vc.getiterator('multi-routing-engine-item'):
    fpc = vc_fpcName.findtext('re-name')
    for ports in vc_fpcName.getiterator('port-information'):
        portName = ports.findtext('port-name')
        portSpeed = ports.findtext('port-speed')
        portState = ports.findtext('port-status')

        for stats_fpcName in stats.getiterator('multi-routing-engine-item'):
         stats_fpc = stats_fpcName.findtext('re-name')
         
         if stats_fpc  == fpc:
          for values in stats_fpcName.getiterator('statistics'):
            stats_portName = values.findtext('port-name')
            stats_portSpeed = int(portSpeed) / 1000
            stats_inputBps = float(values.findtext('input-bps'))
            stats_inputKps = stats_inputBps/1024
            stats_outputBps = float(values.findtext('output-bps'))
            stats_outputKps = stats_outputBps/1024
            
            if stats_portName == 'vcp-255/'+portName:                                                       
              print ('{0:5} {1:>4} {2:>6} {3:>6} {4:>12.2f} {5:>12.2f}'.format(fpc, portName, stats_portSpeed, portState, stats_inputKps, stats_outputKps))





print "=================================================="
dev.close()


