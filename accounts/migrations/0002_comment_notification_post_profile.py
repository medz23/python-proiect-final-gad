# Generated by Django 3.1.7 on 2021-02-28 04:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=25)),
                ('image', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('description', models.CharField(blank=True, max_length=100)),
                ('camps', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('followers', models.ManyToManyField(blank=True, related_name='followers', to='accounts.User')),
                ('follows', models.ManyToManyField(blank=True, related_name='follows', to='accounts.User')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=111, null=True, unique=True)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='post_images')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to='accounts.User')),
                ('tagged_users', models.ManyToManyField(blank=True, related_name='tagged_users', to='accounts.User')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(blank=True, max_length=50)),
                ('read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.post')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='accounts.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.post')),
            ],
        ),
    ]
