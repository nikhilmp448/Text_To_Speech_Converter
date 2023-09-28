# Creating an Executable for the Text-to-Speech Converter Application
The Text-to-Speech Converter (TSS Converter) is a Python application that allows you to convert text into speech and play it using the Python library pygame and the text-to-speech engine pyttsx3. This application provides a graphical user interface (GUI) built with tkinter for user interaction.

## Features
Enter or load text for conversion to speech.
Adjust speech speed and pitch.
Play, pause, and stop audio playback.
Highlight currently spoken words.
Save the converted audio as an MP3 or WAV file.
## Requirements
Before running the application, ensure you have the following dependencies installed:

Python 3.x
Pygame
Pyttsx3
Tkinter (usually included with Python)
You can install pygame and pyttsx3 using pip:

```console
pip install -r requirements.txt
```
## Running the Application
Follow these steps to run the Text-to-Speech Converter application:

1) Clone or download the repository to your local machine.

2) Open a terminal or command prompt and navigate to the project directory.

3) Run the application script using Python:
```console
python textToSpeach.py
```
This command will start the application, and the GUI window will appear.

4) Use the application's GUI to perform the following actions:

    * Enter or load text for conversion.
    * Adjust speech speed and pitch using the sliders.
    * Click the "Convert and Play" button to play the converted speech.
    * Click the "Pause/Resume" button to pause or resume audio playback.
    * Click the "Stop" button to stop audio playback.
    * Click the "Save as Audio" button to save the audio as an MP3 or WAV file.
5) Enjoy using the Text-to-Speech Converter!

## Loading Text from a File
You can load text from a file by clicking the "Load File" button and selecting a text file (with a ".txt" extension) containing the text you want to convert.

## Building an Executable
If you want to create an executable file to run the application without Python and its dependencies, you can use a tool like PyInstaller. Follow the instructions in the section above titled "Creating an Executable File" to package the application.


## Steps to Create an Executable
Follow these steps to create an executable file for the TSS Converter application:

1) Install PyInstaller: If you haven't already installed PyInstaller, do so by running the following command:
```console
pip install pyinstaller
```
2) Navigate to the Application Directory: Open a terminal or command prompt and navigate to the directory containing your TSS Converter application source code.

3) Generate the Spec File: Use PyInstaller to generate a spec file for your application. Replace your_script.py with the name of your Python script:

```console
pyinstaller --name TSSConverter --onefile your_script.py
```
4) Build the Executable: Run the following command to build the executable:
```console
pyinstaller TSSConverter.spec
```
This command will start the build process, and PyInstaller will create the executable file in a dist directory within your project folder.

5) Distribute the Executable: You can now distribute the executable file to users on different platforms:

On Linux: The generated executable can be run directly.
On Windows: The generated executable will have a ".exe" extension and can be run as a Windows application.
On macOS: The generated executable will be a macOS application bundle. Users can run it by double-clicking.
6) Run the Executable: Test the executable on the respective platform to ensure it works as expected.

## Notes
Make sure to provide necessary permissions when saving audio files or loading text files, as the application may need file access rights.

This application was developed using Python and may have platform-specific considerations when creating executables for Windows, Linux, and macOS.


For any issues, questions, or suggestions, please feel free to contact the developer [a link](https://github.com/nikhilmp448/).


