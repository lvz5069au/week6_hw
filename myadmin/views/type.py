from django.shortcuts import render
from django.http import HttpResponse
#
from common.models import Types
# Create your views here.
def index(request):
    '''浏览信息'''
    list = Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
    #遍历查询结果，添加类别缩进效果属性
    for ob in list:
        ob.pname='. . . . '*(ob.path.count(',')-1)
    context = {"typeslist":list}
    return render(request,"myadmin/type/index.html",context)

def add(request,tid):
    '''加载添加页面'''
    #获取父类别信息
    if tid =='0':
        context={'pid':0,'path':'0,','name':'根类别'}
    else:
        ob = Types.objects.get(id=tid)
        context={'pid':ob.id,'path':ob.path+str(ob.id)+',','name':ob.name}
    return render(request,"myadmin/type/add.html",context)

def insert(request):
    '''执行添加'''
    try:
        ob = Types()
        if request.POST['name']=='':
            context={"info":"类别名称不能为空！"}
            request.session['url']='myadmin_type_add'
            request.session['data']=0
            return render(request,"myadmin/info.html",context)
        else:
            ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        ob.path = request.POST['path']
        ob.save()
        context={"info":"添加成功！"}
        request.session['url']='myadmin_type_index'
        request.session['data']=-1
    except Exception as err:
        print(err)
        context={"info":"添加失败！"}
        request.session['url']='myadmin_type_add'
        request.session['data']=0
    return render(request,"myadmin/info.html",context)

def delete(request,tid):
    '''删除信息'''
    try:
        ob = Types.objects.get(id=tid)
        ob.delete()
        request.session['url']='myadmin_type_index'
        request.session['data']=-1
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        request.session['url']='myadmin_type_index'
        request.session['data']=-1
        context={"info":"删除失败！"}
    return render(request,"myadmin/info.html",context)


def edit(request,tid):
    '''加载编辑信息页面'''
    try:
        ob = Types.objects.get(id=tid)
        list = Types.objects.all()
        context={"type":ob,"tlist":list}
        return render(request,"myadmin/type/edit.html",context)
    except Exception as err:
        print(err)
        request.session['url']='myadmin_type_edit'
        request.session['data']=tid
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

def update(request,tid):
    '''执行编辑信息'''
    try:
        ob = Types.objects.get(id=tid)
        if request.POST['name']=='':
            context={"info":"类别名称不能为空！"}
            request.session['url']='myadmin_type_edit'
            request.session['data']=tid
            return render(request,"myadmin/info.html",context)
        else:
            ob.name = request.POST['name']

        pob = Types.objects.get(name=request.POST['pname'])
        ob.pid = pob.id
        ob.path=pob.path+str(pob.id)+','
        ob.save()
        context={"info":"修改成功！"}
        request.session['url']='myadmin_type_index'
        request.session['data']=-1
    except Exception as err:
        print(err)
        context={"info":"修改失败！"}
        request.session['url']='myadmin_type_edit'
        request.session['data']=tid
    return render(request,"myadmin/info.html",context)
