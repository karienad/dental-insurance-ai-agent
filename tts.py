from TTS.api import TTS
import numpy as np
import simpleaudio as sa
from datetime import time

def initialize_tts():
    return TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

def handle_speech_output(queue, play_obj, wav_data, recognizer, source):
    try:
        wav_norm = wav_data * (32767 / max(0.01, np.max(np.abs(wav_data))))
        audio_obj = sa.WaveObject(wav_norm.astype(np.int16), 1, 2, 22050)
        
        if not play_obj or not play_obj.is_playing():
            play_obj = audio_obj.play()
            
            while play_obj.is_playing():
                try:
                    if recognizer.get_energy() > 3000:
                        play_obj.stop()
                        queue.clear()
                        return None
                    time.sleep(0.1)
                except:
                    continue
                    
            return play_obj
        else:
            queue.append(audio_obj)
            return play_obj
            
    except Exception as e:
        print(f"Error in speech output: {str(e)}")
        return play_obj