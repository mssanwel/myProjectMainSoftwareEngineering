# Generated by Django 3.1.7 on 2021-03-27 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('population', models.IntegerField(default=0)),
                ('apiString', models.CharField(max_length=2000)),
                ('urlString', models.CharField(max_length=2000)),
            ],
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
