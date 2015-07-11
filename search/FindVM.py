#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
by:willron
'''
__author__ = '郑绪鹏'

import os
import sys
import commands
import re
#此处需用到nmap工具，所以需要root权限
#def getMacAddrWithNMAP(IPADDR):
#    os.environ['HOSTIP'] = str(IPADDR)
#    return commands.getoutput('nmap -p 80 $HOSTIP | grep -oE "([A-F0-9]{2}:){5}[A-F0-9]{2}"')

#写得很累的类在此脚本里用不上
#class SSHandCMD(object):
#    def __init__(self,IP,PORT='22',USERNAME='root',CMD='uname'):
#        self.IP = IP
#        self.PORT = PORT
#        self.CMD = CMD
#        self.USERNAME = USERNAME
#
#    def Cmd(self):
#        os.environ['SERVERIP'] = str(self.IP)
#        os.environ['SERVERPORT'] = str(self.PORT)
#        os.environ['SERVERUSERNAME'] = str(self.USERNAME)
#        os.environ['CMD'] = str(self.CMD)
#        (CMDSTATUS, CMDOUTPUT) = commands.getstatusoutput('ssh $SERVERUSERNAME@$SERVERIP -p $SERVERPORT $CMD')
#        self.CMDSTATUS = CMDSTATUS
#        self.CMDOUTPUT = CMDOUTPUT

def flatten(ll):
    if isinstance(ll, list):
        for i in ll:
            for element in flatten(i):
                yield element
    else:
        yield ll

class VMName2IP(object):
    #通过虚拟机名称查找IP

    def __init__(self,VMName):
        self.VMName = VMName

    def GetMac(self):
        CMD = 'ps aux | grep qemu-kvm | grep -i %s | grep -iEo "([a-f0-9]{2}:){5}[a-f0-9]{2}"' %self.VMName
        MACLIST = []
        for i in ['192.168.0.3','192.168.0.2','192.168.0.15','192.168.0.16','192.168.0.17']:
            os.environ['CMD'] = str(CMD)
            os.environ['SERVERIP'] = str(i)
            (FINDSTATUS, FINDOUTPUT) = commands.getstatusoutput('ssh root@$SERVERIP -p 59516 $CMD')
            if FINDOUTPUT: 
                MACLIST.append(re.split('\n',FINDOUTPUT))
        return list(flatten(MACLIST))

    def GetIP(self):
        commands.getstatusoutput('seq 255|xargs -I {} -P 255 ping -w 1 -c 1 192.168.0.{}')
        MACLIST = self.GetMac()
        MACandIPandOS = {}
        IPANDOS = []
        for EACHMAC in MACLIST:
            os.environ['EACHMAC'] = str(EACHMAC)
            (FINDLOCALSTATUS, FINDLOCALOUTPUT) = commands.getstatusoutput('arp -a | grep -i $EACHMAC | grep -Po "((192\.168|172\.([1][6-9]|[2]\d|3[01]))(\.([2][0-4]\d|[2][5][0-5]|[01]?\d?\d)){2}|10(\.([2][0-4]\d|[2][5][0-5]|[01]?\d?\d)){3})"')
            if FINDLOCALSTATUS == 0:
                os.environ['FOUNDIP'] = str(FINDLOCALOUTPUT)
                (CHECKOSSTATUS, CHECKOSOUTPUT) = commands.getstatusoutput('ping -c 1 -w 1 $FOUNDIP|grep -oE "ttl=[0-9]{2,3}"')
                OS = 'Windows'if CHECKOSOUTPUT == 'ttl=128' else 'Linux' if CHECKOSOUTPUT == 'ttl=64' else CHECKOSOUTPUT 
                IPANDOS = [FINDLOCALOUTPUT,OS]
                MACandIPandOS[EACHMAC] = IPANDOS
        return MACandIPandOS

#IP to MAC
def getMacAddr(IPADDR):
    os.environ['HOSTIP'] = str(IPADDR)
    (PINGSTATUS,PINGOUTPUT) = commands.getstatusoutput('ping -w 1 -c 1 $HOSTIP')
    if PINGSTATUS != 0:
        #print 'Can not ping %s' %IPADDR
        return 2
        #sys.exit(2)
    else:
        return commands.getoutput('arp -a|grep -E "\($HOSTIP\)"|grep -oiE "([a-f0-9]{2}:){5}[a-f0-9]{2}"')

#KVM服务器中查找MAC地址
def FindVM(MacAddr):
    CMD = 'ps aux | grep qemu-kvm | grep %s | grep -v grep ' %MacAddr
    for i in ['192.168.0.3','192.168.0.2','192.168.0.15','192.168.0.16','192.168.0.17']:
        os.environ['CMD'] = str(CMD)
        os.environ['SERVERIP'] = str(i)
        (FINDSTATUS, FINDOUTPUT) = commands.getstatusoutput('ssh root@$SERVERIP -p 59516 $CMD') 
        if FINDSTATUS == 0:
            VMPSTOLIST = FINDOUTPUT.split()
            for NUM,VAL in enumerate(VMPSTOLIST):
                if VAL == '-name':
                    VMNAME = VMPSTOLIST[NUM+1]
                    return i,VMNAME


#通过虚拟机名称查找IP
def VMName2MAC(VMName):
    CMD = 'ps aux | grep qemu-kvm | grep -i %s | grep -iEo "([a-f0-9]{2}:){5}[a-f0-9]{2}"' %VMName
    MACLIST = []
    for i in ['192.168.0.3','192.168.0.2','192.168.0.15','192.168.0.16','192.168.0.17']:
        os.environ['CMD'] = str(CMD)
        os.environ['SERVERIP'] = str(i)
        (FINDSTATUS, FINDOUTPUT) = commands.getstatusoutput('ssh root@$SERVERIP -p 59516 $CMD') 
        if FINDSTATUS == 0:
            MACLIST.append(FINDOUTPUT)
    return MACLIST

# def RunCheckAllVM():
#     RUNORNORUN = commands.getoutput('ps ax|grep checkallvm|grep -v grep')
#     FINDCHECKALLVM = RUNORNORUN.find('checkallvm.py')
#     if FINDCHECKALLVM == -1:
#         (RUNSTATUS, RUNOUTPUT) = commands.getstatusoutput('python /root/python/FindVM/manage.py rundirect /root/python/FindVM/checkallvm.py\&')
#         return RUNSTATUS, RUNOUTPUT

if __name__=='__main__':
    FindIP = sys.argv[1]
    RET = getMacAddr(FindIP)
    if RET == 2:
        print 'Can not ping %s' %FindIP
        sys.exit(2)
    else:
        (KVMSERVER, VMNAME) = FindVM(RET)
        print 'KVM Server IP:',KVMSERVER
        print 'VM Name:',VMNAME



