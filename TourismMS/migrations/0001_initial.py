# Generated by Django 5.1.4 on 2024-12-30 22:04

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='attractions/')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tourist',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('booking_number', models.CharField(max_length=100, unique=True)),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], max_length=50)),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TourismMS.attraction')),
                ('tourist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TourismMS.tourist')),
            ],
        ),
        migrations.AddField(
            model_name='attraction',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TourismMS.category'),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code', models.ImageField(upload_to='tickets/')),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TourismMS.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TourismMS.tourist')),
            ],
        ),
        migrations.CreateModel(
            name='ContentCreator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TourismMS.tourist')),
            ],
        ),
    ]
