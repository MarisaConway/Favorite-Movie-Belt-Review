# Generated by Django 2.1.7 on 2019-03-22 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('addedby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_movies', to='myapp.User')),
                ('favorites', models.ManyToManyField(related_name='favorites', to='myapp.User')),
            ],
        ),
    ]