import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io
import wave

def listen_continuous():
    r = sr.Recognizer()
    samplerate = 16000
    duration = 5  # listens in 5 second chunks
    
    print("Listening continuously... Press Ctrl+C to stop")
    
    while True:
        try:
            # Record 5 seconds
            audio_data = sd.rec(int(duration * samplerate),
                                samplerate=samplerate,
                                channels=1, dtype='int16')
            sd.wait()
            
            # Convert to wav
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(samplerate)
                wf.writeframes(audio_data.tobytes())
            wav_buffer.seek(0)
            
            # Recognize
            with sr.AudioFile(wav_buffer) as source:
                audio = r.record(source)
            
            text = r.recognize_google(audio)
            print("You said:", text)
            
            # Stop word
            if "stop" in text.lower():
                print("Stopping...")
                break
                
        except sr.UnknownValueError:
            print("...") # silence or unclear
        except sr.RequestError:
            print("No internet")
        except KeyboardInterrupt:
            print("Stopped by user")
            break

listen_continuous()