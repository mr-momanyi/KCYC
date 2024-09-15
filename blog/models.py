from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.urls import reverse

from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter
            (status = Post.Status.PUBLISHED)
        )

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'DRAFT' 
        PUBLISHED = 'PB', 'Published'
    title =  models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                        related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices = Status.choices,
                              default = Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()
    excerpt = models.TextField(null=True, blank=True)  # Excerpt field
    # adding images in the blog
    image = models.ImageField(upload_to='Post/', null=True, blank=True)
    image = models.ImageField(upload_to='updates/', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True) 
    image_url = models.URLField(max_length=500, blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    
    def __str__(self):
        return self.title
    
    
    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = self.body[:200]  # Generate an excerpt from the body if not provided
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
            ]
 
        def __str__(self):
            return self.title
        
        
        
        # def get_absolute_url(self):
        #     return reverse('blog:post_detail', args =[self.id])

        #add the model manager for the article models to set the custom queryset 
class PublishedManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter
            (status = Article.Status.PUBLISHED)
        )
class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published' 

    title =  models.CharField(max_length=250)
    # slug = models.SlugField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                        related_name='blog_articles')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                               choices = Status.choices,
                               default = Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager
    excerpt = models.TextField(null=True, blank=True)  # Excerpt field
    image = models.ImageField(upload_to='Post/', null=True, blank=True)
    image = models.ImageField(upload_to='updates/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='articles', blank=True)




    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields = ['-publish'])
        ]

        def __str__(self):
            return self.title
        
    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = self.body[:200]  # Generate an excerpt from the body if not provided
        super().save(*args, **kwargs)

    def get_related_articles(self):
        return Article.objects.filter(tags__in=self.tags.all()).exclude(id=self.id).distinct().order_by('-publish')[:4]

        
        #not yet fixed this updates views and urls as well as its template
class Updates(models.Model):
   
    title =  models.CharField(max_length=250)
    slug = models.SlugField(unique= True) 
    body = models.TextField()
    image = models.ImageField(upload_to='updates/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    published = models.DateTimeField(default = timezone.now)
   
    class Meta:
        ordering = ['-published']
        indexes = [
                    models.Index(fields=['-published']),
                    ]

    def __str__(self):
        return self.title
    
    def display_image(self):
        if self.image:
            return mark_safe(f'<img scr="{self.image.url}" width="150"/>')
        elif self.image_url:
            return mark_safe(f'<img scr="{self.image.url}" width="150"/>')
        return "No Image"
    
    display_image.short_description = 'Image'
    display_image.allow_tags = True

# the profile setting model
class Profile(models.Model):
    user = models.OneToOneField(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
    upload_to='users/%Y/%m/%d/', blank=True)
def __str__(self):
    return f'Profile of {self.user.username}'


# the comments model
class CommentBlog(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
# the comments model
class CommentArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]
    def __str__(self):
        return f'Comment by {self.name} on {self.article}'
    

# tags = TaggableManager()
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



        
        #this was adding the seo friendly 
        #urls that failed to work early
    
