from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm
from .models import *
from django.views.generic import ListView, DetailView, CreateView


class ListViewDesign(ListView):
    """Посмотреть все дизайны пользователя"""

    model = DesignOrder
    paginate_by = 5
    template_name = "list_design.html"
    login_url = "login"

    def get_queryset(self):
        queryset = DesignOrder.objects.filter(author=self.request.user).order_by("-id")
        return queryset



class CreteDesignOrder(CreateView):
    model = DesignOrder
    fields = ('title', 'content', 'category', 'images')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DesignDetailView(DetailView):
    model = DesignOrder
    template_name = 'design/design_detail.html'

@login_required
def add_comment(request, slug):
    article = get_object_or_404(DesignOrder, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('detail_design', slug=article.slug)
    return redirect('detail_design', slug=article.slug)




