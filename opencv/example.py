import cv2
import numpy as np
from typing import Tuple, Optional


class OpenCVUtilities:
    def __init__(self):
        pass

    # Load an image
    @staticmethod
    def load_image(path: str) -> np.ndarray:
        return cv2.imread(path)

    # Save an image
    @staticmethod
    def save_image(image: np.ndarray, path: str) -> None:
        cv2.imwrite(path, image)

    # Display an image
    @staticmethod
    def display_image(image: np.ndarray, window_name: str = "Image") -> None:
        cv2.imshow(window_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Resize image
    @staticmethod
    def resize_image(image: np.ndarray, dimensions: Tuple[int, int]) -> np.ndarray:
        return cv2.resize(image, dimensions)

    # Convert to grayscale
    @staticmethod
    def to_grayscale(image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    @staticmethod
    def apply_gaussian_blur(image: np.ndarray, kernel_size: Tuple[int, int] = (5, 5)) -> np.ndarray:
        return cv2.GaussianBlur(image, kernel_size, 0)

    # Detect edges using Canny
    @staticmethod
    def detect_edges(image: np.ndarray, low_threshold: int, high_threshold: int) -> np.ndarray:
        return cv2.Canny(image, low_threshold, high_threshold)

    # Perform histogram equalization
    @staticmethod
    def equalize_histogram(image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 2:  # Grayscale
            return cv2.equalizeHist(image)
        elif len(image.shape) == 3:  # Color
            ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
        return image

    # Apply a morphological operation
    @staticmethod
    def morphological_operation(image: np.ndarray, operation: str, kernel_size: Tuple[int, int]) -> np.ndarray:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
        if operation == "dilate":
            return cv2.dilate(image, kernel)
        elif operation == "erode":
            return cv2.erode(image, kernel)
        elif operation == "open":
            return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        elif operation == "close":
            return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        else:
            raise ValueError("Invalid operation type. Choose from 'dilate', 'erode', 'open', 'close'.")

    # Detect faces using Haar cascades
    @staticmethod
    def detect_faces(image: np.ndarray, cascade_path: str) -> np.ndarray:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return image

    # Rotate an image
    @staticmethod
    def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, M, (w, h))

    # Flip an image
    @staticmethod
    def flip_image(image: np.ndarray, flip_code: int) -> np.ndarray:
        return cv2.flip(image, flip_code)

    # Add text to an image
    @staticmethod
    def add_text(image: np.ndarray, text: str, position: Tuple[int, int], font_scale: float = 1, color: Tuple[int, int, int] = (255, 255, 255), thickness: int = 2) -> np.ndarray:
        font = cv2.FONT_HERSHEY_SIMPLEX
        return cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

    # Real-time video capture and processing
    @staticmethod
    def process_video(feed: int = 0, process_frame_func: Optional[callable] = None) -> None:
        cap = cv2.VideoCapture(feed)
        if not cap.isOpened():
            print("Error: Unable to open video feed.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read frame.")
                break

            if process_frame_func:
                frame = process_frame_func(frame)

            cv2.imshow("Video Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    # Template matching
    @staticmethod
    def match_template(image: np.ndarray, template: np.ndarray, threshold: float = 0.8) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray, template_gray, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        for loc in zip(*locations[::-1]):
            cv2.rectangle(image, loc, (loc[0] + template.shape[1], loc[1] + template.shape[0]), (0, 255, 0), 2)
        return image


# Example usage
if __name__ == "__main__":
    utils = OpenCVUtilities()

    # # Example: Load and display an image
    # img = utils.load_image("image.jpg")
    # utils.display_image(img, "Original Image")

    # # Example: Resize and save
    # resized_img = utils.resize_image(img, (500, 500))
    # utils.save_image(resized_img, "resized_image.jpg")

    # # Example: Detect edges and display
    # edges = utils.detect_edges(img, 100, 200)
    # utils.display_image(edges, "Edges Detected")

    # # Example: Process webcam feed with edge detection
    def edge_processing(frame):
        return utils.detect_edges(frame, 50, 150)

    utils.process_video(process_frame_func=edge_processing)
