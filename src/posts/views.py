from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect, reverse

from .models import Post
from .forms import CommentForm
from marketing.models import SignUp



def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title')) 
    return queryset


def category_tags():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title')) 
    return queryset

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    
    context = {
        'queryset': queryset,
    }
    return render(request, 'search_results.html', context)



def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    
    if request.method == 'POST':
        email = request.POST['email']
        new_signup = SignUp() #object
        new_signup.email = email
        new_signup.save()
        
    context = {
        'object_list': featured,
        'latest': latest
    }
    return render(request, 'index.html', context)


def blog(request):
    category_count = get_category_count()
    category_tag = category_tags()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post_list = Post.objects.all()
    #pagination
    paginator = Paginator(post_list, 2) 
    page_request_var = 'page'
    page  = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)


    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
        'categories_tag': category_tag,
    }
    return render(request, 'blog.html', context)

def post(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid:
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs = {
                'id': post.id
            }))

    context = { 
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form,
    }
    return render(request, 'post.html', context)