from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class Session(models.Model):
    TYPES = (
        ("vocal", "vocal"),
        ("guitar", "guitar"),
        ("bass", "bass"),
        ("synthesizer", "synthesizer"),
        ("drum", "drum"),
        ("others", "others"),
    )
    name = models.CharField("name", max_length=16, choices=TYPES, unique=True)

    def __str__(self) -> str:
        return self.name


class MemberManager(UserManager):
    pass


class Member(SoftDeleteMixin, AbstractUser):
    SKILL_LEVEL = (
        ("beginner", "beginner"),
        ("intermediate", "intermediate"),
        ("advanced", "advanced"),
    )
    sessions = models.ManyToManyField(Session, related_name="members")
    main_session = models.ForeignKey(Session, on_delete=models.PROTECT, null=True, blank=True)
    skill_level = models.CharField(max_length=16, choices=SKILL_LEVEL)

    objects = MemberManager()


class Song(SoftDeleteMixin, models.Model):
    name = models.CharField("name", max_length=255, unique=True)
    artist = models.CharField("artist", max_length=255)
    link = models.URLField("link", null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class TeamManager(models.Manager):
    def members(self):
        team:Team = self.object
        return (
            team.vocal1, team.vocal2, team.guitar1, team.guitar2,
            team.bass1, team.bass2, team.synthesizer1, team.synthesizer2,
            team.drum, team.others)


class Team(models.Model):
    name = models.CharField("name", max_length=255, unique=True)
    
    vocal1          = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="team_as_vocal1", null=True, blank=True)
    vocal2          = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="team_as_vocal2", null=True, blank=True)
    guitar1         = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="team_as_guitar1", null=True, blank=True)
    guitar2         = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="team_as_guitar2", null=True, blank=True)
    bass1           = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="team_as_bass1", null=True, blank=True)
    bass2           = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="team_as_bass2", null=True, blank=True)
    synthesizer1    = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="team_as_synthesizer1", null=True, blank=True)
    synthesizer2    = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="team_as_synthesizer2", null=True, blank=True)
    drum            = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="team_as_drum", null=True, blank=True)
    others          = models.ManyToManyField(Member, related_name="teams", blank=True)

    songs = models.ManyToManyField(Song, related_name="played_by")

    def __str__(self) -> str:
        return self.name


class Collaboration(models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    song = models.ForeignKey(Song, on_delete=models.PROTECT)

    def __str__(self):
        return f"team {self.team} playing {self.song}"


class Concert(models.Model):
    name = models.CharField("name", max_length=255, unique=True)
    collaborations = models.ManyToManyField(Collaboration, related_name="concerts")

    def __str__(self) -> str:
        return self.name
