from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('Education', '0001_initial'),
    ]

    operations = [
        # Step 1: Add slug as nullable first (no unique constraint yet)
        migrations.AddField(
            model_name='news',
            name='slug',
            field=models.SlugField(max_length=255, null=True, blank=True),
        ),
    ]
