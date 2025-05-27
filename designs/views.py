from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from designs.forms import CommentForm
from designs.models import OrderDesign


class DesignLIst(ListView):
    model = OrderDesign


class DesignDetailView(DetailView):
    model = OrderDesign
    template_name = 'designs/design_detail.html'
    context_object_name = 'designers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()

        context['comments'] = self.object.comments.all()
        return context

    def get_queryset(self):
        print(self.request.user)
        queryset = OrderDesign.objects.filter(user=self.request.user)
        print(queryset)
        return queryset


@login_required
def add_comment(request, id):
    design = get_object_or_404(OrderDesign, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.designs = design  # Используем designs вместо design (как в модели)
            comment.author = request.user
            comment.save()
            return redirect('designs:design_detail', pk=design.id)  # Добавляем id для редиректа
        else:
            # Если форма невалидна, можно вернуть пользователя на страницу с ошибками
            return render(request, 'designs/design_detail.html', {
                'designers': design,
                'comment_form': form,
                'comments': design.comments.all()
            })

    # Если метод не POST, перенаправляем на детальную страницу
    return redirect('designs:design_detail', pk=design.id)


class DesignCreateView(CreateView):
    model = OrderDesign
    fields = ['title', 'complexity', 'interest', 'interest', 'width', 'length', 'description', 'images']
