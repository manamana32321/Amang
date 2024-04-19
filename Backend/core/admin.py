from django.contrib import admin
from .models import Session, Member, Song, Team, Collaboration, Concert


models = (Session, Member, Song, Team, Collaboration, Concert)
for model in models:
    admin.site.register(model)
