# Simple & Fast Image Validator for Profile and Post Images
# Author: Joshua Ferguson

# Image Validator



from marshmallow import ValidationError
import json

class ImageValidator:
    
    # TODO: Implement Image Size Validation
    @staticmethod
    def val_size(image_path, max_size=2):
        """
        Validates the size of the image.
        Raises ValidationError if the image is too large.
        """
        return True
    
    # TODO: Implement Image Format Validation
    @staticmethod
    def val_format(image_path):
        """
        Validates the format of the image.
        Raises ValidationError if the image is not a valid format.
        """
        return True

    # TODO: Test Image Profanity Validation and Integate into the Message/Profiles Routes
    @staticmethod
    def val_profanity(image_path):
        """
        Validates the image for NSFW Pornographic and Hentai Content.
        - If profanity is detected, raises ValidationError.
        """
        
        return True