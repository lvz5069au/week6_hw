from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import urllib
from django.db.models import Q
from common.models import Users
from django.core.paginator import Paginator
#
# Create your views here.
def index(request,pIndex):
    '''浏览信息'''
    list = Users.objects.all()
    p=Paginator(list,4)
    if pIndex == "":
        pIndex="1"
    list2 = p.page(pIndex)
    plist = p.page_range
    context = {"userslist":list2,"plist":plist,"pIndex":pIndex}
    return render(request,"myadmin/users/index.html",context)

def add(request):
    '''加载添加页面'''
    return render(request,"myadmin/users/add.html")

def insert(request):
    '''执行添加'''
    try:
        ob = Users()
        if request.POST['username']=='':
            context={"info":"账户名不能为空！"}
            request.session['url']='myadmin_users_add'
            request.session['data']=-1
            return render(request,"myadmin/info.html",context)
        else:
            ob.username = request.POST['username']
        ob.name = request.POST['name']
        if request.POST['password']=='':
            context={"info":"密码不能为空！"}
            request.session['url']='myadmin_users_add'
            request.session['data']=-1
            return render(request,"myadmin/info.html",context)
        else:
            ob.password = request.POST['password']
        if request.POST['repassword'] != request.POST['password']:
            context={"info":"两次输入的密码不相同！"}
            request.session['url']='myadmin_users_add'
            request.session['data']=-1
            return render(request,"myadmin/info.html",context)
        #获取密码并md5
        import hashlib
        m = hashlib.md5() 
        m.update(bytes(request.POST['password'],encoding="utf8"))
        ob.password = m.hexdigest()
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = 1
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功！"}
        request.session['url']='myadmin_users_index'
        request.session['data']=-1
    except Exception as err:
        print(err)
        request.session['url']='myadmin_users_add'
        request.session['data']=-1
        context={"info":"添加失败！"}
    return render(request,"myadmin/info.html",context)

def delete(request,uid):
    '''删除信息'''
    try:
        ob = Users.objects.get(id=uid)
        if ob.state==0:
            count = Users.objects.filter(state=0).count()
            if count==1:
                context={"info":"至少要保留一个管理员账户！"}
                request.session['url']='myadmin_users_index'
                request.session['data']=-1
                return render(request,"myadmin/info.html",context)
        ob.delete()
        context={"info":"删除成功！"}
        request.session['url']='myadmin_users_index'
        request.session['data']=-1
    except Exception as err:
        print(err)
        request.session['url']='myadmin_users_index'
        request.session['data']=-1
        context={"info":"删除失败！"}
    return render(request,"myadmin/info.html",context)


def edit(request,uid):
    '''加载编辑信息页面'''
    try:
        ob = Users.objects.get(id=uid)
        context={"user":ob}
        return render(request,"myadmin/users/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        request.session['url']='myadmin_users_edit'
        request.session['data']=uid
        return render(request,"myadmin/info.html",context)

def update(request,uid):
    '''执行编辑信息'''
    try:
        ob = Users.objects.get(id=uid)
        ob.name = request.POST['name']
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = request.POST['state']
        ob.save()
        context={"info":"修改成功！"}
        request.session['url']='myadmin_users_index'
        request.session['data']=-1
    except Exception as err:
        print(err)
        context={"info":"修改失败！"}
        request.session['url']='myadmin_users_edit'
        request.session['data']=uid
    return render(request,"myadmin/info.html",context)

def reset(request,uid):
    '''加载编辑信息页面'''
    try:
        ob = Users.objects.get(id=uid)
        context={"user":ob}
        return render(request,"myadmin/users/reset.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        request.session['url']='myadmin_users_reset'
        request.session['data']=uid
        return render(request,"myadmin/info.html",context)

def resetupdate(request,uid):
    '''执行密码重置'''
    try:
        ob = Users.objects.get(id=uid)
        if request.POST['password']=='':
            context={"info":"密码不能为空！"}
            request.session['url']='myadmin_users_add'
            request.session['data']=uid
            return render(request,"myadmin/info.html",context)
        else:
            ob.password = request.POST['password']
        if request.POST['repassword'] != request.POST['password']:
            context={"info":"两次输入的密码不相同！"}
            request.session['url']='myadmin_users_add'
            request.session['data']=uid
            return render(request,"myadmin/info.html",context)
        #获取密码并md5
        import hashlib
        m = hashlib.md5() 
        m.update(bytes(request.POST['password'],encoding="utf8"))
        ob.password = m.hexdigest()
        ob.save()
        context={"info":"密码修改成功！"}
        request.session['url']='myadmin_users_index'
        request.session['data']=-1
    except Exception as err:
        print(err)
        context={"info":"密码修改失败！"}
        request.session['url']='myadmin_users_reset'
        request.session['data']=uid
    return render(request,"myadmin/info.html",context)

def search(request,pIndex):
    '''执行搜索'''
    try:
        key=request.POST['key']
        if request.POST['key'] == '':
            if request.POST['sex'] == '-1':
                list = Users.objects.all()
            else:
                list = Users.objects.filter(Q(sex=int(request.POST['sex'])))
        else:
            if request.POST['sex'] == '-1':
                list = Users.objects.filter(Q(username__startswith=key) | Q(name__startswith=key))
            else:
                list = Users.objects.filter((Q(username__startswith=key) | Q(name__startswith=key)) & Q(sex=int(request.POST['sex'])))
        
        p=Paginator(list,4)
        if pIndex == "":
            pIndex="1"
        list2 = p.page(pIndex)
        plist = p.page_range
        context = {"userslist":list2,"plist":plist,"pIndex":pIndex}
        return render(request,"myadmin/users/search.html",context)
        
    except Exception as err:
        print(err)
        context={"info":"搜索失败！"}
        request.session['url']='myadmin_users_index'
        request.session['data']=-1
    return render(request,"myadmin/info.html",context)