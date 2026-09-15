"""
Filter implementations for image processing
"""

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


class ImageFilters:
    """Collection of image filters"""
    
    @staticmethod
    def blur(image, kernel_size=15):
        """Apply blur filter"""
        return cv2.blur(image, (kernel_size, kernel_size))
    
    @staticmethod
    def sharpen(image, strength=1.5):
        """Apply sharpen filter"""
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Sharpness(pil_image)
        result = enhancer.enhance(strength)
        return cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def edge_detection(image):
        """Detect edges using Canny edge detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    @staticmethod
    def grayscale(image):
        """Convert to grayscale"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    @staticmethod
    def sepia(image):
        """Apply sepia tone filter"""
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        sepia_image = cv2.transform(image, sepia_filter)
        sepia_image = np.clip(sepia_image, 0, 255)
        return sepia_image.astype(np.uint8)
    
    @staticmethod
    def brightness(image, factor=1.2):
        """Adjust brightness"""
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Brightness(pil_image)
        result = enhancer.enhance(factor)
        return cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def contrast(image, factor=1.5):
        """Adjust contrast"""
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Contrast(pil_image)
        result = enhancer.enhance(factor)
        return cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def gaussian_blur(image, kernel_size=21):
        """Apply Gaussian blur"""
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    @staticmethod
    def invert(image):
        """Invert colors"""
        return cv2.bitwise_not(image)
    
    @staticmethod
    def emboss(image):
        """Apply emboss filter"""
        kernel = np.array([[-2, -1, 0],
                          [-1,  1, 1],
                          [ 0,  1, 2]], dtype=np.float32)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        embossed = cv2.filter2D(gray, -1, kernel)
        embossed = np.clip(embossed + 128, 0, 255).astype(np.uint8)
        return cv2.cvtColor(embossed, cv2.COLOR_GRAY2BGR)
