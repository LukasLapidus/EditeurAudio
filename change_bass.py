import librosa

def change_bass(data,coef_bass):
    '''Prend un argument un array de data, le coef d'importance des basses voulues et celui des harmonies
    Renvoie un array de data avec les poids voulus'''
    data_harmonic,data_bass = librosa.effects.hpss(data)
    if coef_bass<=1:
        return(coef_bass*data_bass + data_harmonic)
    if coef_bass>1:
        return(data_bass + data_harmonic/coef_bass)