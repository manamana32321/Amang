# Generated by Django 5.0.4 on 2024-04-19 14:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_rename_music_song_remove_team_artist_team_songs"),
    ]

    operations = [
        migrations.AddField(
            model_name="concert",
            name="name",
            field=models.CharField(
                default="Concert defualt name",
                max_length=255,
                unique=True,
                verbose_name="name",
            ),
            preserve_default=False,
        ),
    ]
