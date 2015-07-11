#coding:utf-8
from django import forms

class VMNameForm(forms.Form):
    VMName = forms.CharField(label="请输入虚拟机名称")

 
class AddForm(forms.Form):
    IP = forms.CharField(label="请输入查询IP")

class SearchForm(forms.Form):
    INFO = forms.CharField(label="请输入查询字段")