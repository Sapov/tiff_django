from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Design, Comment
from .forms import ProjectForm, DesignForm, CommentForm

@login_required
def project_list(request):
    projects = Project.objects.filter(client=request.user) | Project.objects.filter(designer=request.user)
    return render(request, 'designs/project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    designs = project.designs.all()
    return render(request, 'designs/project_detail.html', {'project': project, 'designs': designs})

@login_required
def upload_design(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = DesignForm(request.POST, request.FILES)
        if form.is_valid():
            design = form.save(commit=False)
            design.project = project
            design.uploaded_by = request.user
            design.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = DesignForm()
    return render(request, 'designs/upload_design.html', {'form': form, 'project': project})

@login_required
def add_comment(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.design = design
            comment.author = request.user
            comment.save()
            return redirect('project_detail', project_id=design.project.id)
    else:
        form = CommentForm()
    return render(request, 'designs/add_comment.html', {'form': form, 'design': design})