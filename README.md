# .mp3 to muscial notes API

An API that returns an array of musical notes from an .mp3 file. Works most consistently with files that have clear notes from a single instrument.

## How it works

The API will save the posted .mp3 file to a folder, then convert it from .mp3 to raw .wav format. This .wav file is loaded with the librosa library which extracts an array of amplitudes. After cleaning up this array the script converts the amplitude array to a frequency array along with an array of the same size specifying the probability each frequency is accurate. The probability values are used to determine which of the frequency values should be added to a notes array. Then, the notes array is returned to the API caller in JSON format.

## Prerequisites
- Python 3.x
- ffmpeg

## Configure and run it locally
1. **Clone the repository:**
   
   ```bash
   git clone git@github.com:bocsir/mp3-notes.git
   cd mp3-notes
   ```

2. **Create virtual enviroment:**

    ```bash
    python -m venv env
    ```

3. **Activate virtual environment:**

    Linux and macOS:
    ```bash
    source env/bin/activate
    ```

    Windows: 
    ```bash
    env/Scripts/activate
    ```
4. **Install dependencies**
  
    ```bash
    pip install -r requirements.txt
    ```

5. **Configure Flask**
   
    Linux and macOS:
    ```bash
    export FLASK_APP=app.py
    ```
  
    Windows:
    ```bash
    set FLASK_APP=app.py
    ```

7. **Using the API**

    Start flask application:
    ```bash
    flask run
    ```
  
    Call the API at 127.0.0.1:5000/ using cURL:
    ```bash
    curl -X POST http://127.0.0.1:5000/api/audio -F "file=/path/to/file.mp3"
    ```
    Where ```/path/to/file.mp3``` represents the .mp3 file location you want to get notes from.

     Try it with the included test.mp3:
     ```bash
     curl -X POST http://127.0.0.1:5000/api/audio -F "file=test.mp3"
     ```
   
