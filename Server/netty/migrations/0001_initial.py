# Generated by Django 2.1.15 on 2022-07-07 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('user_id', models.CharField(max_length=200)),
                ('creation', models.CharField(max_length=200)),
                ('expiration', models.CharField(max_length=200)),
            ],
        ),
    ]
