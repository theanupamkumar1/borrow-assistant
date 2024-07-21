import speech_recognition as sr
import pyaudio
import wave
import os
from typing import Optional
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

class SpeechRecognizer:
    def __init__(self, language: str = "en-IN", wake_word: str = "chhotu"):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.wake_word = wake_word.lower()
        self.audio = pyaudio.PyAudio()
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.record_seconds = 5
        self.temp_audio_file = "temp_audio.wav"

    def listen_for_wake_word(self) -> bool:
        """
        Continuously listen for the wake word.
        
        Returns:
            bool: True if wake word detected, False otherwise.
        """
        print(f"Listening for wake word: '{self.wake_word}'...")
        
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=1)
                    text = self.recognizer.recognize_google(audio, language=self.language).lower()
                    
                    if self.wake_word in text:
                        print("Wake word detected!")
                        self.play_activation_sound()
                        return True
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    print("Could not request results from Google Speech Recognition service")
                    return False

    def play_activation_sound(self):
        """
        Play a short sound to indicate wake word detection.
        """
        frequency = 440  # Hz
        duration = 0.2  # seconds
        samples = np.arange(int(self.rate * duration)) / self.rate
        waveform = np.sin(2 * np.pi * frequency * samples)
        audio = np.int16(waveform * 32767)
        
        stream = self.audio.open(format=self.format, channels=1, rate=self.rate, output=True)
        stream.write(audio.tobytes())
        stream.stop_stream()
        stream.close()

    def record_audio(self) -> None:
        """
        Record audio from the microphone and save it to a temporary file.
        """
        stream = self.audio.open(format=self.format, channels=self.channels,
                                 rate=self.rate, input=True,
                                 frames_per_buffer=self.chunk,input_device_index=1)
        
        print("Recording...")
        
        frames = []
        for _ in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
        
        print("Recording finished.")
        
        stream.stop_stream()
        stream.close()
        
        with wave.open(self.temp_audio_file, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))

    def transcribe_audio(self) -> Optional[str]:
        """
        Transcribe the recorded audio using Google's Speech Recognition API.
        
        Returns:
            str: Transcribed text if successful, None otherwise.
        """
        if not os.path.exists(self.temp_audio_file):
            print("No audio file found. Please record audio first.")
            return None

        with sr.AudioFile(self.temp_audio_file) as source:
            audio_data = self.recognizer.record(source)
        
        try:
            text = self.recognizer.recognize_google(audio_data, language=self.language)
            print(f"Transcription: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        
        return None

    def cleanup(self) -> None:
        """
        Clean up resources and remove temporary audio file.
        """
        self.audio.terminate()
        if os.path.exists(self.temp_audio_file):
            os.remove(self.temp_audio_file)

    def recognize_speech(self) -> Optional[str]:
        """
        Wait for wake word, then record audio and transcribe it.
        
        Returns:
            str: Transcribed text if successful, None otherwise.
        """
        if self.listen_for_wake_word():
            self.record_audio()
            text = self.transcribe_audio()
            self.cleanup()
            return text
        return None

# Example usage
if __name__ == "__main__":
    recognizer = SpeechRecognizer(language="en-IN", wake_word="chhotu")
    while True:
        transcribed_text = recognizer.recognize_speech()
        if transcribed_text:
            print(f"Final transcription: {transcribed_text}")
            # Process the transcribed text here
        else:
            print("Speech recognition failed or was interrupted.")