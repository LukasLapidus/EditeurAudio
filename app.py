from flask import Flask, render_template, flash, request, redirect, url_for, abort
from wtforms import Form, StringField, validators, IntegerField, BooleanField, TextAreaField, PasswordField, SelectField
import soundfile as sf
from flask_mysqldb import MySQL
import os 

#import librosa                             # module librosa non fonctionnel
#from effet_temps import accel              # idem
#from cut import cut                        # idem
#from change_bass import change_bass        # idem
#from percussion import percu               # idem
#from sample_unique import sample_unique    # idem


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Lukas13986@&'   # Lié à la base de donnée sur l'ordinateur
app.config['MYSQL_DB'] = 'editeur_audio'        # Nom de la base de données créée et activée
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = './uploads'       # Emplacement des fichiers upload sur le site


# init MYSQL
mysql = MySQL(app)


# Classe pour l'authentification
class UtilisateurForm(Form):
    utilisateur = StringField("Nom d'utilisateur")
    mdp = StringField('Mot de passe')


# Classe définissant les musiques
class MusicForm(Form):
    titre = StringField('titre', [validators.Length(min=1, max=200)])
    artiste = StringField('artiste', [validators.Length(min=1, max=100)])


#logf=False
# Classe définissant les samples (bruitages, percussions, ...)
class SampleForm(Form):
    nom = StringField('nom', [validators.Length(min=1, max=200)])


# Classe qui réunit les infos pour le mixage
class Validate_form(Form):
    original_filename = StringField('original_filename', [validators.Length(min=1, max=30)])
    titre = StringField('titre', [validators.Length(min=1, max=30)])
    filename = StringField('filename', [validators.Length(min=1, max=30)])
    genre = StringField('genre', [validators.Length(min=1, max=30)])
    speed = IntegerField('speed')
    bass = IntegerField('bass')
    sampling_rate = IntegerField('sampling_rate')
    drum_funk = StringField('drum_funk')
    drum_blues= StringField('drum_blues')
    tone = IntegerField('tone')
    sample_id=StringField('sample_id',[validators.Length(min=1, max=200)])
    insert_time=StringField('insert_time',[validators.Length(min=1, max=200)])
    inst_debut=StringField('inst_debut',[validators.Length(min=1, max=200)])
    inst_fin=StringField('inst_fin',[validators.Length(min=1, max=200)])


# Index
@app.route('/inscription')
def signup():
    return render_template('inscription.html')


# Page d'accueil avec système de connexion partiel
@app.route('/',methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS USER (id INT(11) AUTO_INCREMENT PRIMARY KEY, login VARCHAR(200), mdp VARCHAR(200), create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
    cur.execute("CREATE TABLE IF NOT EXISTS sample (id INT(11) AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(255), doc VARCHAR(100) )")
    cur.execute("CREATE TABLE IF NOT EXISTS musique (id INT(11) AUTO_INCREMENT PRIMARY KEY, titre VARCHAR(255), artiste VARCHAR(100), doc VARCHAR(100))")
    mysql.connection.commit()
    cur.close()
    form = UtilisateurForm(request.form)
    if request.method == 'POST' and form.validate():
        utilisateur = form.utilisateur.data
        mdp = form.mdp.data
        
        

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        print("SELECT COUNT(*) FROM USER WHERE login = '{}' AND mdp = '{}'".format(utilisateur,mdp))
        cur.execute("SELECT COUNT(*) FROM USER WHERE login = '{}' AND mdp = '{}'".format(utilisateur,mdp))
        res=cur.fetchone()
        if res["COUNT(*)"] >= 1:
            print("ok")
            logf=True
        else:
            print("probleme poto")
        print(logf)

    return render_template('index.html', form=form)


# Description
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


# Page de transition permettant de choisir sa musique à partir d'une base de donnée
# On peut également upload des musiques depuis cette page
@app.route('/database')
def liste():
    cur = mysql.connection.cursor()

    result=cur.execute("SELECT id, titre, artiste, doc FROM musique ")
    items=cur.fetchall()
     
    cur.close()

    if result > 0:
        return render_template('musique_db.html',items=items)
    else :
        flash("La base de données est vide")
        return render_template('musique_db.html')


# Même chose pour les samples   
@app.route('/sample')
def liste_sample():
    cur = mysql.connection.cursor()

    result=cur.execute("SELECT id, nom FROM sample ")
    items=cur.fetchall()
     
    cur.close()

    if result > 0:
        return render_template('sample_db.html',items=items)
    else :
        flash("La base de Donnée est vide")
        return render_template('sample_db.html')


# Page qui permet de remplir les données pour la base de donnée, on identifie la musique
@app.route('/database/add_music/<filename>', methods=['GET', 'POST'])
def add_music(filename):
    form = MusicForm(request.form)
    if  request.method =='POST':
        titre = form.titre.data
        artiste = form.artiste.data
        doc = filename
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Musique(titre, artiste, doc) VALUES(%s, %s, %s)", (titre, artiste, doc))
        mysql.connection.commit()
        cur.close()
        flash("Musique ajoutée à la base de donnée")
        return redirect(url_for('liste'))
    
    return render_template('ajout_musique.html')


# Même chose pour les samples
@app.route('/add_sample/<filename>', methods=['GET', 'POST'])
def add_sample(filename):
    form = SampleForm(request.form)
    if  request.method =='POST':
        nom = form.nom.data
        doc = filename
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Sample(nom, doc) VALUES( %s, %s)", (nom, doc))
        mysql.connection.commit()
        cur.close()
        flash("Sample ajoutée à la base de donnée")
        return redirect(url_for('liste_sample'))
    
    return render_template('ajout_sample.html')


# Page intermediare qui permet l'upload
@app.route('/upload_music',methods=['POST'])
def upload_music():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Pas de musique envoyée")
            return redirect(url_for('liste'))
        file = request.files['file']
        if file :
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect(url_for('add_music', filename=filename))
    return ('upload.html')


# Même chose pour sample
@app.route('/upload_sample',methods=['POST'])
def upload_sample():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Pas de sample envoyée")
            return redirect(url_for('appliquer_changement'))
        file = request.files['file']
        if file :
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect(url_for('add_sample', filename=filename))
    return ('upload.html')


# Méthode pour supprimer des musiques de la base de donnée
@app.route('/delete_music/<string:id>', methods=['POST'])
def delete_music(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM musique WHERE id=%s',[id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('liste'))


# Même chose pour les samples
@app.route('/delete_sample/<string:id>', methods=['POST'])
def delete_sample(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM sample WHERE id=%s',[id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('liste_sample'))


# Page de mix global
@app.route('/mix/<string:id>', methods=['GET', 'POST'])
def appliquer_changements(id):
    form = Validate_form(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT id, nom FROM sample ")
    objets=cur.fetchall()
    cur.close()

    # Dictionnaire pour envoyer les infos a la page html
    dict={}
    dict['items']=objets
    dict['form']=form
    dict['tempo']=form

    # On récupere les infos depuis notre base de donnée pour les afficher
    cur = mysql.connection.cursor()
    result=cur.execute("SELECT titre,artiste,doc FROM musique WHERE id=%s ",[id])
    item=cur.fetchone()
    cur.close()
    
    dict['doc']= item['doc']
    dict['titre']=item['titre']
    dict['id']=id
    dict['tempo'] = 0
    if request.method == 'POST':    
        
        
        
        original_filename = item['doc']
        filename = form.filename.data
        #-----#audio_data, sampling_rate = librosa.load('uploads/'+original_filename)
        #-----#dict['tempo']=int(librosa.beat.tempo(audio_data,sampling_rate)[0])

        # Evite les erreurs lors de la 1ere connexion
        if filename == ''  :
            return render_template('mix.html',**dict)
        
        # On recupere les donnée du formulaire
        genre = form.genre.data
        speed = form.speed.data
        bass = form.bass.data
        tone = form.tone.data
        sampling_rate = form.sampling_rate.data
        drum_funk = form.drum_funk.data
        drum_blues = form.drum_blues.data
        inst_debut=form.inst_debut.data
        inst_fin=form.inst_fin.data
        insert_time=form.insert_time.data
        sample_id=form.sample_id.data

        # Si les champs du formulaire sont vides, il faut quand même donner des valeurs acceptables
        if inst_debut == '':inst_debut='0'
        if inst_fin == '' : inst_fin = str(-1/sampling_rate)
        
        print(drum_blues)
        print(drum_funk)
        
        cur = mysql.connection.cursor()
        result=cur.execute("SELECT doc FROM sample WHERE id=%s ",[id])
        nom_file=cur.fetchone()
        cur.close()

        # Changements sur le fichier audio

        """ # Partie obsolète à cause du module librosa qui ne fonctionne plus
        #-----#data_final=cut(audio_data,int(float(inst_debut)*sampling_rate), int(float(inst_fin)*sampling_rate))
        if drum_funk == "activate" : 
            #-----#data_final = percu(data_final,son_percu="./uploads/Batterie_funk_1.wav")
        if drum_blues == "activate":
            #-----#data_final = percu(data_final,son_percu="./uploads/Batterie_blues_1.wav")
        if insert_time != "":
            #-----#data_final = sample_unique(data_final,"./uploads"+nom_file['doc'],insert_time)
        if speed != 1:
            #-----#data_final = librosa.effects.time_stretch(data_final, speed)
        if tone != 0:
            #-----#data_final = librosa.effects.pitch_shift(data_final, sampling_rate, tone)
        if bass != 1:
            #-----#data_final= change_bass(data_final,bass)

        #-----#sf.write('uploads/'+filename, data_final, sampling_rate)
        """

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Musique(titre, artiste, doc) VALUES(%s, %s, %s)", (item['titre'], item['artiste'], filename))
        mysql.connection.commit()
        cur.close()


        # Rajouter les validators dans les formulaires
        flash('Changements appliqués à la musique', 'success')
        return redirect(url_for('appliquer_changements', id=id))
    return render_template('mix.html', **dict)

if __name__ == '__main__':
    app.run(debug=True)
