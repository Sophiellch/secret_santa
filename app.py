import streamlit as st
import pandas as pd
from PIL import Image
from itertools import chain
import random
from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image
import streamlit as st

audio_file = open('musique.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/mp3')

# Fonction pour charger l'image avec mise en cache
@st.cache_resource
def load_image(image_path):
    return Image.open(image_path)

# Fonction pour générer les paires de Secret Santa avec mise en cache
@st.cache_data
def generate_secret_santa(participants):
    random.shuffle(participants)
    return list(zip(participants, participants[1:] + [participants[0]]))

# Fonction pour envoyer les e-mails
def send_email(from_email, from_password, to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Connexion au serveur SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return str(e)

# Informations de l'expéditeur
FROM_EMAIL = "secret.santawild2024@gmail.com"
FROM_PASSWORD = "xcwbcedwgvohpnfv"  

# Initialisation de l'application Streamlit
st.title("Secret Santa des Blue Monthy")

# Afficher une image en arrière-plan
st.image(load_image("santa.jpg"), use_container_width=True)

# Étape 1 : Entrer les noms des participants et leurs e-mails
st.subheader("Étape 1 : Entrez les noms des participants et leurs e-mails")
entries = st.text_area(
    "Saisissez les noms et adresses e-mail des participants (nom:email), un par ligne :"
).splitlines()

participants = []
emails = {}

for entry in entries:
    if ":" in entry:
        name, email = entry.split(":", 1)
        name, email = name.strip(), email.strip()
        if name and email:
            participants.append(name)
            emails[name] = email

if len(participants) < 2:
    st.warning("Veuillez entrer au moins deux participants avec des e-mails valides pour continuer.")
else:
    # Bouton pour générer le tirage
    if st.button("Générer le Secret Santa et envoyer les e-mails"):
        # Générer les paires de Secret Santa
        secret_santa_pairs = generate_secret_santa(participants)
        all_emails_sent = True

        for donneur, receveur in secret_santa_pairs:
            recipient_email = emails[donneur]
            subject = "Votre tirage Secret Santa 🎅"
            body = f"Hello {donneur},\n\nVotre mission est d’offrir un cadeau à {receveur} ! \n\nBudget aux alentours de 5€ \n\nNous échangerons ces cadeaux le 20 Décembre 2024 \nA cette occasion nous porterons tous notre plus beau pull de Noël 🎄 \nMerci de garder cette information secrète et amusez-vous ! 🎁\n\nJoyeux Noël !\n\nSecret Santa 🎅"
            
            # Envoyer l'e-mail
            result = send_email(FROM_EMAIL, FROM_PASSWORD, recipient_email, subject, body)
            if result is not True:
                st.error(f"Erreur d'envoi pour {donneur}: {result}")
                all_emails_sent = False

        if all_emails_sent:
            st.success("Tous les e-mails ont été envoyés avec succès !")


