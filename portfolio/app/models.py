from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField()
    value=models.CharField()
class Project(models.Model):
    title=models.CharField()
    description=models.TextField()
    technology=models.TextField()
    url=models.URLField()
    client=models.CharField()
    cover=models.ImageField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE, null=True)


class ProjectImages(models.Model):
    picture=models.ImageField()
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,related_name='images')