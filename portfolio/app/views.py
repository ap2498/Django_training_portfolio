from django.shortcuts import render, redirect
from django.http import JsonResponse
from app.models import Project, ProjectImages, Category
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def entry(request):
    return render(request,'entry.html')
@login_required(login_url='/load_login/')
def load_create_project(request):
    return render(request,'create.html')
def load_home_page(request):
    return render(request,'home.html')
def load_single_project_page(request):
    return render(request,'single_project.html')
def load_category_page(request):
    return render(request,'category.html')
def load_login(request):
    return render(request,"login.html")
def create_project(request):
    if request.method=="POST":
        title=request.POST.get('title')
        desc=request.POST.get("description")
        url=request.POST.get("url")
        technology=request.POST.get('technology')
        client=request.POST.get("client")
        cover=request.FILES.get('cover')
        category=request.FILES.get('category')
        project=Project.objects.create(title=title,description=desc,technology=technology,url=url,client=client,cover=cover,category=category)

        project_images=request.FILES.getlist('images')

        for img in project_images:
            ProjectImages.objects.create(picture=img,project=project)
        return JsonResponse({
            'status':200,
            'message':"Project Created Succesfully"
        })
    
@csrf_exempt
def create_category(request):
    if request.method=="POST":
        name=request.POST.get('name')
        value=request.POST.get('value')

        Category.objects.create(name=name,value=value)
        return JsonResponse({
            'status':200,
            'message':"Category Created Succesfully"
        })
    

def fetch_all_projects(request):
    projects=Project.objects.prefetch_related('images').all()
    data_list=[]
    for project in projects:
        data_list.append({
            'id':project.id,
            'title':project.title,
            'description':project.description,
            'url':project.url,
            'technology':project.technology,
            'cover':project.cover.url,
            'client':project.client,
            # 'category':{
            #     'id':project.category.id,
            #     'category':project.category.name,
            #     'value':project.category.value
            # },
            'images':[{
                'id':p.id,
                'url':p.picture.url,
                'project':p.project.id
            }
            for p in project.images.all()
            ]
        })
    return JsonResponse({
        'message':"Data fetched succesfully",
        'status':200,
        'data':data_list
    })


def fetch_single_project(request,pk):
    project=Project.objects.get(id=pk)
    data=[]
    data.append({
        'id':project.id,
        'title':project.title,
        'description':project.description,
        'url':project.url,
        'technology':project.technology,
        'cover':project.cover.url,
        # 'category':{
        #     'id':project.category.id,
        #     'category':project.category.name,
        #     'project':project.category.value
        # },
        'images':[{
            'id':p.id,
            'url':p.picture.url,
            'project':p.project.id
        }for p in project.images.all()]
    })

    return JsonResponse({
        'message':"Data fetched succesfully",
        'status':200,
        'data':data
    })

def fetch_by_category(request,id):
    projects=Project.objects.filter(category=id)
    data=[]
    for project in projects:
        data.append({
        'id':project.id,
        'title':project.title,
        'description':project.description,
        'url':project.url,
        'technology':project.technology,
        'cover':project.cover.url,
        # 'category':{
        #     'id':project.category.id,
        #     'category':project.category.name,
        #     'project':project.category.value
        # },
        'images':[{
            'id':p.id,
            'url':p.picture.url,
            'project':p.project.id
        }for p in project.images.all()]
    })
        
    return JsonResponse({
        'message':"Data fetched succesfully",
        'status':200,
        'data':data
    })


def get_categories(request):
    categories=Category.objects.all()
    category_list=[]
    for cat in categories:
        category_list.append({
            'id':cat.id,
            'value':cat.value,
            'category':cat.name
        })
    
    return JsonResponse({
        'status':200,
        'message':"Data fetched succesfully",
        'data':category_list
    })

@csrf_exempt
def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'status':200,
                'message':'Username already exists'
            })
        user=User.objects.create_user(username=username,password=password)
        return JsonResponse({
            'message':"Signup succesful",
            'status':200
        })
    
@csrf_exempt
def login_user(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user= authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return JsonResponse({
                'status':200,
                'message':"Logged in Succesfully"
            })
        else:
            return JsonResponse({
                'message':"USer not found",
                'status':400
            })
@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({
            'status': 200,
            'message': 'Logged out successfully',
            'data': []
        })

    return JsonResponse({
        'status': 405,
        'message': 'Method not allowed. Use POST instead.',
        'data': []
    }, status=405)