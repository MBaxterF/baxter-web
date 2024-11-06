import openpyxl
import openai

from html_reader import HTMLReader

url = input("Saisissez l'URL d'1 page web: ")
audit = []

html = HTMLReader()
html.read_url(url)

page = html.render()

if len(page.get_data_tags("Mon compte")) > 0:
    audit.append(["Connexion", "Vérifier que l'accès au compte du client fonctionne"])

if len(page.get_data_tags("Recherche")) > 0:
    audit.append(["Recherche", "Valider la pertinence des articles recherchés"])

if len(page.get_data_tags("Contact")) > 0:
    audit.append(["Contact", "Lancer l'appel depuis le bouton de contact"])

if len(page.get_data_tags("subscribe")) > 0:
    audit.append(["Inscription", "Tester le fonctionnement de l'inscription"])

if len(page.get_data_tags("*")) > 0:
    audit.append(["Champs de formulaire requis", "Marquer tous les champs obligatyoires du formulaire d'inscription"])

if len(page.get_data_tags("search")) == 0:
    audit.append(["Barre de recherche absente", "Vérifier que l'utilisateur peut lancer une recherche"])

if len(page.get_data_tags("h1")) == 0:
    audit.append(["Titre manquant", "Vérifier la présence du titre"])

sheets = openpyxl.load_workbook(url.split('/')[2].replace('.', '_') + "_plan.xlsx")
sheet = sheets['Audit technique']

prompt = "Donne moi un exemple d'audit technique"

for i in range(len(audit)):
    sheet['B' + str(i + 12)] = "X"
    sheet['C' + str(i + 12)] = audit[i][0]
    sheet['D' + str(i + 12)] = audit[i][1]

sheets.save(url.split('/')[2].replace('.', '_') + "_plan.xlsx")