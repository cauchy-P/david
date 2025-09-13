import os
os.environ['QT_QPA_PLATFORM'] = 'xcb'  # Force X11 backend to avoid Wayland plugin error
import zipfile
import cv2
import numpy as np
import sys
from pathlib import Path

class MasImageHelper:
    def __init__(self, zip_path='cctv.zip', folder_name='CCTV'):
        self.zip_path = zip_path
        self.folder_name = folder_name
        self.image_files = []
        self.current_index = 0
        self.window_name = 'CCTV Viewer'
        self.detect_mode = False  # Toggle for astronaut detection
        
    def unzip_images(self):
        """Extract cctv.zip to CCTV folder."""
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.folder_name)
        except FileNotFoundError:
            print(f'Error: {self.zip_path} not found.')
            sys.exit(1)
        except zipfile.BadZipFile:
            print('Error: Invalid zip file.')
            sys.exit(1)
    
    def load_image_files(self):
        """Load list of image files from CCTV folder, ignoring non-image files."""
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        self.image_files = [
            os.path.join(self.folder_name, f) for f in os.listdir(self.folder_name)
            if os.path.isfile(os.path.join(self.folder_name, f)) and 
            f.lower().endswith(valid_extensions)
        ]
        self.image_files.sort()
        if not self.image_files:
            print('No valid image files found in CCTV folder.')
            sys.exit(1)
    
    def detect_astronauts_in_image(self, img):
        """Detect astronauts using color segmentation and return the image with rectangles."""
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Color ranges for astronaut suits (white, orange, gray/beige)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        mask_white = cv2.inRange(hsv, lower_white, upper_white)
        
        lower_orange = np.array([0, 100, 100])
        upper_orange = np.array([20, 255, 255])
        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
        
        lower_gray = np.array([0, 0, 100])
        upper_gray = np.array([180, 50, 200])
        mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
        
        mask = cv2.bitwise_or(mask_white, mask_orange)
        mask = cv2.bitwise_or(mask, mask_gray)
        
        # Morphology to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            if cv2.contourArea(cnt) > 1000:  # Filter small contours
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        return img
    
    def display_image(self, image_path):
        """Display an image, with optional astronaut detection based on detect_mode."""
        img = cv2.imread(image_path)
        if img is None:
            print(f'Error: Could not load image {image_path}.')
            return
        
        if self.detect_mode:
            img = self.detect_astronauts_in_image(img)
        
        cv2.imshow(self.window_name, img)
    
    def browse_images(self):
        """Display images with key navigation: arrows for prev/next, Enter for next, S to toggle detection, V to exit."""
        if not self.image_files:
            print('No images to display.')
            return
        
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        self.display_image(self.image_files[self.current_index])
        
        while True:
            key = cv2.waitKey(0) & 0xFF
            if key == ord('v') or key == ord('V'):  # V to exit
                break
            elif key == 81:  # Left arrow
                self.current_index = (self.current_index - 1) % len(self.image_files)
                self.display_image(self.image_files[self.current_index])
            elif key == 83 or key == 13:  # Right arrow or Enter for next
                self.current_index = (self.current_index + 1) % len(self.image_files)
                self.display_image(self.image_files[self.current_index])
            elif key == ord('s') or key == ord('S'):  # S to toggle detection
                self.detect_mode = not self.detect_mode
                self.display_image(self.image_files[self.current_index])
            elif key == 27:  # ESC as fallback exit
                break
        
        cv2.destroyAllWindows()

def main():
    helper = MasImageHelper()
    helper.unzip_images()
    helper.load_image_files()
    
    # Integrated viewer with browsing and detection
    print('Starting image viewer.')
    print('Controls:')
    print('- Left/Right Arrow or Enter: Navigate images')
    print('- S: Toggle astronaut detection (red boxes)')
    print('- V or ESC: Exit')
    helper.browse_images()

if __name__ == '__main__':
    main()