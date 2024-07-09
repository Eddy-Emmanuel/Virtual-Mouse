# Virtual Mouse with Hand Tracking

This project uses OpenCV, Mediapipe, and PyAutoGUI to create a virtual mouse controlled by hand movements. The project uses a webcam feed to detect hand landmarks and perform mouse movements and clicks based on specific gestures.

## Features

- **Move Mouse**: Move the cursor by raising the tip of your index finger.
- **Mouse Click**: Click by raising both the index finger and middle finger tips simultaneously.

## Requirements

To run this project, you'll need the following dependencies:

- Python 3.x
- OpenCV
- Mediapipe
- PyAutoGUI

You can install these dependencies using `pip`:

```sh
pip install opencv-python mediapipe pyautogui
```

## Installation

1. **Clone the repository**:

```sh
git clone https://github.com/yourusername/virtual-mouse.git
cd virtual-mouse
```

2. **Install the required packages**:

```sh
pip install -r requirements.txt
```

3. **Run the virtual mouse script**:

```sh
python main.py -s 0
```

## Usage

### Command Line Arguments

- `-s`, `--Source`: Source of the video feed. Default is `0` (webcam).

### Hand Gestures

- **Move Mouse**: Raise the tip of your index finger.
- **Mouse Click**: Raise both the index finger and middle finger tips simultaneously.

## File Structure

- `main.py`: The main script to run the virtual mouse.
- `utility.py`: Contains the `Utilities` class for handling hand detection, mouse movement, and clicking functions.
- `requirements.txt`: List of required Python packages.

## Contributing

Feel free to fork this repository and submit pull requests. If you find any issues or have suggestions, please open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
