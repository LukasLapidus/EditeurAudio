import numpy as np
import soundfile as sf
import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt

def percu(data_audio,son_percu):
    '''Prend en argument deux fichiers audio en .wav, Crée (ou écrase) le fichier concaténé entre le frame debut, jusqu'au frame fin en .wav sous le nom new_name'''

    data_percu,sr2 = librosa.load(son_percu)
    sr1 = sr2

    tempo_audio, beat_frames1 = librosa.beat.beat_track(y=data_audio, sr=sr1)
    tempo_percu, beat_frames2 = librosa.beat.beat_track(y=data_percu, sr=sr2)


    sr_modifie = int(sr2*tempo_percu/tempo_audio)
    data_new_percu,sr_modifie = librosa.load(son_percu,sr=sr_modifie)

    tempo_new_percu, beat_frames3 = librosa.beat.beat_track(y=data_new_percu, sr=sr2)


    Nb_frames_audio = len(data_audio)
    Nb_frames_percu = len(data_percu)
    Nb_frames_new_percu = len(data_new_percu)


    premier_zero_audio = premier_zero(data_audio)


    data_final = np.zeros(Nb_frames_audio)
    
    for i in range( premier_zero_audio , Nb_frames_audio ):
        data_final[i] = data_audio[i] + data_new_percu[(i-premier_zero_audio) % Nb_frames_new_percu]/1.5


    return data_final



def premier_zero(data):
    n = len(data)
    i = 0
    while i < n and abs(data[i]) <= 0.02:
        i+=1
    return i

