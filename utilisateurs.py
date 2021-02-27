from wtforms import BooleanField,Form, StringField, TextAreaField, PasswordField, validators, IntegerField, SelectField
from __init__ import db




######################################################
# Inutilisée
######################################################







class UtilisateurForm(Form):
    utilisateur = StringField("Nom d'utilisateur")
    mdp = StringField('Mot de passe')



