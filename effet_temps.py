import numpy as np
import soundfile as sf
import librosa

def accel(audio_data, multiple, debut,fin):
    '''Prend en argument un fichier audio en .wav, le coefficient d'acceleration (2 pour accelerer la musique 2 fois). Crée (ou écrase) le fichier accleré entre le frame debut, jusqu'au frame fin en .wav sous le nom new_name'''
    data_final = np.concatenate((audio_data[0:debut],audio_data[debut:fin:multiple],audio_data[fin:len(audio_data)]))
    return data_final

#accel("country.wav","country_accel.wav",2,0,220000)
