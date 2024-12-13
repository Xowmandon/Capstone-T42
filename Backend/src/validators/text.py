from marshmallow import ValidationError
from better_profanity import profanity


class TextValidator:
    @staticmethod
    def val_length(content,lower_bound=1,upper_bound=500):
        """
        Validates the length of the content.
        Raises ValidationError if the content is too long or too short.
        """
        if len(content) > upper_bound:
            raise ValidationError("Message must be less than 500 characters.")
        if len(content) < lower_bound:
            raise ValidationError("Message must be at least 1 character.")

    @staticmethod
    def val_profanity(content, censor=True):
        """
        Validates the content for profanity.
        - If censor is True, the content is censored instead of raising an error.
        - If profanity is detected and censor is False, raises ValidationError.
        """
        if profanity.contains_profanity(content):
            if censor:
                return profanity.censor(content)
            else:
                raise ValidationError("Content contains profanity.")
            
        return content

    @staticmethod
    def val_all(content, censor=False):
        """
        Runs all validations on the content.
        Returns the validated (and optionally censored) content.
        """
        # Validate the length of the content
        TextValidator.val_length(content)
        
        # Validate the content for profanity
        # Return the censored content if profanity is detected, otherwise return the original content
        return TextValidator.val_profanity(content, censor=censor) 