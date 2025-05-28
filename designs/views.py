from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView

from designs.forms import CommentForm
from designs.models import OrderDesign, Comments

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import OrderDesign

from django.http import JsonResponse
from django.core import serializers

class DesignList(LoginRequiredMixin, ListView):
    model = OrderDesign
    template_name = 'designs/design_list.html'  # Укажите ваш шаблон
    context_object_name = 'designs'  # Имя переменной в шаблоне

    def get_queryset(self):
        """
        Для обычных пользователей - только их заказы,
        для дизайнеров - все заказы
        """
        if self.request.user.role == 'DESIGNER':
            return OrderDesign.objects.all()
        return OrderDesign.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем информацию о роли пользователя в контекст
        context['is_designer'] = self.request.user.role == 'DESIGNER'
        return context


class DesignDetailView(DetailView):
    model = OrderDesign
    template_name = 'designs/design_detail.html'
    context_object_name = 'design'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context

    def get_queryset(self):
        # Базовый queryset - все объекты (ограничим доступ в dispatch)
        return OrderDesign.objects.all()

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект до проверки прав
        self.object = self.get_object()

        # Проверяем права доступа
        if not self.has_permission():
            raise PermissionDenied("У вас нет прав доступа к этому макету")

        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        """Проверка прав доступа"""
        user = self.request.user
        return (
                user == self.object.user or  # Автор поста
                user.role == 'DESIGNER'  # Пользователь с ролью DESIGNER
        )


@login_required
def add_comment(request, id):
    design = get_object_or_404(OrderDesign, id=id)
    if request.user.role == 'DESIGNER' or request.user.role == 'CUSTOMER_RETAIL' :

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
    success_url = reverse_lazy("designs:design_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# class CommentCreateView(CreateView):
#     model = Comments
#     form_class = CommentForm
#     template_name = 'designs/add_comment.html'
#
#     def form_valid(self, form):
#         form.instance.design_id = self.kwargs['design_id']
#         form.instance.author = self.request.user
#         return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('design_detail', kwargs={'pk': self.kwargs['design_id']})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    form_class = CommentForm
    template_name = 'designs/add_comment.html'

    def form_valid(self, form):
        design = OrderDesign.objects.get(pk=self.kwargs['design_id'])
        form.instance.design = design  # Устанавливаем связь с дизайном
        form.instance.author = self.request.user
        print("Design ID:", self.kwargs['design_id'])  # Проверьте что получаете ID
        design = get_object_or_404(OrderDesign, pk=self.kwargs['design_id'])
        print("Found design:", design)  # Проверьте что объект существует
        return super().form_valid(form)


    # def get_success_url(self):
    #     return reverse('design_detail', kwargs={'pk': self.kwargs['design_id']})

    def get_success_url(self):
        return reverse_lazy('designs:design_detail', kwargs={'pk': self.kwargs['design_id']})


# def get_comments(request, design_id):
#     '''endpoint for JS'''
#     design = get_object_or_404(OrderDesign, pk=design_id)
#     comments = design.comments.all().order_by('created_at')
#     comments_json = serializers.serialize('json', comments)
#     return JsonResponse(comments_json, safe=False)


def get_comments(request, design_id):
    design = get_object_or_404(OrderDesign, pk=design_id)
    comments = design.comments.all().order_by('created_at').select_related('author')

    comments_data = []
    for comment in comments:
        comments_data.append({
            'fields': {
                'author': comment.author.pk,
                'text': comment.text,
                'image': comment.image.url if comment.image else None,
                'created_at': comment.created_at.isoformat(),
            }
        })

    return JsonResponse(comments_data, safe=False)