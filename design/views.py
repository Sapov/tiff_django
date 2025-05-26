from django.shortcuts import render
from django.views.generic import ListView, DetailView

from design.models import OrdDesign



class DesignDetailView(DetailView):
    model = OrdDesign
    template_name = 'design_detail.html'
    context_object_name = 'designers'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['comments'] = self.object.comments.all()
    #     return context

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     obj.views += 1
    #     obj.save()
    #     return obj


# Create your views here.
class DesignViewList(ListView):
    model = OrdDesign
    template_name = 'orddesign_list.html'
    context_object_name = 'designers'
    paginate_by = 10

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DesignDetailView(DetailView):
    model = OrdDesign
