from datetime import datetime, timedelta

# Début des publications : 8 août 2025
start_date = datetime(2025, 8, 8)

# 15 speakers, 3 publications par jour → 5 jours
total_speakers = 15
posts_per_day = 3
total_days = (total_speakers + posts_per_day - 1) // posts_per_day  # arrondi au jour supérieur

# Heures de publication par jour (GMT)
post_times = ["09:00:00", "13:00:00", "17:00:00"]

# Données de base des speakers
speakers = [
    {"first_name": "Daniel", "last_name": "Ametsowou", "email": "frusadev@gmail.com"},
    {"first_name": "Denis", "last_name": "AKPAGNONITE", "email": "akpagnonited@gmail.com"},
    {"first_name": "Ibi", "last_name": "Fiberesima", "email": "fiberesimaibi@gmail.com"},
    {"first_name": "Julius", "last_name": "Boakye", "email": "bbjulius900@gmail.com"},
    {"first_name": "Wilfrid", "last_name": "GOEH", "email": "einswilligoeh@gmail.com"},
    {"first_name": "Harmony", "last_name": "Elendu", "email": "elenduharmony@gmail.com"},
    {"first_name": "Yao Gervais", "last_name": "Amoah", "email": "gervaisamoah@gmail.com"},
    {"first_name": "Caleb", "last_name": "ADOGLI", "email": "calebadogli53@gmail.com"},
    {"first_name": "Koami Afantchao", "last_name": "AZIABOU", "email": "aziaboukoami@gmail.com"},
    {"first_name": "Serge", "last_name": "Koudoro", "email": "SergeKoudoro"},
    {"first_name": "Zokora Elvis", "last_name": "Gbagnon", "email": "degbagnon@gmail.com"},
    {"first_name": "Basile", "last_name": "Desjuzeur", "email": "basile.desjuzeur@polytechnique.edu"},
    {"first_name": "Awa", "last_name": "Coulibaly", "email": "awa@example.com"},
    {"first_name": "Noël", "last_name": "Tadegnon", "email": "noel@example.com"},
    {"first_name": "Raoul", "last_name": "Missodey", "email": "raoul@example.com"},
]

# Liens communs
slide_deck = "https://docs.google.com/presentation/d/1WJhfR70xNuk6mufFBKWcxhJw6tMW4PML/edit?usp=sharing"
guidelines = "https://docs.google.com/document/d/1LlRMjgqxyTMsNdh4m8TFIq02KqqlFxrN9mCWfAjTnWo/edit?usp=sharing"

# Générer le JSON final avec horaires et autres infos
json_speakers = []

for i, speaker in enumerate(speakers):
    day = i // posts_per_day
    slot = i % posts_per_day
    date = start_date + timedelta(days=day)
    full_datetime = f"{date.strftime('%A, %d %B %Y')} at {post_times[slot]} GMT"
    flower_name = f"{speaker['first_name'].lower()}.png"

    json_speakers.append({
        "first_name": speaker["first_name"],
        "last_name": speaker["last_name"],
        "email": speaker["email"],
        "publication_time": full_datetime,
        "flower": flower_name,
        "slide_deck": slide_deck,
        "guidelines": guidelines
    })

import json
from caas_jupyter_tools import display_dataframe_to_user
import pandas as pd

# Afficher sous forme de tableau pour vérification humaine
df = pd.DataFrame(json_speakers)
display_dataframe_to_user(name="PyCon Togo 2025 - Speakers Schedule", dataframe=df)

# Retourner le JSON
json_speakers_text = json.dumps(json_speakers, indent=2)
json_speakers_text[:1000]  # Display preview only to avoid overwhelming the UI
