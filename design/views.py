from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from design.forms import CommentForm, AddDesignForm
from design.models import OrdDesign, Comment


class DesignDetailView(DetailView):
    model = OrdDesign
    template_name = 'design_detail.html'
    context_object_name = 'designers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj


# Create your views here.
class DesignViewList(ListView):
    model = OrdDesign
    template_name = 'orddesign_list.html'
    context_object_name = 'designers'
    paginate_by = 10

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DesignCreateView(CreateView):
    form_class = AddDesignForm
    model = OrdDesign
    template_name = 'design/add_design.html'



@login_required
def add_comment(request, slug):
    article = get_object_or_404(OrdDesign, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('design_detail', slug=article.slug)
    return redirect('design_detail', slug=article.slug)


def get_comment_in_order(request, slug):
    order = OrdDesign.objects.get(slug=slug)
    print(order)
    comments = Comment.objects.all()
    # items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе
    # current_order = Order.objects.get(pk=order_id)

    context = {
        "Orders": order,
        "comments": comments,
        # "items_in_order": items_in_order,
        # "current_order": current_order,
        # "order_id": order_id,
        # "order_data_pay": order.pay_link
    }
    return render(request, "design/orddesign_detail.html", context)
