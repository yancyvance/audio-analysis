from pydub import AudioSegment
from scipy.io import wavfile

import numpy as np
import pandas as pd
import librosa
import librosa.display
import io


class Recording:
    
    def __init__(self, filename=None, other_recording=None, sample_rate=None, as_scipy=None):
        """ Ideally mp3 files but can be another object. """
        if filename:
            self.mp3_file = AudioSegment.from_mp3(filename)
            self.channels = 1 #self.mp3_file.channels
            self.sample_rate = self.mp3_file.frame_rate
            self.mono = self.mp3_file.split_to_mono()[0] # first channel only?
            self.as_numpy = None
            self.as_scipy = None

            # populate information
            self.fill_numpy(False)
            self.fill_scipy()
        elif other_recording:
            self.mp3_file = other_recording.mp3_file
            self.channels = other_recording.channels
            self.sample_rate = sound_rate # passed as resampled
            self.mono = other_recording.mono # TODO
            self.as_numpy = other_recording.as_numpy # TODO
            self.as_scipy = as_scipy # only this is implemented
        
    
    def get_chunk(self, start, end):
        """ Needs a Timedelta information for start and end. """
        s = start.total_seconds() * 1000
        e = end.total_seconds() * 1000 + 1 # since it is exclusive
        
        return self.mp3[s:e]
    
    
    def fill_numpy(self, normalized=False):
        y = np.array( self.mono.get_array_of_samples() )
        
        if self.channels == 2:
            y = y.reshape( (-1, 2) )
           
        if normalized:
            self.as_numpy = np.float32(y) / 2**15
        else:
            self.as_numpy = y
            
            
    def fill_scipy(self):
        self.as_scipy = librosa.util.buf_to_float(self.as_numpy)
        
        
        
    def resample(self, target_sr):
        # create object
        resampled_scipy = librosa.resample(self.as_scipy, orig_sr=self.sample_rate, target_sr=target_sr)
        
        # return a copy
        return Recording(self, sample_rate=target_sr, resampled_scipy)
    
    
    def get_bytes(self):
        # needs the scipy
        file = io.BytesIO()
        wavfile.write(file, self.sample_rate, self.as_scipy)
        file.seek(0)
        return file
        


