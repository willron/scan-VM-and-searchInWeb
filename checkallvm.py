#!/usr/bin/env python
#coding=utf-8
import time
from search.models import VMServer
from search.views import *

#VMServer.objects.create(name='test1',ip='192.168.0.255',mac='11:11:11:11:11:11',hostserverip='192.168.0.1',os='Windows')

#KVM主机列表
KVMSERVER = ['192.168.0.2','192.168.0.3','192.168.0.15','192.168.0.16','192.168.0.17']

#SSH端口
SSHPORT = '59516'
os.environ['SSHPORT'] = str(SSHPORT)

def getOSfromAllIP():
#ping整个192.168.0.0网段，建立arp表的同时，获取IP和通过ttl判断操作系统
    IPANDOS = {}
    (PINGSTATUS, PINGOUTPUT) = commands.getstatusoutput('seq 254|xargs -I {} -P 254 ping -w 1 -c 1 192.168.0.{}|grep ttl|tr -d ":"')
    for EACHLINE in PINGOUTPUT.split('\n'):
        EACH = EACHLINE.split()
        IPANDOS[EACH[3]] = 'Windows' if EACH[5] == 'ttl=128' else 'Linux' if EACH[5] == 'ttl=64' else 'Other'
    return IPANDOS

#搜索arp表找到IP，MAC联系
def getIPfromARP():
    MACANDIP = {}
    (ARPSTATUS, ARPOUTPUT) = commands.getstatusoutput('arp -n|grep -v Address')
    for EACHLINE in ARPOUTPUT.split('\n'):
        EACH = EACHLINE.split()
        MACANDIP[EACH[2]] = EACH[0]
    return MACANDIP

#通过发送ps指令到KVMSERVER，获取运行中的虚拟机列表和虚拟机网卡mac地址
def getNameMac():
    MACANDVMNAMEANDKVMIP = []
    for EACHSERVER in KVMSERVER:
        os.environ['EACHSERVER'] = str(EACHSERVER)
        (SSHSTATUS, SSHOUTPUT) = commands.getstatusoutput('ssh root@$EACHSERVER -p $SSHPORT ps aux | grep qemu-kvm')
        for EACHLINE in SSHOUTPUT.split('\n'):
            MACNUMINLIST = EACHLINE.find('mac=')
            EACHMAC = EACHLINE[MACNUMINLIST+4:MACNUMINLIST+21]
            VMPSTOLIST = EACHLINE.split()
            for NUM,VAL in enumerate(VMPSTOLIST):
                if VAL == '-name':
                    EACHVMNAME = VMPSTOLIST[NUM+1]
                    EACHVM = {}
                    EACHVM['VMNAME'] = EACHVMNAME
                    EACHVM['VMMAC'] = EACHMAC
                    EACHVM['KVMIP'] = EACHSERVER
                    MACANDVMNAMEANDKVMIP.append(EACHVM)
    return MACANDVMNAMEANDKVMIP


while True:
    ALLIPANDOS = getOSfromAllIP()
    ALLIPANDMAC = getIPfromARP()
    ALLVMNAMEANDVMMACANDKVMIP = getNameMac()
    #VMServer.objects.all().delete()
    for SETSTATUS in VMServer.objects.all():
        SETSTATUS.vmstatus = 'offline'
        SETSTATUS.save()
    for NUM,VAL in enumerate(ALLVMNAMEANDVMMACANDKVMIP):
        WILLCREATE_NAME = VAL['VMNAME']
        WILLCREATE_MAC = VAL['VMMAC']
        WILLCREATE_HOSTSERVERIP = VAL['KVMIP']
        WILLCREATE_VMIP = ALLIPANDMAC.get(WILLCREATE_MAC,'Unknow')
        WILLCREATE_OS = ALLIPANDOS.get(WILLCREATE_VMIP,'Unknow')
        WILLCREATE_VMSTATUS = 'online'
        #VMServer.objects.update_or_create(defaults='mac',name = WILLCREATE_NAME, mac = WILLCREATE_MAC, ip = WILLCREATE_VMIP, hostserverip = WILLCREATE_KVMIP, os = WILLCREATE_OS)
        VMServer.objects.update_or_create(mac = WILLCREATE_MAC, defaults = { 'name' : WILLCREATE_NAME, 'ip' : WILLCREATE_VMIP, 'hostserverip' : WILLCREATE_HOSTSERVERIP, 'os' : WILLCREATE_OS, 'vmstatus' : WILLCREATE_VMSTATUS })
    time.sleep(60)