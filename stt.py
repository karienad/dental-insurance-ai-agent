import speech_recognition as sr
import whisper
import numpy as np
from scipy import signal
import simpleaudio as sa
import time

def initialize_enhanced_recognition():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 3000
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.dynamic_energy_ratio = 1.5
    recognizer.pause_threshold = 1.0
    
    def remove_noise(audio_data):
        audio_array = np.frombuffer(audio_data.frame_data, dtype=np.int16)
        nyquist = 22050 / 2
        low = 300 / nyquist
        high = 3000 / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        filtered_audio = signal.filtfilt(b, a, audio_array)
        return filtered_audio
    
    recognizer.remove_noise = remove_noise
    return recognizer

def listen_for_speech(recognizer, source, play_obj=None):
    print("\nListening...")
    if play_obj and play_obj.is_playing():
        play_obj.stop()
        
    try:
        full_audio_data = b''
        is_speaking = False
        
        while True:
            try:
                audio = recognizer.listen(source, timeout=0.5)
                if len(audio.get_raw_data()) > 0:
                    is_speaking = True
                    full_audio_data += audio.get_raw_data()
                
                if is_speaking:
                    try:
                        recognizer.listen(source, timeout=1.0)
                        break
                    except sr.WaitTimeoutError:
                        continue
            except sr.WaitTimeoutError:
                if full_audio_data:
                    break
                continue
                
        if not full_audio_data:
            return None
            
        return sr.AudioData(full_audio_data, audio.sample_rate, audio.sample_width)
        
    except Exception as e:
        print(f"Error in listening: {str(e)}")
        return None