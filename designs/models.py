from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=100)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_projects')
    designer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='designer_projects')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Design(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='designs')
    image = models.ImageField(upload_to='images/design')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Design for {self.project.title}'

class Comment(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comments {self.author.user_name}'

