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


def get_pre_challenge_info_email(first_name):
    subject = "Challenge starts at midnight | PyCon Togo registration opens tomorrow"

    body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 650px; margin: auto; line-height: 1.6; color: #333;">
        <h2>Bonjour {first_name}, Hello!</h2>

        <p>
            🇫🇷 Le <strong>Challenge 30 Jours Python</strong> organisé par <strong>Python Togo</strong> commence ce soir à <strong>00h00</strong> (minuit).<br>
            🇬🇧 The <strong>30 Days of Python Challenge</strong> starts tonight at <strong>00:00 UTC</strong>.
        </p>

        <p>
            🇫🇷 Tu recevras un email chaque jour avec une tâche à compléter, des ressources utiles, et un lien pour soumettre ta solution.<br>
            🇬🇧 You will receive one email per day with your task, helpful resources, and a link to submit your solution.
        </p>

        <p>
            🇫🇷 C’est totalement gratuit, et c’est pour nous tous, pour apprendre ensemble et faire grandir la communauté Python.<br>
            🇬🇧 This is 100% free and made for all of us, to learn together and grow the Python community.
        </p>

        <hr>

        <h3>🗓️ PyCon Togo 2025 — Inscriptions</h3>
        <p>
            🇫🇷 Les inscriptions pour <strong>PyCon Togo 2025</strong> ouvrent demain à <strong>16h30min GMT</strong>. Les places sont limitées, alors pense à réserver rapidement.<br>
            Visite : <a href="https://pycontg.pytogo.org">https://pycontg.pytogo.org</a><br><br>
            🇬🇧 <strong>PyCon Togo 2025 registration</strong> opens tomorrow at <strong>4:30 PM UTC</strong>. Places are limited — save your spot quickly!<br>
            Visit: <a href="https://pycontg.pytogo.org">https://pycontg.pytogo.org</a>
        </p>

        <hr>

        <h3>🎙️ Canal vocal #workshop sur Discord</h3>
        <p>
            🇫🇷 Chaque jour, des échanges et mini-ateliers auront lieu dans le canal vocal <code>#workshop</code> sur Discord. Tu peux y poser des questions, écouter ou partager ta solution.<br>
            🇬🇧 Join our <code>#workshop</code> voice channel daily on Discord to share, ask, or just listen in.
        </p>

        <p>
            👉 <a href="https://pytogo.org/discord">Rejoins notre serveur Discord ici</a>
        </p>

        <hr>

        <h3>💬 Besoin d’aide ? / Need help?</h3>
        <p>
            🇫🇷 Si tu as la moindre question, n’hésite pas à :
            <ul>
                <li>💬 poser dans le serveur Discord (channel <code>#challenge-30jours</code>)</li>
                <li>📧 envoyer un email à <a href="mailto:challenge@pytogo.org">challenge@pytogo.org</a></li>
                <li>📞 appeler ou écrire sur WhatsApp : +228 98 27 38 05 ou +228 98 77 66 82</li>
            </ul>
            🇬🇧 If you have any question, feel free to:
            <ul>
                <li>💬 ask in the Discord server (<code>#challenge-30jours</code> channel)</li>
                <li>📧 email us at <a href="mailto:challenge@pytogo.org">challenge@pytogo.org</a></li>
                <li>📞 call or WhatsApp: +228 98 27 38 05 or +228 98 77 66 82</li>
            </ul>
        </p>

        <hr>

        <p style="font-size: 0.95em;">
            🇫🇷 Merci d’être avec nous dans cette aventure. On apprend ensemble, on grandit ensemble.<br>
            🇬🇧 Thank you for being part of this journey. We learn together, we grow together.
        </p>

        <p style="font-size: 0.9em;">
            -- Wachiou BOURAIMA (Wasiu Ibrahim)
        </p>
    </div>
    """

    return subject, body



def get_submission_instruction_email(first_name, fr_title, en_title, fr_link, en_link):
    subject = "Soumets ta solution pour le jour 1 | Submit your Day 1 solution"

    body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 650px; margin: auto; line-height: 1.6; color: #333;">
        <h2>🇫🇷 Bonjour {first_name},<br>🇬🇧 Hello {first_name},</h2>

        <p>
            🇫🇷 Le <strong>Challenge 30 Jours Python</strong> a officiellement commencé hier à minuit. Nous espérons que tout se passe bien pour toi !<br>
            🇬🇧 The <strong>30 Days of Python Challenge</strong> officially started last night at midnight. We hope it’s going well for you!
        </p>

        <h3>📌 Tâche du jour 1 — Day 1 Task</h3>
        <p>
            🇫🇷 <strong>{fr_title}</strong><br>
            <a href="{fr_link}">{fr_link}</a><br><br>
            🇬🇧 <strong>{en_title}</strong><br>
            <a href="{en_link}">{en_link}</a>
        </p>

        <hr>

        <h3>📝 Soumettre ta solution — Submit your solution</h3>
        <p>
            🇫🇷 Tu peux soumettre ta solution ici : <a href="https://challenge.pytogo.org/submit">https://challenge.pytogo.org/submit</a><br>
            🇬🇧 You can submit your solution here: <a href="https://challenge.pytogo.org/submit">https://challenge.pytogo.org/submit</a>
        </p>

        <p>
            🇫🇷 À l’arrivée sur la page, il te suffit de :
            <ul>
                <li>Entrer l'adresse e-mail utilisée lors de l'inscription</li>
                <li>Indiquer le lien vers ta solution (Drive, GitHub, Replit, etc.) ou écrire ton code directement</li>
                <li>(Optionnel) Ajouter une brève explication</li>
            </ul>
            🇬🇧 On the page, simply:
            <ul>
                <li>Enter your registration email</li>
                <li>Provide a link to your code (Drive, GitHub, Replit, etc.) or write it directly</li>
                <li>(Optional) Add a brief explanation</li>
            </ul>
        </p>

        <p><strong>📸 Capture du formulaire — Form Screenshot</strong></p>
        <p>
            <img src="https://challenge.pytogo.org/static/images/submit_form_fr.png" alt="Aperçu formulaire de soumission" style="width: 100%; max-width: 600px; border: 1px solid #ccc; border-radius: 8px;">
        </p>

        <hr>

        <p>
            🇫🇷 Il n'y a pas de bonne ou de mauvaise façon de faire, l’essentiel est de participer régulièrement !<br>
            🇬🇧 There is no "perfect" way to submit — the most important thing is to stay consistent!
        </p>

        <p style="font-size: 0.9em;">
            -- L'équipe Python Togo / Python Togo Team
        </p>
    </div>
    """

    return subject, body


def new_daily_challenge_email(first_name, day_number, fr_title, en_title, fr_link, en_link):

        subject = f"[Jour {day_number} / Day {day_number}] {fr_title} | {en_title} – Tu progresses bien ! Keep going!"

        body = f"""
           <div style="font-family: Arial, sans-serif; font-size: 16px; line-height: 1.6; color: #333; padding: 20px;">

            <!-- VERSION FRANÇAISE -->
            <p><strong>🇫🇷 Version française</strong></p>

            <h2>Bonjour {first_name}, Hello!</h2>
            
            <h2 style="color: #1a73e8;">Challenge Python – Jour { day_number }</h2>

            <p>
                Félicitations pour ta participation continue au <strong>Challenge 30 Jours de Python</strong> ! Tu fais un travail formidable, et on t’encourage à continuer ainsi.
            </p>

            <p>
                Si tu n’as pas encore soumis toutes les tâches, ce n’est pas grave. Tu peux toujours le faire à ton rythme. L’objectif est de <strong>progresser régulièrement</strong>, pas d’aller vite.
            </p>

            <p>
                Nous avons remarqué que plusieurs personnes rencontrent des difficultés avec GitHub. Pas d’inquiétude ! Voici quelques ressources utiles pour apprendre à utiliser GitHub :
            </p>

            <ul>
                
                <li><a href="https://www.youtube.com/watch?v=hPfgekYUKgk" target="_blank">Les Tutos - Débuter avec Git et Github en 30 min</a></li>
                <li><a href="https://rtavenar.github.io/tuto-git/book.pdf" target="_blank">Tutoriel d'introduction à git</a></li>
                <li><a href="https://www.youtube.com/watch?v=X3KCX99I2pQ&t=94s" target="_blank">Débutant : Comment utiliser GitHub</a></li>
                <li><a href="https://www.youtube.com/watch?v=4o9qzbssfII" target="_blank">Git & GitHub pour les débutants (vidéo YouTube)</a></li>
                <li><a href="https://learngitbranching.js.org/?locale=fr_FR" target="_blank">Learn Git Branching (interactif)</a></li>
                <li><a href="https://www.atlassian.com/fr/git/tutorials/what-is-git" target="_blank">Guide Git par Atlassian</a></li>
            </ul>

            <p>
                Rejoins aussi le canal <code><a href="https://discord.com/channels/1367111367102042112/1367111370176331836" target="_blank">#workshop/a></code> sur Discord pour poser tes questions et suivre les sessions en direct.
            </p>

            <p>
                📌 Astuce : Si tu suis la version française du document, pense à consulter la version anglaise aussi. Cela peut t’aider à mieux comprendre.
            </p>

            <p>
                <strong>Ressources du jour :</strong><br>
                ➤ <a href="{ fr_link }" target="_blank">Document du jour { day_number } (FR)</a><br>
                ➤ <a href="{ en_link }" target="_blank">Document of the day { day_number } (EN)</a>
            </p>

            <p>
                <strong>Soumettre ta solution :</strong><br>
                <a href="https://challenge.pytogo.org/submit" target="_blank">https://challenge.pytogo.org/submit</a><br>
                Tu peux y coller ton code ou envoyer un lien (GitHub, Replit, Google Drive…).
            </p>

            <p>
                Pour toute question :<br>
                📧 challenge@pytogo.org<br>
                📱 +228 98 27 38 05 / +228 92 55 59 87
            </p>

            <hr style="margin: 40px 0;">

            <!-- ENGLISH VERSION -->
            <p><strong>🇬🇧 English version</strong></p>

            <h2>Hello {first_name}, Bonjour!</h2>
            <h2 style="color: #1a73e8;">Python Challenge – Day { day_number }</h2>

            <p>
                Congratulations on your progress in the <strong>30-Day Python Challenge</strong>! You're doing an amazing job – keep going!
            </p>

            <p>
                If you haven’t submitted all the tasks yet, no worries. You can still do it. The key is <strong>consistency</strong>, not speed.
            </p>

            <p>
                We've noticed that some participants are facing issues with GitHub. Don’t worry! Here are some helpful resources to learn GitHub:
            </p>

            <ul>
                <li><a href="https://www.youtube.com/watch?v=RGOj5yH7evk" target="_blank">Git & GitHub for Beginners (YouTube)</a></li>
                <li><a href="https://learngitbranching.js.org/" target="_blank">Learn Git Branching (Interactive)</a></li>
                <li><a href="https://www.atlassian.com/git/tutorials/what-is-git" target="_blank">Git Tutorial by Atlassian</a></li>
            </ul>

            <p>
                Join our <code><a href="https://discord.com/channels/1367111367102042112/1367111370176331836" target="_blank">#workshop</a></code> channel on Discord to ask questions or attend live sessions.
            </p>

            <p>
                📌 Tip: If you read the document in French and find inconsistencies, refer to the English version for clarification.
            </p>

            <p>
                <strong>Today's resources:</strong><br>
                ➤ <a href="{ fr_link }" target="_blank">French Document</a><br>
                ➤ <a href="{ en_link }" target="_blank">English Document</a>
            </p>

            <p>
                <strong>Submit your solution:</strong><br>
                <a href="https://challenge.pytogo.org/submit" target="_blank">https://challenge.pytogo.org/submit</a><br>
                You can paste your code or send a link (GitHub, Replit, Google Drive…).
            </p>

            <p>
                For support:<br>
                📧 challenge@pytogo.org<br>
                📱 +228 98 27 38 05 / +228 98 77 66 82
            </p>

        </div>
        """
        return subject, body


def new_new_mail_daily_mail(participant, day_number, fr_title, en_title, fr_link, en_link):
    previous_day = day_number - 1
    subject = f"[Jour {day_number}] / [Day {day_number}] Bravo pour ta régularité 👏 | Rendez-vous au workshop du 31 juillet !"
    subject = f"[Jour {day_number}]/ [Day {day_number}] {participant} Ensemble on avance ! 🌍 | Bilan et discussion le 31 juillet sur Discord"


    html = f"""
    <div style="font-family:Arial, sans-serif; line-height:1.6; font-size:16px; color:#333; max-width:650px; margin:auto;">
        <p>Bonjour {participant},</p>

        <p>👏 <strong>Félicitations</strong> pour ta constance jusqu’au <strong>jour {previous_day}</strong> du challenge ! Tu fais déjà un excellent travail. Continue à ton rythme, l’important c’est la régularité et la compréhension.</p>

        <hr style="border:none; border-top:1px solid #ddd;"/>

        <h3>📌 Jour {day_number} – Nouvelle tâche</h3>
        <p>➡️ Titre de la tâche : <strong>{fr_title}</strong></p>
          ➤ <a href="{ fr_link }" target="_blank">Document du jour { day_number } (FR)</a><br>
          ➤ <a href="{ en_link }" target="_blank">Document of the day { day_number } (EN)</a>
        <p style="color:#d14;"><strong>🔁 Pour éviter toute confusion liée à la traduction, pense à consulter aussi la version anglaise !</strong></p>

        <hr style="border:none; border-top:1px solid #ddd;"/>

        <h3>📝 Soumettre ta solution</h3>
        <p>Soumets ta solution ici : <a href="https://challenge.pytogo.org/submit">https://challenge.pytogo.org/submit</a></p>
        <p>Tu peux soit <strong>coller ton code</strong>, soit envoyer un <strong>lien vers ton fichier ou ton dépôt GitHub</strong>.</p>

        <h4>📘 Ressources GitHub</h4>
        <ul>
            <li><a href="https://www.youtube.com/watch?v=hPfgekYUKgk">Les Tutos - Débuter avec Git et Github en 30 min</a></li>
            <li><a href="https://www.youtube.com/watch?v=X3KCX99I2pQ&t=94s">Les Tutos - Git et Github pour les débutants</a></li>
            <li><a href="https://openclassrooms.com/fr/courses/2342361-gerez-votre-code-avec-git-et-github">OpenClassrooms - Git & GitHub (FR)</a></li>
            <li><a href="https://rtavenar.github.io/tuto-git/book.pdf" target="_blank">Tutoriel d'introduction à git</a></li>
            <li><a href="https://www.youtube.com/watch?v=X3KCX99I2pQ&t=94s" target="_blank">Débutant : Comment utiliser GitHub</a></li>
            <li><a href="https://www.youtube.com/watch?v=4o9qzbssfII" target="_blank">Git & GitHub pour les débutants (vidéo YouTube)</a></li>
            <li><a href="https://learngitbranching.js.org/?locale=fr_FR" target="_blank">Learn Git Branching (interactif)</a></li>
            <li><a href="https://www.atlassian.com/fr/git/tutorials/what-is-git" target="_blank">Guide Git par Atlassian</a></li>
        </ul>

        <hr style="border:none; border-top:1px solid #ddd;"/>

        <h3>📢 Partage ton progrès</h3>
        <p>Publie ton avancée sur <strong>LinkedIn, Twitter/X ou Facebook</strong> pour inspirer d’autres personnes.</p>
        <p>Utilise les hashtags suivants :</p>
        <code>#PyConTogo2025 #PythonTogo #Challenge30DaysOfPython #PythonTogoChallenge #30DaysOfPythonWithPythonTogo</code>

        <hr style="border:none; border-top:1px solid #ddd;"/>

        <h3>🎙️ Discord & Workshop</h3>
        <p>Tu peux rejoindre notre serveur Discord ici : <a href="https://pytogo.org/discord">https://pytogo.org/discord</a></p>
        <p>Pose tes questions dans le canal vocal <strong>#workshop</strong>.</p>
        <p><strong>📅 Jeudi 31 juillet</strong> en soirée, nous ferons un grand atelier vocal : bilan de la première semaine et explication complète des tâches passées. Ne rate pas ça !</p>

        <hr style="border:none; border-top:1px solid #ddd;"/>

        <p style="text-align:center; color:#666;">🇬🇧 English version below</p>

        <hr style="border:none; border-top:1px dashed #bbb;"/>

        <p>Hello dear {participant},</p>

        <p>👏 <strong>Congrats</strong> for reaching <strong>Day {previous_day}</strong> of the challenge! You're doing great. Keep moving at your own pace — it’s all about consistency and learning.</p>

        <h3>📌 Day {day_number} – New Task</h3>
        <p>➡️ Task title: <strong>{en_title}</strong></p>
          ➤ <a href="{ fr_link }" target="_blank">Document du jour { day_number } (FR)</a><br>
          ➤ <a href="{ en_link }" target="_blank">Document of the day { day_number } (EN)</a>
        <p style="color:#d14;"><strong>🔁 Please check the English version to avoid any typo issues in the translated French version.</strong></p>

        <h3>📝 Submit your work</h3>
        <p>Submit here: <a href="https://challenge.pytogo.org/submit">https://challenge.pytogo.org/submit</a></p>
        <p>You can either <strong>paste your code</strong> or share a <strong>link to a file or GitHub repo</strong>.</p>

        <h4>📘 GitHub Resources</h4>
        <ul>
            <li><a href="https://www.youtube.com/watch?v=RGOj5yH7evk">Git and GitHub for Beginners - Crash Course</a></li>
            <li><a href="https://docs.github.com/en/get-started/quickstart">GitHub Docs (EN)</a></li>
        </ul>

        <h3>📣 Share your progress</h3>
        <p>Post on <strong>LinkedIn, Twitter/X or Facebook</strong> to show what you’ve learned.</p>
        <p>Use these hashtags:</p>
        <code>#PyConTogo2025 #PythonTogo #Challenge30DaysOfPython #PythonTogoChallenge #30DaysOfCodeWithPythonTogo</code>

        <h3>🎙️ Discord & Workshop</h3>
        <p>Join our Discord server here: <a href="https://pytogo.org/discord">https://pytogo.org/discord</a></p>
        <p>Use the <strong><a href="https://discord.com/channels/1367111367102042112/1367111370176331836">#workshop</a></strong> voice channel to ask your questions.</p>
        <p><strong>📅 On Thursday, July 31</strong> in the evening, we’ll host a big community workshop to review the first week and explain all past tasks in detail. Don’t miss it!</p>

        <p style="margin-top:30px;">💙 <em>The Python Togo Team</em><br/>
        📩 challenge@pytogo.org</p>
    </div>
    """
    return subject, html
    

def recap_mail_day(participant, fr_link, en_link):
    subject = f"📚 [Récapitulatif semaine 1] / [Week 1 Recap] – Merci d’avoir suivi le live !"
    
    html = f"""
    <div style="font-family:Arial, sans-serif; font-size:16px; line-height:1.6; color:#333; max-width:650px; margin:auto;">
        <p>Bonjour {participant},</p>

        <p>Merci à tous ceux qui ont participé au <strong>workshop de ce soir</strong> sur Discord. 🙌</p>
        <p>Si tu l’as manqué, pas grave ! Tu peux continuer à ton rythme.</p>

        <p>Voici le document récapitulatif de la première semaine :</p>
        <ul>
            <li><a href="{fr_link}" target="_blank">📄 Document récapitulatif (FR)</a></li>
            <li><a href="{en_link}" target="_blank">📄 Recap document (EN)</a></li>
        </ul>

        <p>Bonne lecture et bonne continuation dans le challenge ! 🚀</p>

        <hr style="border:none; border-top:1px dashed #bbb;"/>
        <p style="text-align:center; color:#666;">🇬🇧 English version below</p>
        <hr style="border:none; border-top:1px dashed #bbb;"/>

        <p>Hello {participant},</p>

        <p>Thanks to everyone who joined today's <strong>Discord live workshop</strong> 🙌</p>
        <p>If you missed it, don’t worry — you can continue on your own pace.</p>

        <p>Here is the recap document for the first week:</p>
        <ul>
            <li><a href="{fr_link}" target="_blank">📄 Récapitulatif (FR)</a></li>
            <li><a href="{en_link}" target="_blank">📄 Recap Document (EN)</a></li>
        </ul>

        <p>Keep going strong! 💪</p>

        <p style="margin-top:30px;">💙 <em>The Python Togo Team</em><br/>
        📩 challenge@pytogo.org</p>
    </div>
    """
    
    return subject, html


def daily_task_mail_after_live(participant, day_number, fr_title, en_title, fr_link, en_link):
    subject = f"[Jour {day_number}] / [Day {day_number}] – Nouvelle mission & lien de soumission 🧠💻"

    html = f"""
    <div style="font-family:Arial, sans-serif; font-size:16px; line-height:1.6; color:#333; max-width:650px; margin:auto;">
        <p>Bonjour {participant},</p>

        <p>Le challenge continue, et chaque ligne de code te rapproche de ton prochain niveau ! 🚀</p>
        <p>Que tu aies assisté au live du 31 juillet ou non, l'important est de progresser à ton rythme.</p>

        <h3>📌 Tâche du jour {day_number}</h3>
        <p><strong>{fr_title}</strong></p>
        <ul>
            <li><a href="{fr_link}" target="_blank">📄 Document du jour (FR)</a></li>
            <li><a href="{en_link}" target="_blank">📄 Document of the day (EN)</a></li>
        </ul>

        <p>✅ Une fois ta solution prête, pense à la soumettre ici :  
        <a href="https://challenge.pytogo.org/submit" target="_blank">https://challenge.pytogo.org/submit</a></p>


        <p style="color:#d14;"><strong>👉 Consulte la version anglaise pour éviter les erreurs de traduction.</strong></p>

        <p>Continue à coder, à apprendre et à te dépasser. On est avec toi 💪🏽</p>

        <hr style="border:none; border-top:1px dashed #bbb;"/>
        <p style="text-align:center; color:#666;">🇬🇧 English version below</p>
        <hr style="border:none; border-top:1px dashed #bbb;"/>

        <p>Hello {participant},</p>

        <p>The challenge goes on — and every line of code brings you closer to mastery! 💡</p>
        <p>Whether or not you joined the July 31st live session, what matters most is learning at your own pace.</p>

        <h3>📌 Day {day_number} Task</h3>
        <p><strong>{en_title}</strong></p>
        <ul>
            <li><a href="{fr_link}" target="_blank">📄 Document du jour (FR)</a></li>
            <li><a href="{en_link}" target="_blank">📄 Document of the day (EN)</a></li>
        </ul>

        <p>✅ Once you're done, submit your solution here:  
        <a href="https://challenge.pytogo.org/submit" target="_blank">https://challenge.pytogo.org/submit</a></p>

        <p>📺 You can also catch up on past sessions and tutorials on our YouTube channel:  
        <a href="https://www.youtube.com/@PythonTogo" target="_blank">https://www.youtube.com/@PythonTogo</a></p>

        <p style="color:#d14;"><strong>👉 Check the English version to avoid translation issues.</strong></p>

        <p>Keep coding, keep learning, and keep showing up. We're cheering you on! 👏🏽</p>

        <p style="margin-top:30px;">💙 <em>The Python Togo Team</em><br/>
        📩 challenge@pytogo.org</p>
    </div>
    """
    return subject, html


def daily_mail_with_task(participant, day_number, fr_title, en_title, fr_link, en_link):
    previous_day = day_number - 1
    subject = f"[Jour {day_number}] / [Day {day_number}] – Nouvelle tâche + Félicitations 🎉"

    html = f"""
    <div style="font-family:Arial, sans-serif; font-size:16px; line-height:1.6; color:#333; max-width:650px; margin:auto;">
        <p>Bonjour {participant},</p>

        <h2>🎉 Bravo ! Tu as validé le jour {previous_day} du challenge</h2>
        <p>Peu importe si tu as tout compris ou non, l’important est d’avancer à ton rythme.  
        Ceux qui ont compris : continuez sur cette lancée 💪.  
        Ceux qui ont eu des difficultés : pas de souci, reviens sur les jours précédents et pose tes questions dans notre  
        <a href="https://discord.com/channels/1367111367102042112/1367111370176331836" target="_blank">channel #workshop</a> sur Discord.</p>

        <hr style="border:none; border-top:1px solid #ddd;"/>

        <h3>📌 Jour {day_number} – Nouvelle tâche</h3>
        <p><strong>{fr_title}</strong></p>
        ➤ <a href="{fr_link}" target="_blank">Document du jour {day_number} (FR)</a><br>
        ➤ <a href="{en_link}" target="_blank">Document of the day {day_number} (EN)</a>
        <p style="color:#d14;"><strong>Pense à consulter aussi la version anglaise pour éviter toute confusion liée à la traduction.</strong></p>

        <hr style="border:none; border-top:1px solid #ddd;"/>

        <h3>🎟️ PyCon Togo 2025</h3>
        <p>L’événement aura lieu le <strong>23 août 2025</strong> !  

        <p>🙏 Nous nous excusons pour notre calme de ces derniers jours — nous sommes en plein dans les préparatifs du PyCon Togo.  
        Mais ne t’inquiète pas, il y aura une <strong>grande session récapitulative</strong> avant la fin du challenge.</p>

        <p>🚀 Continue comme ça et on se retrouve bientôt !</p>

        <hr style="border:none; border-top:1px dashed #bbb;"/>
        <p style="text-align:center; color:#666;">🇬🇧 English version below</p>
        <hr style="border:none; border-top:1px dashed #bbb;"/>

        <p>Hello {participant},</p>

        <h2>🎉 Well done! You completed day {previous_day} of the challenge</h2>
        <p>It doesn’t matter if you’ve understood everything yet — what matters is making steady progress.  
        If you understood: keep it up 💪.  
        If you had difficulties: no problem, revisit previous days and ask your questions in our  
        <a href="https://discord.com/channels/1367111367102042112/1367111370176331836" target="_blank">#workshop channel</a> on Discord.</p>

        <hr style="border:none; border-top:1px solid #ddd;"/>

        <h3>📌 Day {day_number} – New task</h3>
        <p><strong>{en_title}</strong></p>
        ➤ <a href="{fr_link}" target="_blank">Document du jour {day_number} (FR)</a><br>
        ➤ <a href="{en_link}" target="_blank">Document of the day {day_number} (EN)</a>
        <p style="color:#d14;"><strong>Make sure to check the English version to avoid translation confusion.</strong></p>

        <hr style="border:none; border-top:1px solid #ddd;"/>

        <h3>🎟️ PyCon Togo 2025</h3>
        <p>The event will take place on <strong>August 23, 2025</strong>!  

        <p>🙏 Sorry for being a bit quiet lately — we’ve been busy preparing for PyCon Togo.  
        But don’t worry, we’ll have a <strong>big recap session</strong> before the end of the challenge.</p>

        <p>🚀 Keep it up and see you soon!</p>

        <p style="margin-top:30px;">💙 <em>The Python Togo Team</em><br/>
        📩 challenge@pytogo.org</p>
    </div>
    """
    return subject, html


def mail_day_23(participant, day_number, fr_title, en_title, fr_link, en_link):
 
    subject = f"[Day {day_number} / Jour {day_number}] 🚀 You're almost there! | Plus que quelques pas!"

    html = f"""
    <div style="font-family:Arial, sans-serif; line-height:1.6; font-size:16px; color:#333; max-width:650px; margin:auto;">
        <p>Hi {participant},</p>

        <p>🚀 <strong>Only one week left!</strong> You’ve made it to <strong>Day {day_number}</strong>, and the finish line is almost in sight.  
        Every single step you’ve taken has brought you closer — and this journey is proof of your dedication. Keep that momentum going! 💪</p>

        <p>⚠️ Don’t forget: <strong>Task 30</strong> will be special. Be ready for it!</p>

        <h3>📌 Today's Task</h3>
        <p><strong>{en_title}</strong></p>
        ➤ <a href="{fr_link}" target="_blank">Document du jour (FR)</a><br>
        ➤ <a href="{en_link}" target="_blank">Document of the day (EN)</a>

        <h3>📚 Keep going after the challenge</h3>
        <p>Join <strong>Genepy</strong> under Python Togo to continue learning and taking on new challenges:</p>
        <p><a href="https://genepy.org/teams/pythontogo">https://genepy.org/teams/pythontogo</a></p>

        <h3>💬 Stay connected</h3>
        <p>Ask questions and exchange ideas in our <strong>#workshop</strong> channel on Discord:</p>
        <p><a href="https://discord.com/channels/1367111367102042112/1367111370176331836">Direct link to #workshop</a></p>

        <hr style="border:none; border-top:1px dashed #bbb; margin:30px 0;"/>
        <p style="text-align:center; color:#666;">🇫🇷 Version française ci-dessous</p>
        <hr style="border:none; border-top:1px dashed #bbb;"/>

        <p>Salut {participant},</p>

        <p>🚀 <strong>Encore une semaine !</strong> Tu es arrivé jusqu’au <strong>jour {day_number}</strong> et la ligne d’arrivée est tout proche.  
        Chaque pas que tu as fait t’a rapproché de la fin — cette aventure prouve ta persévérance. Continue sur ta lancée ! 💪</p>

        <p>⚠️ N’oublie pas : <strong>la tâche 30</strong> sera spéciale. Sois prêt !</p>

        <h3>📌 Tâche du jour</h3>
        <p><strong>{fr_title}</strong></p>
        ➤ <a href="{fr_link}" target="_blank">Document du jour (FR)</a><br>
        ➤ <a href="{en_link}" target="_blank">Document of the day (EN)</a>

        <h3>📚 Continue après le challenge</h3>
        <p>Rejoins <strong>Genepy</strong> sous Python Togo pour continuer à apprendre et relever de nouveaux défis :</p>
        <p><a href="https://genepy.org/teams/pythontogo">https://genepy.org/teams/pythontogo</a></p>

        <h3>💬 Reste connecté</h3>
        <p>Pose tes questions et échange avec la communauté dans notre channel <strong>#workshop</strong> sur Discord :</p>
        <p><a href="https://discord.com/channels/1367111367102042112/1367111370176331836">Lien direct vers #workshop</a></p>

        <p style="margin-top:30px;">💙 <em>The Python Togo Team</em><br/>
        📩 challenge@pytogo.org</p>
    </div>
    """
    return subject, html

def mail_day_bilingual(participant, day_number, fr_title, en_title, fr_link, en_link):
    previous_day = day_number - 1
    subject = f"[Jour {day_number}] / [Day {day_number}] On continue | Nouvelle tâche + Vercel + Discord"

    html = f"""
    <div style="font-family:Arial, sans-serif; line-height:1.6; font-size:16px; color:#333; max-width:680px; margin:auto;">
        <!-- ====== FRANÇAIS ====== -->
        <p>Bonjour {participant},</p>

        <p>Tu as tenu jusqu’au <strong>jour {previous_day}</strong>. On garde le cap : l’objectif n’est pas de dépasser les autres, mais de <strong>te dépasser toi-même</strong>, un pas après l’autre.</p>

        <hr style="border:none; border-top:1px solid #ddd; margin:18px 0;"/>

        <h3 style="margin:0 0 8px;">Jour {day_number} — Tâche du jour</h3>
        <p style="margin:0 0 6px;">Titre (FR) : <strong>{fr_title}</strong></p>
        <p style="margin:0 0 10px;">Titre (EN) : <strong>{en_title}</strong></p>
        <p style="margin:0 0 6px;">➤ <a href="{fr_link}" target="_blank">Document du jour {day_number} (FR)</a></p>
        <p style="margin:0 0 10px;">➤ <a href="{en_link}" target="_blank">Document of the day {day_number} (EN)</a></p>
        <p style="color:#a11; margin:6px 0 0;"><strong>Astuce :</strong> pour éviter d’éventuelles coquilles de traduction, jette aussi un œil à la version anglaise.</p>

        <h3 style="margin:18px 0 8px;">Déploiement</h3>
        <p>Besoin de mettre en ligne ? Essaie <strong>Vercel</strong> (offre gratuite) :</p>
        <p style="margin:0 0 6px;">• Site : <a href="https://vercel.com" target="_blank">https://vercel.com</a></p>
        <p style="margin:0 0 10px;">• Docs utiles : <a href="https://matiasfuentes.hashnode.dev/how-to-deploy-a-flask-web-app-on-vercel" target="_blank">https://matiasfuentes.hashnode.dev/how-to-deploy-a-flask-web-app-on-vercel</a> &nbsp;|&nbsp; <a href="https://vercel.com/guides" target="_blank">Guides</a></p>

        <h3 style="margin:18px 0 8px;">Soumettre ta solution</h3>
        <p>Dépose ton travail ici : <a href="https://challenge.pytogo.org/submit" target="_blank">https://challenge.pytogo.org/submit</a><br/>
        (colle le code ou partage un lien — fichier ou dépôt GitHub)</p>

        <h3 style="margin:18px 0 8px;">Discord & séance questions</h3>
        <p>Des questions ? Passe sur le serveur Discord :</p>
        <p style="margin:0 0 6px;">• Rejoindre : <a href="https://pytogo.org/discord" target="_blank">https://pytogo.org/discord</a></p>
        <p style="margin:0 0 10px;">• Accès direct au canal <strong>#workshop</strong> : <a href="https://discord.com/channels/1367111367102042112/1367111370176331836" target="_blank">ouvrir le canal</a></p>

        <h3 style="margin:18px 0 8px;">PyCon Togo 2025</h3>
        <p><strong>Samedi 23 août 2025</strong> — reste à l’écoute pour la confirmation finale du lieu.<br/>
        Lieu provisoire : <strong>Amphithéâtre de l’UniPod, Université de Lomé</strong>.</p>

        <hr style="border:none; border-top:1px dashed #bbb; margin:22px 0;"/>
        <p style="text-align:center; color:#666; margin:0;">🇬🇧 English version below</p>
        <hr style="border:none; border-top:1px dashed #bbb; margin:12px 0 18px;"/>

        <!-- ====== ENGLISH ====== -->
        <p>Hello {participant},</p>

        <p>You’ve stayed consistent up to <strong>Day {previous_day}</strong>. Keep your eyes on the goal: not to outpace others, but to <strong>outgrow yesterday’s you</strong>.</p>

        <h3 style="margin:0 0 8px;">Day {day_number} — Today’s task</h3>
        <p style="margin:0 0 6px;">Title (FR): <strong>{fr_title}</strong></p>
        <p style="margin:0 0 10px;">Title (EN): <strong>{en_title}</strong></p>
        <p style="margin:0 0 6px;">➤ <a href="{fr_link}" target="_blank">Document du jour {day_number} (FR)</a></p>
        <p style="margin:0 0 10px;">➤ <a href="{en_link}" target="_blank">Document of the day {day_number} (EN)</a></p>
        <p style="color:#a11; margin:6px 0 0;"><strong>Note:</strong> if you read the French doc, cross-check the English version to avoid possible translation typos.</p>

        <h3 style="margin:18px 0 8px;">Deployment</h3>
        <p>Ship it with <strong>Vercel</strong> (free tier available):</p>
        <p style="margin:0 0 6px;">• Site: <a href="https://vercel.com" target="_blank">https://vercel.com</a></p>
        <p style="margin:0 0 10px;">• Docs: <a href="https://matiasfuentes.hashnode.dev/how-to-deploy-a-flask-web-app-on-vercel" target="_blank">https://matiasfuentes.hashnode.dev/how-to-deploy-a-flask-web-app-on-vercel</a> &nbsp;|&nbsp; <a href="https://vercel.com/guides" target="_blank">Guides</a></p>

        <h3 style="margin:18px 0 8px;">Submit your work</h3>
        <p>Submit here: <a href="https://challenge.pytogo.org/submit" target="_blank">https://challenge.pytogo.org/submit</a><br/>
        (paste code or share a link — file or GitHub repo)</p>

        <h3 style="margin:18px 0 8px;">Discord & live help</h3>
        <p>Need help? Join the Discord server:</p>
        <p style="margin:0 0 6px;">• Join: <a href="https://pytogo.org/discord" target="_blank">https://pytogo.org/discord</a></p>
        <p style="margin:0 0 10px;">• Direct access to <strong>#workshop</strong>: <a href="https://discord.com/channels/1367111367102042112/1367111370176331836" target="_blank">open channel</a></p>

        <h3 style="margin:18px 0 8px;">PyCon Togo 2025</h3>
        <p><strong>Saturday, August 23, 2025</strong> — final confirmation coming soon.<br/>
        Provisional venue: <strong>UniPod amphitheatre, University of Lomé</strong>.</p>

        <p style="margin-top:24px; color:#555;">— The Python Togo Team</p>
    </div>
    """
    return subject, html




if __name__ == "__main__":
    participants = get_some_thing("participants")
    if not participants:
        print("No participants found.")
    
    subject, body = daily_mail_with_task("Participant", 1, "Titre de la tâche", "Task Title", "https://example.com/fr", "https://example.com/en")
    send_email_with_or_without_attachment(body, subject, receiver_email="wachioubouraima56@gmail.com")
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
                
                