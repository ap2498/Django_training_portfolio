from django.shortcuts import render, redirect
from django.http import JsonResponse
from app.models import Project, ProjectImages, Category

# Create your views here.
def entry(request):
    return render(request,'entry.html')

def load_create_project(request):
    return render(request,'create.html')
def load_home_page(request):
    return render(request,'home.html')

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