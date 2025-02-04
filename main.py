import mediapipe as mp
import cv2, time
import pyautogui
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

model_path = './face_landmarker.task' # Change for different models

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

webcam = cv2.VideoCapture(1) # Change for different cameras

VERTICAL_THRESHOLD = 40 # Initial threshold for eye postition threshold
SCROLL_DELAY = 0.1  # seconds between scrolls

last_scroll_time = time.time() # Time of last scroll to buffer scrolls

def show_start_menu():
    menu_frame = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Title
    cv2.putText(menu_frame, "Eye Control Menu", (150, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Instructions
    instructions = [
        "Controls:",
        "W - Increase sensitivity",
        "S - Decrease sensitivity",
        "Q - Quit",
        "",
        "Looking down = Scroll down",
        "",
        "Press SPACE to start"
    ]
    
    y_pos = 100
    for instruction in instructions:
        cv2.putText(menu_frame, instruction, (50, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        y_pos += 40
    
    cv2.imshow("Eye auto scroll", menu_frame)
    
    # Wait for space key
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            return True
        elif key == ord('q'):
            return False

if not show_start_menu():
    webcam.release()
    cv2.destroyAllWindows()
    exit()

# Create a face landmarker instance with the live stream mode:
def result_callback(result: FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global last_scroll_time
    
    if result.face_blendshapes:
        blendshapes = result.face_blendshapes[0]
        
        # Extract eye-related blendshapes
        eye_states = {
            'Left Eye': {
                'Blink': next(b.score for b in blendshapes if b.category_name == 'eyeBlinkLeft'),
                'Look Up': next(b.score for b in blendshapes if b.category_name == 'eyeLookUpLeft'),
                'Look Down': next(b.score for b in blendshapes if b.category_name == 'eyeLookDownLeft'),
                'Look Left': next(b.score for b in blendshapes if b.category_name == 'eyeLookOutLeft'),
                'Look Right': next(b.score for b in blendshapes if b.category_name == 'eyeLookInLeft'),
            },
            'Right Eye': {
                'Blink': next(b.score for b in blendshapes if b.category_name == 'eyeBlinkRight'),
                'Look Up': next(b.score for b in blendshapes if b.category_name == 'eyeLookUpRight'),
                'Look Down': next(b.score for b in blendshapes if b.category_name == 'eyeLookDownRight'),
                'Look Left': next(b.score for b in blendshapes if b.category_name == 'eyeLookInRight'),
                'Look Right': next(b.score for b in blendshapes if b.category_name == 'eyeLookOutRight'),
            }
        }

        # Clear the console
        # os.system('cls' if os.name == 'nt' else 'clear')

        # Print formatted output
        print("\nEye Positions:")
        for eye, states in eye_states.items():
            print(f"\n{eye}:")
            for state, score in states.items():
                # Convert score to percentage
                percentage = score * 100
                # Only show significant movements (above 10%)
                if percentage > 10:
                    print(f"  {state}: {percentage:.1f}%")
                if state == 'Look Down' and eye == 'Left Eye' and percentage > VERTICAL_THRESHOLD: # Only check 1 eye to limit scrolls
                    try:
                        if time.time() - last_scroll_time > SCROLL_DELAY:
                            pyautogui.scroll(-50)
                            last_scroll_time = time.time()
                    except Exception as e:
                        print(f"Error scrolling: {e}")


options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=result_callback,
    num_faces=1,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=False,
)

frame_timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)

with FaceLandmarker.create_from_options(options) as landmarker:
    def main_loop(landmarker, webcam):
        global VERTICAL_THRESHOLD, last_scroll_time
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                return True  # Return to menu
            elif key == ord('w'):
                VERTICAL_THRESHOLD += 5
                print(f"Vertical Threshold: {VERTICAL_THRESHOLD}")
            elif key == ord('s'):
                VERTICAL_THRESHOLD -= 5
                print(f"Vertical Threshold: {VERTICAL_THRESHOLD}")

            frame_timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
            ret, frame = webcam.read()
            if not ret:
                print("Failed to capture frame from webcam. Exiting.")
                return False

            # Add threshold display to frame
            cv2.putText(frame, f"Threshold: {VERTICAL_THRESHOLD}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show the frame
            cv2.imshow("Eye auto scroll", frame)

            # Convert the frame received from OpenCV to a MediaPipe's Image object.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            landmarker.detect_async(mp_image, frame_timestamp_ms)

    # Main program loop
    while True:
        if show_start_menu():
            # Start the main tracking loop
            if not main_loop(landmarker, webcam):
                break  # Exit if there's an error
        else:
            break  # Exit if user quits from menu

    # Cleanup
    webcam.release()
    cv2.destroyAllWindows()
