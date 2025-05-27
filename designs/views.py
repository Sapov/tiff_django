from django.shortcuts import render
from django.views.generic import ListView, DetailView

from designs.models import OrderDesign


# Create your views here.
class DesignLIst(ListView):
    model = OrderDesign


class DesignDetailView(DetailView):
    model = OrderDesign
    template_name = 'designs/design_detail.html'
    context_object_name = 'designers'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context

    #
    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     obj.views += 1
    #     obj.save()
    #     return obj
    #
    def get_queryset(self):
        print(self.request.user)
        queryset = OrderDesign.objects.filter(user=self.request.user)
        print(queryset)
        return queryset
