import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import essentia
from essentia.standard import EqloudLoader, PredominantPitchMelodia


global FRAME_SIZE
global HOPE_SIZE

FRAME_SIZE = 2048
HOPE_SIZE = 1024
DEGREE = 3


def melody_xtraction(sound_path):
    # Load audiofile with equal-loudness filter
    loader = EqloudLoader(filename=sound_path, sampleRate=44100)
    audio = loader()

    # Extract the pitch curve, input raw audio
    audio_dur = len(audio) / 44100.0

    pitch_extractor = PredominantPitchMelodia(frameSize=FRAME_SIZE, hopSize=HOPE_SIZE)
    pitch_values, pitch_confidence = pitch_extractor(audio)

    # Pitch on frames. Compute frame time positions
    pitch_times = np.linspace(0.0, audio_dur, len(pitch_values))

    #print(len(pitch_values), pitch_values)

    return (pitch_values, pitch_confidence, pitch_times)

def plot_contours(where, pitch_values, pitch_confidence, pitch_times, i=0):
    plt.rcParams['figure.figsize'] = (15, 6)
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(pitch_times, pitch_values)
    axarr[0].set_title('estimated pitch [Hz]')
    axarr[1].plot(pitch_times, pitch_confidence)
    axarr[1].set_title('pitch confidence')
    if where == 'show':
        plt.show()
    elif where == 'save':
        myplot = plt.gcf()
        myplot.savefig('/mnt/DATA/thesis/img/contours/contour_' + str(i))
    elif where == 'none':
        pass
    else:
        raise Exception("Not valid input.")

# filtering
def delete_zeroes(pitch_values):
    smooth_pitch_values = np.delete(pitch_values, np.argwhere(pitch_values < 30))
    smooth_pitch_times = np.array(range(len(smooth_pitch_values)))
    return smooth_pitch_values, smooth_pitch_times

# smoothing
def predict_abstract_contour(x,y,degree=DEGREE):
    ''' Use Linear Regression to make a smooth melodic line, that shows the abstract movement.
    Returns:
        mel_coefs (list): A list with the coefficients of the function.
        y_pred: Function for plotting
    '''
    x = x.reshape(-1, 1) # preprocess for the model
    poly = PolynomialFeatures(degree=degree) # features

    # Fit the curve.
    X_poly = poly.fit_transform(x)
    poly.fit(X_poly, y)
    lr = LinearRegression()
    lr.fit(X_poly, y)
    y_pred = lr.predict(X_poly)

    mel_coefs = (lr.coef_).tolist()
    return mel_coefs, y_pred


def mx_for_all_audiofiles(sound_paths):
    ''' Extract pitch conntours for all the audiofiles.
    '''
    pvl, pcl, ptl = [], [], []
    for pos, path in enumerate(sound_paths):
        pv, pc, pt = melody_xtraction(path)
        #plot_contours('save', pv, pc, pt, sound_paths.split('.')[0]
        pvl.append(pv)
        pcl.append(pc)
        ptl.append(pt)
    return (pvl, pcl, ptl)

def final_contour(path):
     pv,_,_ = melody_xtraction(path)
     s_pitch_values, s_pitch_times = delete_zeroes(pv)
     times_length = len(s_pitch_times)
     coefs,_ = predict_abstract_contour(s_pitch_times, s_pitch_values)
     return coefs, times_length


def final_contours_all(sound_paths):
    ''' Compute smoothed contours for all the audiofiles.
    '''
    times_length_list = []
    coefs_list = []
    for pos, path in enumerate(sound_paths):
        pv,_,_ = melody_xtraction(path)
        s_pitch_values, s_pitch_times = delete_zeroes(pv)
        times_length_list.append(len(s_pitch_times))
        coefs,_ = predict_abstract_contour(s_pitch_times, s_pitch_values)
        coefs_list.append(coefs)
    print(" ..contours extracted \n ------------------------------------------------")
    return coefs_list, times_length_list

if __name__ == '__main__':
    #sound = '/mnt/DATA/thesis/code_extra/filter-similarity/testsounds/495947__phonosupf__viola-glissando-10.wav'
    #sound = '/mnt/DATA/thesis/code/mirlc2/sounds/Tin Whistle, Flutter, A (H1).ogg'
    sound = '/mnt/DATA/thesis/537875__ghostwiremedia__vibraphone-scale.wav'
    pv, pc, pt = melody_xtraction(sound)
    plot_contours('save', pv, pc, pt)
    print(len(pv))
    print('done')
