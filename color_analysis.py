import cv2
import numpy as np
import glob

def analyze_screenshots(screenshot_dir="screenshots"):
    for img_path in glob.glob(screenshot_dir + "/*.png"):
        img = cv2.imread(img_path)
        if img is None:
            continue
        # Example: find dominant color with simple k-means
        data = img.reshape((-1, 3))
        data = np.float32(data)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = 3  # 3 dominant colors
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        # You can do something with centers here
        print(f"Analyzed {img_path}, dominant colors (BGR): {centers}")

if __name__ == "__main__":
    analyze_screenshots()
