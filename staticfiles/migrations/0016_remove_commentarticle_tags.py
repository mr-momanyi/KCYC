# Generated by Django 5.0.6 on 2024-08-09 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_commentarticle_tags_alter_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentarticle',
            name='tags',
        ),
    ]
