# Generated by Django 4.0.3 on 2023-05-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrailList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
            ],
        ),
    ]
