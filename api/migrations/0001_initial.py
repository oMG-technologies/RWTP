# Generated by Django 3.2.3 on 2021-07-10 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('conversion', models.CharField(max_length=6, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i', models.IntegerField()),
                ('frontCard', models.CharField(max_length=40)),
                ('backCard', models.CharField(max_length=40)),
                ('source_language', models.CharField(max_length=10)),
                ('target_language', models.CharField(max_length=10)),
                ('pronunciation_frontCard', models.CharField(max_length=200)),
                ('pronunciation_backCard', models.CharField(max_length=200)),
                ('translation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='api.language')),
            ],
            options={
                'verbose_name_plural': 'Translations',
            },
        ),
    ]
