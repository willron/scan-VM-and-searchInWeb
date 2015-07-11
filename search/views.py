#coding:utf-8
from django.shortcuts import render
import re
import commands
from models import VMServer
# from django.shortcuts import render_to_response
from django.http import HttpResponse
from .forms import AddForm, VMNameForm, SearchForm
from FindVM import *
import json

def api_search_ip(request):
    if request.GET:
        KVMIP = request.GET['kvmip']
        VMNAME = request.GET['vmname']
        DBINFO = VMServer.objects.filter(hostserverip__icontains = KVMIP , name__icontains = VMNAME)
        SEACHLIST = []
        for i in DBINFO:
            SEACHLIST.append(i.ip)
        return HttpResponse(SEACHLIST)
    else:
        return HttpResponse('Need kvmip and vmname')

def search_from_db(request):
    if request.method == 'POST':# 当提交表单时
        form = SearchForm(request.POST) # form 包含提交的数据
        if form.is_valid():# 如果提交的数据合法
            INFO = form.cleaned_data['INFO']
            MATCHKVM = re.compile(r'^192\.168\.0\.((1[5-7])$|2$|3$)')
            MATCHMAC = re.compile(r'^([a-fA-F0-9]{2}:){5,5}[a-fA-F0-9]{2}$')
            MATCHIP = re.compile(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$')
            MATCHOS = re.compile(r'(^windows$)|(^linux$)',re.I)
            if MATCHKVM.match(INFO):
                MATCHINFO = VMServer.objects.filter(hostserverip__icontains = INFO)
            elif MATCHIP.match(INFO):
                MATCHINFO = VMServer.objects.filter(ip__contains = INFO.encode('utf-8'))
            elif MATCHMAC.match(INFO):
                MATCHINFO = VMServer.objects.filter(mac__icontains = INFO)
            elif MATCHOS.match(INFO):
                MATCHINFO = VMServer.objects.filter(os__icontains = INFO)
            else:
                MATCHINFO = VMServer.objects.filter(name__icontains = INFO)

            if MATCHINFO == None:
                return HttpResponse('Nothing!!')
            else:
                form2 = SearchForm()
                return render(request, 'search.html', {'form':form2,'FROMDB':MATCHINFO,'keyword':INFO})
    else:# 当正常访问时
        # RUNORNORUN = commands.getoutput('ps ax|grep checkallvm|grep -v grep')
        # FINDCHECKALLVM = RUNORNORUN.find('checkallvm.py')
        # if FINDCHECKALLVM == -1:
        #     commands.getstatusoutput('python ../manage.py rundirect ../checkallvm.py')
        # status, output = RunCheckAllVM()
        # print status, output
        form = SearchForm()
    return render(request, 'search.html', {'form':form})


# def vmnametoip(request):
#     if request.method == 'POST':# 当提交表单时
#         form = VMNameForm(request.POST) # form 包含提交的数据
#         if form.is_valid():# 如果提交的数据合法
#             VMName = form.cleaned_data['VMName']
#             SEAR = VMName2IP(VMName)
#             getMACandIPandOS = SEAR.GetIP()
#             if not getMACandIPandOS:
#                 return HttpResponse('Nothing!!')
#             else:
#                 form2 = VMNameForm()
#                 return render(request, 'vmnametoip.html', {'form':form2,'MACANDIPANDOS':getMACandIPandOS})
#     else:# 当正常访问时
#         #GETIP = None
#         form = VMNameForm()
#     return render(request, 'vmnametoip.html', {'form':form})
#
#
# def findvm(request):
#     if request.method == 'POST':# 当提交表单时
#         form = AddForm(request.POST) # form 包含提交的数据
#         if form.is_valid():# 如果提交的数据合法
#             IP = form.cleaned_data['IP']
#             RETMAC = getMacAddr(IP)
#             if RETMAC == 2:
#                 return HttpResponse('Can\'t ping %s' %IP)
#             else:
#                 (KVMIP, VMNAME) = FindVM(RETMAC)
#                 f = [KVMIP, VMNAME, IP.encode('utf-8')]
#                 #f = 'KVM宿主机IP:%s ，虚拟机名:%s ,虚拟机IP：%s' %(KVMIP, VMNAME, IP.encode('utf-8'))
#                 #return HttpResponse(f)
#                 form2 = AddForm()
#                 return render(request, 'index.html', {'form':form2,'msg':f})
#     else:# 当正常访问时
#         form = AddForm()
#     return render(request, 'index.html', {'form':form})
