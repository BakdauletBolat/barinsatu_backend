# Generated by Django 4.0.1 on 2022-02-08 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('story', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('isLiked', models.BooleanField(default=True)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_likes', to='story.story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Лайк для Историй',
                'verbose_name_plural': 'Лайк для Историй',
            },
        ),
        migrations.CreateModel(
            name='StoryComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_comments', to=settings.AUTH_USER_MODEL)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_comments', to='story.story')),
            ],
            options={
                'verbose_name': 'Коммент для Историй',
                'verbose_name_plural': 'Комменты для Историй',
            },
        ),
        migrations.AddConstraint(
            model_name='storylike',
            constraint=models.UniqueConstraint(fields=('user', 'story'), name='unique_like_story'),
        ),
    ]
