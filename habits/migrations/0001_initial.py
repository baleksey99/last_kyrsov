from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, to='auth.User')),
                ('telegram_chat_id', models.BigIntegerField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=255)),
                ('time', models.TimeField()),
                ('action', models.TextField()),
                ('is_pleasant', models.BooleanField(default=False)),
                ('periodicity', models.IntegerField(default=1)),
                ('reward', models.CharField(blank=True, max_length=255)),
                ('execution_time', models.DurationField()),
                ('is_public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.customuser')),
                ('related_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.habit')),
            ],
        ),
    ]
