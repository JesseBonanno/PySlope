# Generated by Django 3.2.4 on 2022-03-29 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slope', '0003_auto_20220328_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialmodel',
            name='color',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='materialmodel',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pointloadmodel',
            name='color',
            field=models.CharField(blank=True, default='blue', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='udlmodel',
            name='color',
            field=models.CharField(blank=True, default='red', max_length=20, null=True),
        ),
    ]