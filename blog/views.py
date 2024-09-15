from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from .models import Post, Article, Updates
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from.models import Profile
from django.db.models import Count
from. forms import (LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm,
                     EmailPostForm, CommentBlogForm, CommentArticleForm, SearchForm)
# for search query
from django.db.models import Q

from .models import Post, Article, Updates
from django.contrib.postgres.search import SearchVector


# paginator
# from django.core.paginator import Paginator


from django.core.mail import send_mail
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from django.conf import settings



@login_required
def home(request):
    latest_post = Post.objects.order_by('-published_at').first()
    return render(request, 'blog/post/home.html', {'latest_post': latest_post})
@login_required
def join_us(request):
    return render(request, 'blog/post/join.html')
@login_required
def post_list(request):
    posts = Post.published.all()

    # # Pagination with 3 posts per page
    # paginator = Paginator(post_list, 3)
    # page_number = request.GET.get('page', 1)
    # posts = paginator.page(page_number)

    
    return render(request,'blog/post/list.html',
                  {'posts':posts})
@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    posts = Post.published.all()

    # Get related posts based on shared tags
    related_posts = Post.published.filter(tags__in=post.tags.all()).exclude(id=post.id).annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    

    # Fetch the most recent blog post
    latest_post = Post.published.order_by('-publish').first()

    

    # Render the post detail template
    return render(
        request,
        'blog/post/detail.html',  # Your post detail template
        {
            'post': post,
            'posts': posts,
            'related_posts': related_posts,  # Include related posts in the context
            'latest_post': latest_post,      # Include the latest post in the context
        }
    )
@login_required
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'blog/post/article_list.html', {'articles':articles})
@login_required
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)  # Fetch the article by its slug
    related_articles = Article.objects.filter(tags__in=article.tags.all()).exclude(id=article.id).distinct().order_by('-publish')[:4]
    comments = article.comments.filter(active=True)  # List of active comments for this post
    form = CommentArticleForm()

    # Fetch other published articles, excluding the current one
    articles = Article.objects.exclude(id=article.id).filter(status=Article.Status.PUBLISHED)[:5]

    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'articles': articles,  # Pass the list of articles to the template
        'related_articles': related_articles,
        
    }
    return render(request, 'blog/post/article_detail.html', context)
@login_required
# the view of the updates is yet to be added over here
def post_updates(request):
    updates = Updates.objects.all().order_by('-published')
    return render(request, 'blog/post/updates.html', {'updates': updates})
@login_required
def post_home(request):
    return render(request, 'blog/post/home.html')
@login_required
def post_about(request):
    return render(request, 'blog/post/about.html')

# registration views
@login_required
def dashboard(request):

    return render(request, 'blog/home.html', {'section': 'home'})
@login_required
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authentication successful')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()
            return render(request, 'blog/post/login.html', {'form': form})
# @login_required        
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user's profile
            Profile.objects.create(user=new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'user_form': user_form})


# logout custom view
@login_required
def logout_confirmation_view(request):
    if request.method =='POST':
        logout(request)
        return redirect('blog:logout_success')
    return render(request, 'registration/logout.html')

def logout_success_view(request):
    return render(request, 'registration/logout_success.html')

@login_required
def edit(request):
    if request.method == 'POST':
        # Initialize the forms with POST data and files
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the forms if they are valid
            user_form.save()
            profile_form.save()
            return render(request, 'blog/edit_done.html')  # Optional success page
    else:
        # Initialize the forms with the current user instance for non-POST requests
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    # Render the edit page with the forms
    return render(request, 'blog/edit.html', {'user_form': user_form, 'profile_form': profile_form})
@login_required
def post_contact(request):
    return render(request, 'blog/post/contact.html')

@login_required
# email post form view - sharing post via email
def post_share(request, post_id):
# Retrieve post by id
    post = get_object_or_404(
    Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        
# Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
# Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{cd['name']} ({cd['email']}) "
                        f"recommends you read {post.title}")
            message = (f"Read {post.title} at {post_url}\n\n"
                        f"{cd['name']}\'s comments: {cd['comments']}")
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cd['to']])
            sent = True
# ... send email
    else:
        form = EmailPostForm()
        return render(request,'blog/post/share.html', {'post': post,'form': form, 'sent':sent})
    

@login_required    # share by email for the articles
def article_share(request, article_id):
# Retrieve post by id
    article = get_object_or_404(
    Article, id=article_id, status=Article.Status.PUBLISHED)
    if request.method == 'POST':
        sent = False
# Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
# Form fields passed validation
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())
            subject = (f"{cd['name']} ({cd['email']}) "
                        f"recommends you read {article.title}")
            message = (f"Read {article.title} at {article_url}\n\n"
                        f"{cd['name']}\'s comments: {cd['comments']}")
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cd['to']])
            sent = True
# ... send email
    else:
        form = EmailPostForm()
        return render(request,'blog/post/share.html', {'article': article,'form': form, 'sent':sent})
@login_required    
# COMMENT VIEW
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentBlogForm(data=request.POST)
    
    if form.is_valid():
        # If the form is valid, save the comment
        commentblog = form.save(commit=False)
        commentblog.post = post
        commentblog.save()
        
        # Render the blog_comment template with the saved comment
        return render(request, 'blog/post/blog_comment.html', {'post': post, 'form': form, 'commentblog': commentblog})
    
    # If the form is not valid, handle it here, possibly rendering the form again with errors
    return render(request, 'blog/post/blog_comment.html', {'post': post, 'form': form})
    
@login_required
@require_POST
def article_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id, status=article.Status.PUBLISHED)
    commentarticle = None
# A comment was posted
    form = CommentArticleForm(data=request.POST)
    if form.is_valid():
    # Create a Comment object without saving it to the database
        commentarticle = form.save(commit=False)
# Assign the post to the comment
        commentarticle.article = article
# Save the comment to the database
        commentarticle.save()
        return render(request, 'blog/post/article_comment.html',{'article': article, 'form': form, 
                                                         'commentarticle': commentarticle})
@login_required    
def library(request):
    # Fetch all published articles or any specific content for the library
    # library_articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-publish')
   return render(request, 'blog/post/library.html')
@login_required
def courses(request):

    return render(request, 'blog/post/courses.html')
@login_required
def services(request):

    return render(request, 'blog/post/services.html')
@login_required
def causes(request):

    return render(request, 'blog/post/causes.html')

def effects(request):

    return render(request, 'blog/post/effects.html')
@login_required
def solutions(request):

    return render(request, 'blog/post/solutions.html')


# search query view


@login_required
def search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            # Search across Post, Article, and Updates models
            post_results = Post.published.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

            article_results = Article.objects.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

            update_results = Updates.objects.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query)
            ).distinct()

            # Combine results into one list
            results = list(post_results) + list(article_results) + list(update_results)

    return render(request, 'blog/post/search.html', {
        'form': form,
        'query': query,
        'results': results,
    })










# User = get_user_model()

# def password_reset_request(request):
#     if request.user =='POST':
#         password_reset_form = PasswordResetForm(request.POST)
#         if password_reset_form.is_valid():
#             data = password_reset_form.cleaned_data['email']
#             associated_users = User.objects.filter(email=data)
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject = "Password Reset Requested"
#                     email_template_name = "blog/registration/password_reset_email.txt"
#                     c = {
#                             "email": user.email,
#                             'domain': request.META['HTTP_HOST'],
#                             'site_name': 'Website',
#                             "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                             "user": user,
#                             'token': default_token_generator.make_token(user),
#                             'protocol': 'http',

#                         }
#                     email = render_to_string(email_template_name, c)
#                     send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
#             return redirect("blog:password_reset_done")
#         password_reset_form = PasswordResetForm()
#         return render(request, "blog/registration/password_reset.html", {"password_reset_form":password_reset_form})
        
# def password_reset_done(request):
#     return render(request, 'blog/registration/password_reset_done.html')
# def password_reset_confirm(request, uid64=None, token=None):
#     try:
#         uid = force_str(urlsafe_base64_decode(uid64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, user.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         if request.method == 'POST':
#             set_password_form = SetPasswordForm(user, request.POST)
#             if set_password_form.is_valid():
#                 set_password_form.save()
#                 return redirect('blog/registration/password_reset_complete')
#         else:
#             set_password_form = SetPasswordForm(user)
#     else:
#         return HttpResponse('password reset link is invalid', status = 400)
#     return render(request, 'blog/registration/password-reset_confirm.html', {'form':set_password_form})

# def password_reset_complete(request):
#     return render(request, 'blog/registration/password_reset_complete.html')






# search query view
# def post_search(request):
#     form = PostSearchForm
#     query = request.GET.get('query', '')

#     if query:
#         results = Post.objects.filter(title=query)
#         results = Article.objects.filter(title=query)
#         results = Updates.objects.filter(title=query)
#     else:
#        results = Post.objects.none() 
#        results = Article.objects.none() 
#        results = Updates.objects.none() 

#        form = form

#     return render(request, 'blog/post/search.html', {'results':results})


