from django.http import Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def index(request):
    posts = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )[:5]
    return render(
        request,
        template_name='blog/index.html',
        context={'post_list': posts}
    )


def post_detail(request, post_id):
    queryset = Post.objects.select_related(
        'category',
        'location'
    ).all()
    post = get_object_or_404(queryset, pk=post_id)

    if (post.pub_date > timezone.now()
            or not post.is_published
            or not post.category.is_published):
        raise Http404(f"Пост с id {post_id} не найден.")

    return render(
        request,
        template_name='blog/detail.html',
        context={'post': post}
    )


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if not category.is_published:
        raise Http404(f"Категория с slug {category_slug} не найдена.")

    posts = category.posts.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category=category
    )

    return render(
        request,
        template_name='blog/category.html',
        context={'post_list': posts, 'category': category}
    )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
