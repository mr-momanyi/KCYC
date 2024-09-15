from django.contrib import admin


# Register your models here.
from.models import Post, Article, Updates, Profile, CommentBlog, CommentArticle, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS
    filter_horizontal = ('tags',)

    

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = [ 'publish']
    show_facets = admin.ShowFacets.ALWAYS
    filter_horizontal = ('tags',)



@admin.register(Updates)
class UpdatesAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'published']
    list_filter = [ 'published']
    search_fields = ['title', 'body', 'image', 'image_url']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published'
    ordering = [ 'published']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']


@admin.register(CommentBlog)
class CommentBlogAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']


@admin.register(CommentArticle)
class CommentArticleAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'article', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']