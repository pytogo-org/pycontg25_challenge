from email_template import render_email_template

from db import get_some_thing
from send_mail import send_email_with_or_without_attachment

def welcome_msg(first_name):
    msgs = [{
        "subject": "[Français] Bienvenu(e) au Challenge 30 Jours de Python",
        "body": f"""\
         <h2>Bonjour {first_name},</h2>
        <p>
        Félicitations ! Tu viens de t’inscrire au <strong>Challenge 30 Jours Python</strong> organisé par <strong>Python Togo</strong> en prélude à <strong>PyCon Togo 2025</strong>, prévu pour le 23 août.
        </p>
        <p>
        <strong>Durée du challenge :</strong> du 23 juillet au 22 août à 23h59. <br>
        Chaque jour, tu recevras un email contenant :
        </p>s
        <ul>
        <li>Le défi Python du jour</li>
        <li>Des ressources pour t’aider à le résoudre</li>
        <li>Un lien pour soumettre ta solution</li>
        </ul>
        <p>
        <strong>Soumission :</strong> rends-toi sur notre plateforme 
        <a href="https://challenge.pytogo.org/">https://challenge.pytogo.org/</a> et soumets :
        </p>
        <ul>
        <li>Le lien vers ton code (GitHub, Replit, etc.)</li>
        <li>Une brève explication de ta solution (optionnelle)</li>
        </ul>
        <p>
        <strong>Rejoins notre serveur Discord :</strong> 
        <a href="https://pytogo.org/discord">https://pytogo.org/discord</a><br>
        Une fois à l’intérieur :
        </p>
        <ul>
        <li>Présente-toi dans le canal <code>#challenge-30jours</code></li>
        <li>Signale que tu participes pour recevoir un rôle spécial</li>
        <li>Reste actif pour profiter de l'entraide de la communauté</li>
        </ul>
        <p>
        Tu as un serveur Discord ? N'hésite pas à nous le dire si tu veux collaborer avec nous.
        </p>
        <p>
        Pour toute question ou assistance, écris-nous à <a href="mailto:challenge@pytogo.org">challenge@pytogo.org</a>.
        </p>

        """},
        {
            "subject": "[English Version] Welcome to the 30-Day Python Challenge",
            "body": f"""\
        <h2>Hi  {first_name},</h2>
        <p>
        Congratulations! You have successfully registered for the <strong>30-Day Python Challenge</strong> organized by <strong>Python Togo</strong>, in preparation for <strong>PyCon Togo 2025</strong>, taking place on August 23.
        </p>
        <p>
        <strong>Challenge duration:</strong> from July 23 to August 22 at 11:59 PM UTC.<br>
        Each day, you will receive an email containing:
        </p>
        <ul>
        <li>The daily Python challenge</li>
        <li>Helpful learning resources</li>
        <li>A link to submit your solution</li>
        </ul>
        <p>
        <strong>Submission:</strong> go to 
        <a href="https://challenge.pytogo.org/">https://challenge.pytogo.org/</a> and submit:
        </p>
        <ul>
        <li>The link to your code (GitHub, Replit, etc.)</li>
        <li>A brief explanation of your solution (optional)</li>
        </ul>
        <p>
        <strong>Join our Discord server:</strong> 
        <a href="https://pytogo.org/discord">https://pytogo.org/discord</a><br>
        Once inside:
        </p>
        <ul>
        <li>Introduce yourself in the <code>#challenge-30days</code> channel</li>
        <li>Let us know you're participating so we can assign you a special role</li>
        <li>Stay active and engage with the community</li>
        </ul>
        <p>
        Do you already have a Discord server? Let us know if you'd like to collaborate.
        </p>
        <p>
        For help or support, reach out at <a href="mailto:challenge@pytogo.org">challenge@pytogo.org</a>.
        </p>
        """
        }
    ]
    return msgs


def get_daily_challenge_email(first_name, day_number, fr_title, en_title, fr_link, en_link):
    return [{
        "subject": f"[Jour {day_number}] {fr_title}",
        "body": f"""\
        <h2>Bonjour {first_name},</h2>
        <p>Voici ta tâche du jour <strong>Jour {day_number}</strong> :</p>
        <p><strong>{fr_title}</strong></p>
        <p>👉 <a href="{fr_link}">Accède à la tâche ici</a></p>
        <br>
        <p>Bonne chance et n'oublie pas de soumettre ta solution !</p>
        """,
    }, {
        "subject": f"[Day {day_number}] {en_title}",
        "body": f"""\
        <h2>Hi {first_name},</h2>
        <p>Here is your task for <strong>Day {day_number}</strong>:</p>
        <p><strong>{en_title}</strong></p>
        <p>👉 <a href="{en_link}">Access the challenge here</a></p>
        <br>
        <p>Good luck and don’t forget to submit your solution!</p>
        """,
    }]


def get_bilingual_challenge_email(first_name, day_number, fr_title, en_title, fr_link, en_link):
    subject = f"[Day {day_number}] - {en_title} | [Jour {day_number}] - {fr_title}"

    body = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 650px; margin: auto; color: #333;">
        <h2>👋 Hello {first_name}!</h2>
        <p>
            This is your daily challenge email from <strong>Python Togo</strong> .<br>
            You’ll find <strong>the English version first</strong>, followed by <strong>the French version below</strong>.
        </p>

        <h3> 🇬🇧 English Challenge</h3>
        <p>
            <strong>Day {day_number} - {en_title}</strong><br>
            <a href="{en_link}">Click here to access today’s challenge</a>
        </p>

        <h3>🇫🇷  Défi en Français</h3>
        <p>
            <strong>Jour {day_number} - {fr_title}</strong><br>
            <a href="{fr_link}">Clique ici pour accéder à la tâche du jour</a>
        </p>

        <hr>

        <p style="font-size: 0.95em; color: #555;">
             Reminder / Rappel : Ce n’est pas la vitesse qui compte, mais la régularité.<br>
            It's not about speed, it's about consistency. Keep going!
        </p> 

        <hr>
        <br>

        <h3>Join the #workshop voice channel / Rejoins le canal vocal <a href="https://discord.gg/Uyf6nk436D">#workshop</a> </h3>
        <p>
             <strong>🇬🇧 We’ve set up a dedicated voice channel <code>#workshop</code> on our Discord server!</strong><br>
            Come share your solution, ask questions, or just listen. Every day, we’ll host live mini-workshops to review the current or previous day’s task.<br>
            No pressure Just good vibes, good Python, and community support 😊
        </p>

        <p>
            <strong>🇫🇷 Un canal vocal <code>#workshop</code> est disponible sur notre serveur Discord !</strong><br>
            Viens partager ta solution, poser tes questions ou simplement écouter. Chaque jour, on organise de petits ateliers audio pour discuter de la tâche du jour (ou d’hier).<br>
            Pas besoin d’être expert. On apprend tous ensemble 😊
        </p>

        <p style="font-size: 0.9em;">
            — The <strong>Python Togo</strong> team<br>
            Discord  : <a href="https://pytogo.org/discord">pytogo.org/discord</a>
        </p>
    </div>
    """

    return subject, body



if __name__ == "__main__":
    participants = get_some_thing("participants")
    if not participants:
        print("No participants found.")
        
    for participant in participants:
            first_name = participant.get('full_name', 'Participant')
            participant_email = participant.get('email')
            email_msgs = welcome_msg(first_name)
            for email in email_msgs:
                body = render_email_template(
                    first_name=first_name,
                    message=email['body']
                )
                subject = email['subject']
                
                send_email_with_or_without_attachment(body, subject, participant_email)