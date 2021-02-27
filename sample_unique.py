import numpy as np
import soundfile as sf
import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt

def sample_unique(data_audio,sample,date):
    '''Prend en argument deux fichiers audio en .wav, Crée (ou écrase) le fichier concaténé entre le frame debut, jusqu'au frame fin en .wav sous le nom new_name'''
    
    data_sample,sr2 = librosa.load(sample)
    sr1 = sr2

    Nb_frames_audio = len(data_audio)
    Nb_frames_sample = len(data_sample)

    frame_debut = int(date*sr1) # date en seconde

    data_final = np.copy(data_audio)
    
    if frame_debut + Nb_frames_sample > Nb_frames_audio:
        print("erreur de date fournit pour le sample")
        return None

    for i in range(Nb_frames_sample):
        data_final[frame_debut+i] = data_audio[frame_debut+i] + data_sample[i]


    return data_final



