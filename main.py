import os
import numpy as np
import json
import warnings
import nltk
import time
import speech_recognition as sr
import whisper

from utils import (
    fake_patient, 
    format_speech_output, 
    get_verification_summary, 
    initialize_correction_system,
    validate_input_context,
    enhance_accent_handling,
    handle_confirmation
)
from llm import initialize_llm
from stt import initialize_enhanced_recognition, listen_for_speech
from tts import initialize_tts, handle_speech_output
from verification import InsuranceVerification
from flow import ConversationFlowManager, verify_patient


def main():
    try:
        nltk.download('punkt_tab', quiet=True)
        warnings.filterwarnings('ignore')
        office_name = "Everest Dental Clinic"

        patient = fake_patient()
        verification = InsuranceVerification(office_name, patient)
        flow_manager = ConversationFlowManager(verification, patient)
        faiss_index, correction_df = initialize_correction_system()
        
        if faiss_index is None or correction_df is None:
            print("Could not initialize correction system")
            return

        tts = initialize_tts()
        recognizer = initialize_enhanced_recognition()
        queue = []
        play_obj = None

        if not hasattr(whisper, 'cached_model'):
            whisper.cached_model = whisper.load_model("base")

        # Display patient information
        print("\nPatient Information Available:")
        print(f"Name: {patient['first_name']} {patient['last_name']}")
        print(f"DOB: {patient['date_of_birth']}")
        print(f"Member ID: {patient['member_number']}")
        print(f"Insurance: {patient['insurance_provider']}")
        print("\nStarting in Patient Information Phase\n")

        # Initial greeting
        initial_message = (
            f"Hi, this is an assistant from {office_name}. "
            f"I'm calling about our patient {patient['first_name']} {patient['last_name']}. "
            f"Would you mind helping me verify insurance coverage?"
        )
        initial_message = format_speech_output(initial_message)
        wav = np.array(tts.tts(text=initial_message))
        play_obj = handle_speech_output(queue, play_obj, wav, recognizer, None)

        # Main conversation loop
        while True:
            try:
                with sr.Microphone() as source:
                    # Handle interruptions during speech
                    if play_obj and play_obj.is_playing():
                        if recognizer.get_energy() > 3000:
                            play_obj.stop()
                            queue.clear()
                            audio = listen_for_speech(recognizer, source, play_obj)
                            if audio:
                                text = recognizer.recognize_whisper(audio, model="base")
                                print(f"Heard during speech: {text}")
                                continue

                    # Process queued audio
                    while len(queue) > 0:
                        if play_obj and play_obj.is_playing():
                            time.sleep(0.1)
                            continue
                        play_obj = queue.pop(0).play()

                    # Listen for speech
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = listen_for_speech(recognizer, source, play_obj)
                    
                    if not audio:
                        continue

                    # Process speech input
                    text = recognizer.recognize_whisper(audio, model="base")
                    print(f"Original input: {text}")
                    
                    # Check for quit command
                    if text.lower() == "quit":
                        verification_summary = get_verification_summary(verification)
                        print("\nVerification Summary:")
                        for category, data in verification_summary['collected'].items():
                            if data:
                                print(f"\n{category.upper()}:")
                                for field, value in data.items():
                                    print(f"  {field}: {value}")
                        
                        with open('verification_results.json', 'w') as f:
                            json.dump(verification_summary, f, indent=2)
                        print("\nResults saved to verification_results.json")
                        break

                    # First check if input needs correction in context
                    validation_result = validate_input_context(text, verification, flow_manager, faiss_index, correction_df)
                    
                    if validation_result["needs_correction"]:
                        print(f"Input needs correction: {validation_result['reason']}")
                        # Pass current context when calling enhance_accent_handling
                        current_context = "insurance verification" if flow_manager.verification_started else "patient information"
                        correction_result = enhance_accent_handling(text, faiss_index, correction_df, verification, current_context)
                        
                        if correction_result['needs_confirmation']:
                            confirmation_msg = correction_result['confirmation_msg']
                            formatted_confirmation = format_speech_output(confirmation_msg)
                            print(f"Seeking confirmation: {formatted_confirmation}")
                            wav = np.array(tts.tts(text=formatted_confirmation))
                            play_obj = handle_speech_output(queue, play_obj, wav, recognizer, source)
                            
                            confirmation_audio = listen_for_speech(recognizer, source, play_obj)
                            if confirmation_audio:
                                confirmation = recognizer.recognize_whisper(confirmation_audio, model="base")
                                if handle_confirmation(confirmation):
                                    text = correction_result['corrected']
                                    print(f"Confirmation received, using corrected input: {text}")
                                else:
                                    print("Correction rejected, asking for rephrasing")
                                    error_msg = "Could you please rephrase that?"
                                    wav = np.array(tts.tts(text=error_msg))
                                    play_obj = handle_speech_output(queue, play_obj, wav, recognizer, source)
                                    continue
                        else:
                            text = correction_result['corrected']
                            print(f"Auto-corrected input: {text}")
                    else:
                        print("Input was valid, proceeding without correction")

                    # Process response and get next action
                    print(f"Processing response: {text}")
                    response, is_transition = flow_manager.process_response(text, verification)
                    print(f"Response: {response}, Is transition: {is_transition}")
                    
                    if response:
                        formatted_response = format_speech_output(response)
                        print(f"\nResponding: {formatted_response}")
                        wav = np.array(tts.tts(text=formatted_response))
                        play_obj = handle_speech_output(queue, play_obj, wav, recognizer, source)

                    # Check for verification completion
                    verification_summary = get_verification_summary(verification)
                    if verification_summary['status'] == 'complete':
                        print("\nVerification Complete!")
                        print("\nFinal Verification Summary:")
                        for category, data in verification_summary['collected'].items():
                            if data:
                                print(f"\n{category.upper()}:")
                                for field, value in data.items():
                                    print(f"  {field}: {value}")
                        
                        completion_message = "All verification information has been collected. Thank you for your help.\
                        Have a nice day. Bye Bye."
                        wav = np.array(tts.tts(text=completion_message))
                        play_obj = handle_speech_output(queue, play_obj, wav, recognizer, source)
                        break

            except sr.UnknownValueError:
                print("Could not understand audio input")
                error_msg = "I'm sorry, I couldn't understand that. Could you please repeat?"
                wav = np.array(tts.tts(text=error_msg))
                play_obj = handle_speech_output(queue, play_obj, wav, recognizer, source)
                
            except Exception as e:
                print(f"Error in main loop: {str(e)}")
                error_msg = "I encountered an error. Could you please rephrase that?"
                wav = np.array(tts.tts(text=error_msg))
                play_obj = handle_speech_output(queue, play_obj, wav, recognizer, source)

    finally:
        if play_obj and play_obj.is_playing():
            play_obj.stop()
        if hasattr(whisper, 'cached_model'):
            del whisper.cached_model

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("\nSession ended")

