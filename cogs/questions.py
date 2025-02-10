from http.client import responses
from os import name
import discord
from discord.ext import commands
from discord import app_commands
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import io
from datetime import datetime
import textwrap
import re

class MandataireQuestionnaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_questions = {}
        self.questions = [
            "Quel est votre prénom ?",
            "Quel est votre numéro de téléphone ?",
            "Quel est votre email professionnel ?",
            "Quelle est l'adresse complète du bien ?",
            "Quel est le prix net vendeur ?",
            "Quelle est la commission d'agence ?",
            "Quel est le prix FAI (Frais d'Agence Inclus) ?",
            "Quelle est la surface habitable  ?",
            "Quelle est la surface du terrain ?",
            "Quel est le nombre de pièces ?",
            "Quel est le DPE (Diagnostic de Performance Énergétique) ?",
            "Quelles sont les informations spécifiques ? (cave, parking, etc.)",
            "Y a-t-il des travaux à prévoir ? Si oui, lesquels ?",
            "Quel est le montant des charges annuelles ?",
            "Quelle est la taxe foncière ?"
        ]
        print(f"✓ Initialized with {len(self.questions)} questions")

    @app_commands.command(
        name="questionnaire",
        description="Démarrer le questionnaire immobilier"
    )
    @app_commands.checks.has_permissions(send_messages=True)
    async def questionnaire(self, interaction: discord.Interaction):
        try:
            user_id = interaction.user.id
            if not self.questions:
                raise ValueError("No questions configured")
            
            self.active_questions[user_id] = {
                'current_question': 0,
                'responses': [],
                'name': None
            }
            
            await interaction.response.send_message(
                f"Question 1/{len(self.questions)}: {self.questions[0]}\n" +
                "Veuillez répondre à cette question de manière précise.",
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Une erreur est survenue: {str(e)}",
                ephemeral=True
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        if user_id not in self.active_questions:
            return

        session = self.active_questions[user_id]
        current_q = session['current_question']

        try:
            if current_q == 0:
                if not re.match("^[a-zA-Z]+$", message.content):
                    await message.channel.send("❌ Le prénom ne peut contenir que des lettres sans espaces.")
                    return
                
                session['name'] = message.content
            elif current_q == 1:
                if not re.match(r"^\+?(\d{1,3})?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}$", message.content):
                    await message.channel.send("❌ Le numéro de téléphone est invalide. Veuillez entrer un numéro valide.")
                    return

            elif current_q == 2:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", message.content):
                    await message.channel.send("❌ L'email est invalide. Veuillez entrer un email valide.")
                    return

            elif current_q == 3:
                if not message.content.strip():
                    await message.channel.send("❌ L'adresse ne peut pas être vide.")
                    return

            elif current_q == 4 or current_q == 5 or current_q == 6:
                if not re.match(r"^\d{1,3}(?:[\s,]\d{3})*$", message.content):
                    await message.channel.send("❌ Le prix doit être un nombre entier avec des espaces (ex: 800 000).")
                    return

            elif current_q == 7 or current_q == 8:
                if not message.content.isdigit():
                    await message.channel.send("❌ La surface doit être un nombre entier.")
                    return
# factoriser le code 
            session['responses'].append(message.content)

            if current_q < len(self.questions) - 1:
                session['current_question'] += 1
                await message.channel.send(
                    f"Question {current_q + 2}/{len(self.questions)}: {self.questions[current_q + 1]}\n"
                    "Veuillez répondre à cette question de manière précise."
                )
            else:
                pdf_file = await self.generate_pdf(session['name'], session['responses'])

                if pdf_file:
                    embed = discord.Embed(
                        title=f"Fiche technique immobilière - {session['name']}",
                        color=discord.Color.green(),
                        description="✅ La fiche technique a été générée avec succès."
                    )

                    # Add summary fields
                    for i, (q, r) in enumerate(zip(self.questions, session['responses'])):
                        embed.add_field(
                            name=f"Q{i+1}: {q}",
                            value=f"R: {r[:100]}{'...' if len(r) > 100 else ''}",
                            inline=False
                        )

                    await message.channel.send(
                        content="Voici votre fiche technique :",
                        embed=embed,
                        file=pdf_file
                    )
                else:
                    await message.channel.send("❌ Une erreur est survenue lors de la génération du PDF.")

                del self.active_questions[user_id]

        except Exception as e:
            await message.channel.send(f"❌ Une erreur est survenue: {str(e)}")
            del self.active_questions[user_id]

    
    async def generate_pdf(self, name, responses):
       # Création du buffer pour le fichier PDF
        buffer = io.BytesIO()

        # Définir la taille de la page en lettre
        width, height = letter

        # Création du canvas pour dessiner sur le PDF
        c = canvas.Canvas(buffer, pagesize=letter)

        try:


            # Logo de l'agence (optionnel) - à décommenter si tu veux ajouter un logo
            c.drawImage("Efficity.png", 450, height - 50, width=100, height=50)

            # En-tête du document
            c.setFont("Times-Roman", 16)
            c.drawString(100, height - 50, "MANDAT DE VENTE IMMOBILIÈRE")
            c.setFont("Times-Roman", 10)
            c.drawString(100, height - 70, "Document Confidentiel - Usage Professionnel")

            # Informations de l'agence
            c.setFont("Times-Bold", 12)
            c.drawString(100, height - 100, "Agence Immobilière XYZ")
            c.setFont("Times-Roman", 10)
            c.drawString(100, height - 120, "Adresse: 123 Rue de l'Immobilier, Paris")
            c.drawString(100, height - 135, "Tél: 01 23 45 67 89 | Email: contact@xyz-immobilier.fr")

            # Espacement
            c.drawString(100, height - 160, "-" * 50)

            # Informations sur le mandataire
            c.setFont("Times-Bold", 12)
            c.drawString(100, height - 180, f"Mandataire: {name}")
            c.setFont("Times-Roman", 10)
            c.drawString(100, height - 200, f"Date: {datetime.now().strftime('%d/%m/%Y')}")

            # Espacement
            c.drawString(100, height - 220, "-" * 50)

            # Informations du bien immobilier
            c.setFont("Times-Bold", 12)
            c.drawString(100, height - 240, "Informations sur le bien immobilier")
            c.setFont("Times-Roman", 10)
            c.drawString(100, height - 260, f"Adresse du bien: {responses[3]}")  # Réponse à l'adresse
            c.drawString(100, height - 275, f"Prix net vendeur: {responses[4]} €")  # Réponse au prix net
            c.drawString(100, height - 290, f"Commission d'agence: {responses[5]} %")  # Réponse à la commission
            c.drawString(100, height - 305, f"Prix FAI: {responses[6]} €")  # Réponse au prix FAI
            c.drawString(100, height - 320, f"Surface habitable: {responses[7]} m²")  # Réponse à la surface habitable
            c.drawString(100, height - 335, f"Surface du terrain: {responses[8]} m²")  # Réponse à la surface du terrain
            c.drawString(100, height - 350, f"Nombre de pièces: {responses[9]}")  # Réponse au nombre de pièces
            c.drawString(100, height - 365, f"DPE: {responses[10]}")  # Réponse au DPE
            c.drawString(100, height - 380, f"Travaux à prévoir: {responses[12]}")  # Réponse aux travaux

            # Espacement
            c.drawString(100, height - 400, "-" * 50)

            # Informations supplémentaires
            c.setFont("Times-Bold", 12)
            c.drawString(100, height - 420, "Informations supplémentaires")
            c.setFont("Times-Roman", 10)
            c.drawString(100, height - 440, f"Charges annuelles: {responses[13]} €")  # Réponse aux charges annuelles
            c.drawString(100, height - 455, f"Taxe foncière: {responses[14]} €")  # Réponse à la taxe foncière

            # Footer
            c.setFont("Times-Italic", 8)
            c.drawString(100, 30, "Document généré automatiquement - Confidentiel")
            c.drawString(100, 20, f"Date d'édition: {datetime.now().strftime('%d/%m/%Y à %H:%M')}")

            c.save()
            buffer.seek(0)

            # Générer le fichier pour Discord
            return discord.File(fp=buffer, filename=f"mandat_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")

        except Exception as e:
            print(f"Erreur PDF: {str(e)}")
            return None

    
async def setup(bot):
    await bot.add_cog(MandataireQuestionnaire(bot))
