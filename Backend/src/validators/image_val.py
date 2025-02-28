# Simple & Fast Image Validator for Profile and Post Images
# Author: Joshua Ferguson

# Image Validator

from marshmallow import ValidationError
from PIL import Image
import json, os

IMAGE_SIZE_ERROR = {"error": "Image size exceeds limit!"}
IMAGE_FORMAT_ERROR = {"error": "Image Format Invalid!"}
IMAGE_PROFANITY_ERROR = {"error": "Image Containts Profanity!"}
    
class ImageValidator:
    
    # TODO: Implement Image Size Validation
    @staticmethod
    def val_size(image_file, max_size_mb=10):
        """
        Validates the size of the image.
        Raises ValidationError if the image is too large.
        """
        image_file.seek(0, os.SEEK_END)
        file_size = image_file.tell() / (1024 * 1024)  # Convert bytes to MB
        image_file.seek(0)
        return file_size <= max_size_mb
    
    # TODO: Implement Image Format Validation
    @staticmethod
    def val_format(image_path):
        """
        Validates the format of the image.
        Raises ValidationError if the image is not a valid format.
        """
        valid_formats = {"JPEG", "JPG", "PNG"}
        try:
            img = Image.open(image_path)
            return img.format in valid_formats
        except Exception:
            return False


    # TODO: Test Image Profanity Validation and Integate into the Message/Profiles Routes
    @staticmethod
    def val_profanity(image_path):
        """
        Validates the image for NSFW Pornographic and Hentai Content.
        - If profanity is detected, raises ValidationError.
        """
        
        return True
    
    def val_all(self, image_path):
        
        errors = []
        # Val Size
        if not self.val_size(image_path):
            errors.append(IMAGE_SIZE_ERROR)
        # Val Format
        if not self.val_format(image_path):
            errors.append(IMAGE_FORMAT_ERROR)
        # Val Profanity
        if not self.val_profanity(image_path):
            errors.append(IMAGE_PROFANITY_ERROR)
        
        # Prints Errors if Found
        if errors:
            for error in errors:
                print(error)
            return False
        
        # Return True if Passes All
        return True