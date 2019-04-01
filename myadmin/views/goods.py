from django.shortcuts import render
from django.http import HttpResponse
#
from common.models import Goods,Types
from datetime import datetime
from PIL import Image
import time,os
# Create your views here.
def index(request):
    '''浏览信息'''
    list = Goods.objects.all()
    #遍历商品信息，并获取对应的商品类别名称，以typename名封装
    for vo in list:
        ty = Types.objects.get(id=vo.typeid)
        vo.typename = ty.name
    context = {"goodslist":list}
    return render(request,"myadmin/goods/index.html",context)

def add(request):
    '''加载添加页面'''
    #获取商品类别信息
    tlist = Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
    for ob in tlist:
        ob.pname = '. . .'*(ob.path.count(',')-1)
    context={'typelist':tlist}
    return render(request,"myadmin/goods/add.html",context)

def insert(request):
    '''执行添加'''
    try:
        #保存商品信息
        ob = Goods()
        if request.POST['goods']=='':
            context={"info":"商品名称不能为空！"}
            request.session['url']='myadmin_goods_add'
            request.session['data']=-1
            return render(request,"myadmin/info.html",context)
        else:
            ob.goods = request.POST['goods']

        if request.POST['price']=='':
            context={"info":"单价不能为空！"}
            request.session['url']='myadmin_goods_add'
            request.session['data']=-1
            return render(request,"myadmin/info.html",context)  
        else:       
            ob.price = request.POST['price']

        if request.POST['store']=='':
            request.session['url']='myadmin_goods_add'
            request.session['data']=-1
            context={"info":"库存量不能为空！"}
            return render(request,"myadmin/info.html",context)  
        else: 
            ob.store = request.POST['store']

        #图片的上传处理
        myfile = request.FILES.get("pic",None)
        if not myfile:
            context={"info":"没有上传文件!"}
            request.session['url']='myadmin_goods_add'
            request.session['data']=-1
            return render(request,"myadmin/info.html",context)
        filename = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/goods/"+filename,"wb+")
        #分块写入文件 
        for chunk in myfile.chunks():       
            destination.write(chunk)  
        destination.close()

        #图片的缩放
        im = Image.open("./static/goods/"+filename)
        #缩放到375*375(缩放后的宽高比例不变):
        im.thumbnail((375, 375)) 
        im.save("./static/goods/"+filename,None)
        
        im = Image.open("./static/goods/"+filename)
        #缩放到220*220(缩放后的宽高比例不变):
        im.thumbnail((220,220)) 
        im.save("./static/goods/m_"+filename,None)

        im = Image.open("./static/goods/"+filename)
        #缩放到75*75(缩放后的宽高比例不变):
        im.thumbnail((75, 75)) 
        im.save("./static/goods/s_"+filename,None)

        #保存商品信息
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.content = request.POST['content']
        ob.picname = filename
        ob.state = 0
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功！"}
        request.session['url']='myadmin_goods_index'
        request.session['data']=-1
    except Exception as err:
        print(err)
        request.session['url']='myadmin_goods_add'
        request.session['data']=-1
        context={"info":"添加失败！"}
    return render(request,"myadmin/info.html",context)

def delete(request,gid):
    '''删除信息'''
    try:
        ob = Goods.objects.get(id=gid)
        os.remove("./static/goods/"+ob.picname)
        os.remove("./static/goods/s_"+ob.picname)
        os.remove("./static/goods/m_"+ob.picname)
        ob.delete()
        context={"info":"删除成功！"}
        request.session['url']='myadmin_goods_index'
        request.session['data']=-1
    except Exception as err:
        print(err)
        request.session['url']='myadmin_goods_index'
        request.session['data']=-1
        context={"info":"删除失败！"}
    return render(request,"myadmin/info.html",context)


def edit(request,gid):
    '''加载编辑信息页面'''
    try:
        g = Goods.objects.get(id=gid)
        tlist = Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
        for ob in tlist:
            ob.pname = '. . .'*(ob.path.count(',')-1)
        context={"good":g,'typelist':tlist}
        return render(request,"myadmin/goods/edit.html",context)
    except Exception as err:
        print(err)
        request.session['url']='myadmin_goods_edit'
        request.session['data']=gid
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

def update(request,gid):
    '''执行信息修改'''
    try:
        ob = Goods.objects.get(id=gid)
        '''执行其它信息修改'''
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.content = request.POST['content']
        ob.state = request.POST['state']
        if request.POST['goods']=='':
            context={"info":"商品名称不能为空！"}
            request.session['url']='myadmin_goods_edit'
            request.session['data']=gid
            return render(request,"myadmin/info.html",context)
        else:
            ob.goods = request.POST['goods']

        if request.POST['price']=='':
            context={"info":"单价不能为空！"}
            request.session['url']='myadmin_goods_edit'
            request.session['data']=gid
            return render(request,"myadmin/info.html",context)  
        else:       
            ob.price = request.POST['price']

        if request.POST['store']=='':
            context={"info":"库存量不能为空！"}
            request.session['url']='myadmin_goods_edit'
            request.session['data']=gid
            return render(request,"myadmin/info.html",context)  
        else: 
            ob.store = request.POST['store']

        '''执行新图片上传'''
        myfile=request.FILES.get("pic",None)
        if myfile:
            '''删除原图片'''
            os.remove("./static/goods/"+ob.picname)
            os.remove("./static/goods/s_"+ob.picname)
            os.remove("./static/goods/m_"+ob.picname)
            '''添加新图片'''
            filename = str(time.time())+"."+myfile.name.split('.').pop()
            destination = open("./static/goods/"+filename,"wb+")
            #分块写入文件 
            for chunk in myfile.chunks():       
                destination.write(chunk)  
            destination.close()

            #图片的缩放
            im = Image.open("./static/goods/"+filename)
            #缩放到375*375(缩放后的宽高比例不变):
            im.thumbnail((375, 375)) 
            im.save("./static/goods/"+filename,None)
            
            im = Image.open("./static/goods/"+filename)
            #缩放到220*220(缩放后的宽高比例不变):
            im.thumbnail((220,220)) 
            im.save("./static/goods/m_"+filename,None)

            im = Image.open("./static/goods/"+filename)
            #缩放到75*75(缩放后的宽高比例不变):
            im.thumbnail((75, 75)) 
            im.save("./static/goods/s_"+filename,None)

        ob.save()
        context={"info":"修改成功！"}
        request.session['url']='myadmin_goods_index'
        request.session['data']=-1
    except Exception as err:
        print(err)
        request.session['url']='myadmin_goods_edit'
        request.session['data']=gid
        context={"info":"修改失败！"}
    return render(request,"myadmin/info.html",context)