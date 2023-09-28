import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pyttsx3
import threading
import shutil
import pygame
import tempfile
import os

class TextToSpeechConverter:
    """converting text to speech and playing it."""

    def __init__(self, root):
        """
        Initialize the TextToSpeechConverter.

        Args:
            root (tk.Tk): The root tkinter window.
        """

        self.root = root
        self.root.title("TSS Converter")

        self.setup_gui()
        self.setup_audio()

    def setup_gui(self):
        """Set up the graphical user interface."""

        label = tk.Label(self.root, text="Enter Text:")
        label.pack()

        self.text_entry = tk.Text(self.root, wrap=tk.WORD, width=60, height=15)
        self.text_entry.pack()
        self.text_preview_frame = tk.Frame(self.root)
        self.text_preview_frame.pack()

        

        load_button = tk.Button(self.root, text="Load File", command=self.load_text_from_file)
        load_button.pack()

        convert_button = tk.Button(self.root, text="Convert and Play", command=self.convert_and_play)
        convert_button.pack()

        save_audio_button = tk.Button(self.root, text="Save as Audio", command=self.save_as_audio)
        save_audio_button.pack()

        play_pause_button = tk.Button(self.root, text="Pause/Resume", command=self.pause_resume_audio)
        play_pause_button.pack()

        stop_button = tk.Button(self.root, text="Stop", command=self.stop_audio)
        stop_button.pack()
        

        # Speed control slider
        speed_label = tk.Label(self.root, text="Speed:")
        speed_label.pack()
        self.speed_slider = tk.Scale(self.root, from_=0.5, to=2.0, orient="horizontal", resolution=0.1)
        self.speed_slider.set(1.0)  # Default speed is 1.0
        self.speed_slider.pack()

        # Pitch control slider
        pitch_label = tk.Label(self.root, text="Pitch:")
        pitch_label.pack()
        self.pitch_slider = tk.Scale(self.root, from_=0.5, to=10.0, orient="horizontal", resolution=0.1)
        self.pitch_slider.set(1.0)  # Default pitch is 1.0
        self.pitch_slider.pack()

        self.text_preview_labels = []
        for _ in range(5):  # Display the current word and the surrounding two words
            label = tk.Label(self.text_preview_frame, text="", font=("Arial", 12))
            self.text_preview_labels.append(label)
            label.pack(side="left")


    def setup_audio(self):
        """Set up the audio components."""

        pygame.mixer.init()
        self.audio_thread = None
        self.is_playing = False
        self.text_to_play = ""
        self.audio_file_path = ""
        self.speed = 1.0
        self.pitch = 1.0

        # Initialize pyttsx3
        self.engine = pyttsx3.init()

    def convert_and_play(self):
        """Convert the entered text to speech and play it."""

        if self.is_playing:
            self.stop_audio()

        text = self.text_entry.get("1.0", "end-1c")
        if text.strip() and (text != self.text_to_play or self.speed != self.speed_slider.get() or self.pitch != self.pitch_slider.get()):
            self.text_to_play = text
            self.speed = self.speed_slider.get()  # Get speed from the slider
            self.pitch = self.pitch_slider.get()
            try:
                temp_dir = tempfile.mkdtemp()
                mp3_file_path = os.path.join(temp_dir, "TTS.wav")

                # Configure the speech synthesis engine with speed and pitch
                self.engine.setProperty("rate", self.speed * 200)  # Adjust the rate (speed)
                self.engine.setProperty("pitch", self.pitch)  # Adjust the pitch

                # Save the speech to an audio file
                self.engine.save_to_file(text, mp3_file_path)
                self.engine.runAndWait()

                self.audio_file_path = mp3_file_path

                def play_audio():
                    pygame.mixer.music.load(mp3_file_path)
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_endevent(pygame.USEREVENT)

                    # Start highlighting currently spoken words
                    self.highlight_current_and_surrounding_words(text)

                self.audio_thread = threading.Thread(target=play_audio)
                self.audio_thread.start()
                self.is_playing = True
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during text-to-speech conversion: {str(e)}")
        elif text.strip() and text == self.text_to_play and self.speed == self.speed_slider.get() and self.pitch == self.pitch_slider.get():
            self.play_again()
        else:
            messagebox.showwarning("Warning", "Please enter text to convert and play.")


    def highlight_current_and_surrounding_words(self, text):
        """
        Highlight the current word and surrounding words during playback.

        Args:
            text (str): The text being played.
        """
        words = text.split()
        current_word_index = 0

        while self.is_playing and current_word_index < len(words):
            # Determine the indices of the words to highlight
            start_index = max(0, current_word_index - 2)
            end_index = min(current_word_index + 2, len(words))

            # Update label texts with highlighted current word and surrounding words
            for i, label in enumerate(self.text_preview_labels):
                if start_index + i == current_word_index:
                    label.config(text=words[start_index + i], fg="blue", font=("Arial", 12))
                else:
                    label.config(text=words[start_index + i], fg="black", font=("Arial", 12))

            self.text_preview_frame.update()
            current_word_index += 1
            pygame.time.delay(int(len(words[current_word_index - 1]) * 100))  # Adjust the delay based on word length

            # Reset the labels' texts and colors
            for label in self.text_preview_labels:
                label.config(text="", fg="black")

            
    def save_as_audio(self):
        """Save the speech as an audio file."""

        if self.audio_file_path:
            if self.is_playing:
                self.stop_audio()  # Stop audio playback if it's currently playing

            save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")])
            if save_path:
                try:
                    shutil.copy(self.audio_file_path, save_path)
                    self.audio_file_path = save_path
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while saving the audio file: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No audio to save. Please convert text to audio first.")

    def stop_audio(self):
        """Stop the audio playback."""

        if self.is_playing or self.audio_thread is not None:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.audio_thread = None

    def pause_resume_audio(self):
        """Pause or resume the audio playback."""

        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def play_again(self):
        """Restart the audio playback."""

        pygame.mixer.music.play()
        self.is_playing = True


    def load_text_from_file(self):
        """Load text from a file into the text entry field."""

        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        try:
            if file_path:
                with open(file_path, "r") as file:
                    text = file.read()
                    self.text_entry.delete("1.0", "end")
                    self.text_entry.insert("1.0", text)

        except FileNotFoundError:
            messagebox.showerror("Error", "File not found or operation canceled.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the file: {str(e)}")


    

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechConverter(root)
    root.mainloop()


