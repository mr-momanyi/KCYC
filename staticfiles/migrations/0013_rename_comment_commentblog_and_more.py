# Generated by Django 5.0.6 on 2024-06-17 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_commentarticle'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='CommentBlog',
        ),
        migrations.RenameIndex(
            model_name='commentblog',
            new_name='blog_commen_created_a134b3_idx',
            old_name='blog_commen_created_0e6ed4_idx',
        ),
    ]
