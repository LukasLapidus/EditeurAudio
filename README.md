## Intitulé du projet : Réalisation d'un site d'édition mp3

## Notes pour la DTY

Pour que le site soit opérationnel il sera nécessaire d'avoir intallé MySQL Community Server et de créer une base de données spécifique sur son propre environnement comme indiqué dans la fin du README.

Le module librosa utilisé pour modifier les fichiers audio n'est pas stable et renvoie une erreur à l'importation. Ainsi, s'il est possible de se balader sur le site, d'upload des musiques ainsi que des samples, la musique ne sera pas modifiée et aucun fichier ne pourra être lu/exporté dans le dossier downloads.

S'il s'avère que le module librosa fonctionne, essayez de lancer 'app_avec_musique.py' et non 'app.py'.

Lorsque que l'on arrive sur le site, un identifiant et un mot de passe sont demandés. Cependant, le système d'authentification n'est pas opérationnel, il est donc inutile d'essayer de se connecter (il n'y a pas de système d'enregistrement). Il en va de même pour l'onglet connexion.

## Membres du groupe
* Alexandre Belot
* Timothée Dunglas
* Lukas Lapidus
* Arnaud Petit
* Salomé Fournel
* Alex Richaume

## MVP 
Créer une interface utilisateur sur internet avec des fonctionnalités de base (mise à disposition d'un fichier audio, bouton play/pause, option "accélérer")

## Etapes de réalisation du projet
* Création du git et des branches pour les membres du groupe
* Création des différentes pages du site internet (HTML+Flask+MySQL (base de données de fichiers audio))
* Ajout des différentes fonctionnalités

## A faire avant de lancer le site : Création de la base de donnée
* Créer la base de donnée dans MySQL "editeur_audio" avec la commande suivante : 'CREATE DATABASE editeur_audio; 
* Pour pouvoir se connecter à la base de donnée, il faut aussi modifier le champ mot de passe dans app.py (ligne 23) pour qu'il corresponde a celui que vous avez choisi.

## Tuto
Afin de profiter pleinement de votre expérience au sein de ce site d'édition mp3, exécutez le fichier app.py en ayant installé au préalable les librairies suivantes :
* Flask
* wtForm
* Soundfile
* Librosa (Update : Se télécharge correctement mais ne s'importe pas correctement lors de la compilation)
* OS
* Flask_mysqldb
* numpy
* matplotlib

Voici un bref résumé des fonctionnalités que propose ce site.
* Mise à disposition d'une musique de test et d'une base de données vide qui pourra contenir différentes pistes que vous voudrez charger ainsi que leurs caractéristiques.

Dans l'onglet mix, différentes fonctions d'édition vous seront proposées :
* Un bouton pour accélérer votre piste (vous pourrez sélectionner le facteur d'accélération)
* Un bouton pour superposer à la piste des sons de batterie (Funk et/ou Blues) en rythme
* Un bouton pour amplifier les percussions de la piste d'origine
* Un bouton pour sélectionner et couper une partie de la piste initiale
