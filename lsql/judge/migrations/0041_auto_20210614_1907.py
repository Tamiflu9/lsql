# Generated by Django 3.2.4 on 2021-06-14 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0040_alter_usedhint_request_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='veredict_code',
            new_name='verdict_code',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='veredict_message',
            new_name='verdict_message',
        ),
    ]
