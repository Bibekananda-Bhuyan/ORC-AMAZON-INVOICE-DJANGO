# Generated by Django 3.1 on 2020-08-10 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0007_auto_20200810_0322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='is_digitized',
        ),
        migrations.AddField(
            model_name='invoice',
            name='is_digitized_i',
            field=models.BooleanField(default=True, verbose_name='Is Degitized'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='trackingId',
            field=models.CharField(default='uhnpcvpnsx', max_length=100),
        ),
    ]
