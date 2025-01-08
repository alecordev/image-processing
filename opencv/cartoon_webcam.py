import datetime

import cv2
import numpy as np


def save_screenshot(frame):
    """Save the current frame as a screenshot with a timestamped filename."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%d_%H-%M-%S"
    )
    filename = f"screenshot_{timestamp}.png"
    cv2.imwrite(filename, frame)
    print(f"Screenshot saved: {filename}")


def f5():
    """
    Cartoonizing an image with user controls.
    Press 's' for sketch mode, 'c' for cartoon mode, 'Enter' for normal mode, and 'Esc' to exit.
    """

    def cartoonize_image(img, ds_factor=4, sketch_mode=False):
        # Convert image to grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply median filter to the grayscale image
        img_gray = cv2.medianBlur(img_gray, 7)

        # Detect edges in the image and threshold it
        edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize=5)
        _, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)

        if sketch_mode:
            # Create a sketch effect
            img_sketch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            kernel = np.ones((3, 3), np.uint8)
            img_eroded = cv2.erode(img_sketch, kernel, iterations=1)
            return cv2.medianBlur(img_eroded, 5)

        # Resize the image for faster processing
        img_small = cv2.resize(
            img,
            None,
            fx=1.0 / ds_factor,
            fy=1.0 / ds_factor,
            interpolation=cv2.INTER_AREA,
        )
        num_repetitions = 10
        sigma_color = 5
        sigma_space = 7
        size = 5

        # Apply bilateral filter to smooth the image
        for _ in range(num_repetitions):
            img_small = cv2.bilateralFilter(img_small, size, sigma_color, sigma_space)

        img_output = cv2.resize(
            img_small, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_LINEAR
        )

        # Combine edges with the smoothed image
        return cv2.bitwise_and(img_output, img_output, mask=mask)

    def display_instructions(frame):
        """Overlay instructions on the video feed."""
        instructions = [
            "Press 's': Sketch Mode",
            "Press 'c': Cartoonize Mode",
            "Press 'Enter': Normal Mode",
            "Press 'p': Take Screenshot",
            "Press 'Esc': Exit",
        ]
        y = 20
        for instruction in instructions:
            cv2.putText(
                frame,
                instruction,
                (10, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                1,
            )
            y += 30

    cap = cv2.VideoCapture(0)
    cur_mode = "normal"  # Default mode

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting.")
            break

        frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)

        c = cv2.waitKey(1)
        if c == 27:  # Esc key
            break
        elif c == ord("s"):
            cur_mode = "sketch"
        elif c == ord("c"):
            cur_mode = "cartoon"
        elif c == 13:  # Enter key
            cur_mode = "normal"
        elif c == ord("p"):
            if processed_frame is not None:
                save_screenshot(processed_frame)
            else:
                save_screenshot(frame)

        # Apply selected mode
        if cur_mode == "sketch":
            processed_frame = cartoonize_image(frame, sketch_mode=True)
        elif cur_mode == "cartoon":
            processed_frame = cartoonize_image(frame, sketch_mode=False)
        else:  # Normal mode
            processed_frame = frame

        # Overlay instructions
        display_instructions(processed_frame)

        cv2.imshow("Cartoonize", processed_frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    f5()
