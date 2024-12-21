## Running Locally
1. Setup a virtual environment using `python -m venv env`
2. Install the dependencies using `pip install -r requirements.txt`
3. Then run the script following usage section

## Usage 
The script arguments are
```py
usage: img2pan.py [-h] [-ct CAPTURE_TO] [-o OUTPUT_TO]

options:
  -h, --help            show this help message and exit
  -ct CAPTURE_TO, --capture-to CAPTURE_TO
                        save the generated frames to the provided path
  -o OUTPUT_TO, --output-to OUTPUT_TO
                        save the generated panaroma to the provided path
```

After the camera turns on, the usage is,

- Pressing key 'c'
    * The cam starts saving the frames to memory every `self.capture_buffer` seconds.
- Pressing key 's'
    * The cam stops saving the frames to memory and calls `self.save_frames(flush=True)`.
    This is useful for testing.
- Pressing key 'q'
    * The cam stops saving the frames to memory and the cam itself is released. However,
    the frames are still stored and can be accessed using `save_frames` and `get_frames` methods.
