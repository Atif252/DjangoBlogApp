# Generated by Django 2.2.2 on 2019-09-15 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Questions',
            new_name='Question',
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'The Question', 'verbose_name_plural': 'Peoples Questions'},
        ),
    ]
