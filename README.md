# Eye Auto Scroll

Eye Auto Scroll is a simple tool that leverages Google MediaPipe's Face Landmarker solution to track eye movements in real-time and automatically scroll your screen or add your own eye based commands. With this application, you can adjust how far you have to look down before triggering a scroll, making it perfect if you want to read while enjoying a messy meal.

## How It Works

The application uses your webcam to capture live video feed and processes it using MediaPipe’s face landmarker model for real-time facial and eye tracking. When your eye’s "Look Down" score exceeds a set threshold (default is 40%), the program triggers a scroll action using pyautogui. You can adjust the vertical threshold (and thus the sensitivity) using simple keyboard controls.

## Resources & Acknowledgements

This project was built using resources and guides from Google MediaPipe:
- [MediaPipe Face Landmarker (Live Stream)](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker/python#live-stream)
- [MediaPipe Solutions Guide](https://ai.google.dev/edge/mediapipe/solutions/guide)

The face landmarker model used (file: `face_landmarker.task`) was downloaded from Google’s docs mentioned above.

## Requirements

- **Python 3.12** – Note: Google MediaPipe currently supports only Python 3.12.
- [OpenCV-Python](https://pypi.org/project/opencv-python/)
- [MediaPipe](https://pypi.org/project/mediapipe/)
- [NumPy](https://pypi.org/project/numpy/)
- [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/IsJustJason/eye-commands.git
   cd eye-commands
   ```

2. **Install the requirements:**

   ```bash
   pip install opencv-python mediapipe numpy pyautogui
   ```

## Configuration

If you need to change the video device (e.g., if you’re using a different webcam), simply modify the video device number in the code. Open `main.py` and change the following line:

```python
webcam = cv2.VideoCapture(1) # Change for different cameras
```


## Usage Instructions

1. **Run the application:**

   ```bash
   python main.py
   ```

2. **Review the Start Menu:**

   A start menu will appear, showing controls and instructions.
   - **Note:** Due to a known bug, you may need to press the SPACE key twice to fully start the application.

3. **During Operation:**

   - **Look Down to Scroll:** When you look down (detected by the left eye), the application will trigger an auto-scroll. This makes it easier to read on-screen content even if you switch focus to another window.
   - **Adjust Sensitivity:**
     - Press **W** to increase the sensitivity (vertical threshold).
     - Press **S** to decrease the sensitivity.
   - Press **Q** at any time to quit and return to the menu.

Now you can enjoy your meal 🍽️ even while reading something important!

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open a pull request or raise an issue on the repository.

## License

This project is licensed under the MIT License.