# J.A.R.V.I.S

## Description
J.A.R.V.I.S. is a virtual assistant designed to help you with day-to-day tasks, such as controlling smart home devices, performing searches, and more. It leverages speech recognition and various APIs to provide a seamless user experience.

## Features
- **Smart Home Control**: Control your TV and other smart home devices.
- **Web Browsing**: Open websites and perform searches on different platforms like Google, Bing, and YouTube.
- **Voice Commands**: Execute various commands through voice input.
- **Fun Interactions**: Responds to fun commands like jokes and repeating phrases.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/J.A.R.V.I.S.git
    ```
2. Navigate to the project directory:
    ```bash
    cd J.A.R.V.I.S
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the main script:
    ```bash
    python main.py
    ```
2. Use voice commands to interact with J.A.R.V.I.S. Some example commands include:
    - "Open YouTube"
    - "Search for weather on Bing"
    - "Turn off the TV"
    - "Tell me a joke"

## File Structure
- `main.py`: The main entry point of the application.
- `tv.py`: Contains functions to control the TV.
- `browser.py`: Handles web browsing functionalities.
- `speech.py`: Manages speech recognition and text-to-speech functionalities.
- `test_speech.py`: Script for testing speech recognition.
- `log.txt`: Log file for error messages and debugging.

## Error Handling
Errors are logged in the `log.txt` file. If you encounter issues, check this file for more details.

## Contributing
1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Description of changes"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-branch
    ```
5. Open a pull request.


## Acknowledgements
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pyaudio](https://pypi.org/project/PyAudio/)
- [webbrowser](https://docs.python.org/3/library/webbrowser.html)
- [requests](https://pypi.org/project/requests/)

## Contact
For any questions or suggestions, please open an issue or contact the project maintainer at [liamjbusby08@outlook.com].