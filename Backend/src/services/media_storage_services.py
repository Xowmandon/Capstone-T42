
"""
Author: Joshua Ferguson
- Services for Media Storage and Bucket Services
- Used to Store and Retrieve Profile Images of Users by URLs of Objects stored on AWS s3
"""

import boto3
from botocore.exceptions import ClientError
from marshmallow import ValidationError
from Backend.src.extensions import db
from Backend.src.models.photo import UserPhoto
from Backend.src.models.user import User
from Backend.src.validators.image_val import ImageValidator
from Backend.src.utils import EnvManager

class UserPhotos():
    
    def __init__(self,user_id):
        self.profile_picture = []
        self.user_photos = []

class BucketService:
    """
    A service class for interacting with an S3 bucket.

    Attributes:
        s3_client: The S3 client object.
        bucket_name: The name of the S3 bucket.
        region: The AWS region where the bucket is located.
        folders: A list of folders within the bucket (optional).
    """

    def __init__(self,s3_client_param,bucket_name, region, folders=None):
        """
        Initializes the BucketService instance.

        Args:
            s3_client: The S3 client object.
            bucket_name: The name of the S3 bucket.
            region: The AWS region where the bucket is located.
            folders: A list of valid folders in the S3 bucket (optional).
        """
        self.s3_client = s3_client_param
        self.bucket_name = bucket_name
        self.region = region
        self.folders = folders if folders else []

        if not self.val_connection():
            raise ValueError("Connection to S3 bucket failed")
                
    def val_connection(self):
        
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError as e:
            print(e)
            return False
    
    def upload_file(self, file):
        """
        Uploads a file to the S3 bucket.

        Args:
            file: The local file path to be uploaded.
        """
        self.s3_client.upload_file(file, self.bucket_name, file)

    def delete_file(self, file_path):
        """
        Deletes a file from the S3 bucket.

        Args:
            file_path: The path of the file in the S3 bucket to delete.
        """
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_path)

    def get_objects(self,limit=None,page_size=None):
        
        obj_keys = []
        if limit != None:
            for obj in self.s3_client.Bucket(self.bucket_name).objects.limit(limit):
                obj_keys.append(obj)
            

        elif page_size != None:
            for obj in self.s3_client.Bucket(self.bucket_name).objects.page_size(page_size):
                obj_keys.append(obj)
        
        # Returns All Objects if No Limit or Page Size Set
        return obj_keys

class MediaStorageService(BucketService):
    """
    A specialized service for media file storage using an S3 bucket.
    Inherits from `BucketService` and adds support for user-based file management.
    """

    def __init__(self, s3_client_param,bucket_name, region, folders=None):
     
        super().__init__(
            s3_client_param=s3_client_param,
            bucket_name=bucket_name, 
            region=region, 
            folders=folders
            )

    def upload_user_photo(self, file, user_id, file_name, db_save=True, is_main_photo=False,folder=None):
        """
        Uploads a file to the media storage service.

        Args:
            file: The local file path to be uploaded.
            user_id: The ID of the user who owns the file.
            file_name: The name of the file in the S3 bucket.
            folder: The folder within the S3 bucket to store the file (optional).

        Returns:
            The URL of the uploaded file if successful, otherwise None.

        Raises:
            ClientError: If an error occurs during the upload process.
        """
        
        file_path = self._make_file_path(user_id=user_id, file_name=file_name, folder=folder)
        file_url = self.retrieve_file_url(user_id=user_id, file_name=file_name, folder=folder)

        try:
            
            # Validates Image According to Size, Format, and Profanity 
            if not ImageValidator().val_all(file_url):
                raise ValidationError("error: Image Validation Failed!")
            
            try:
                # Upload to S3 Bucket with file_data and Full Path with Folder,etc
                self.s3_client.upload_file(
                    file, 
                    self.bucket_name, 
                    file_path, 
                    ExtraArgs={'ACL': 'public-read', 'ContentType': file.content_type}
                    )
                
                # If Saving to DB, create new UserPhoto, add the File URL, and decide if its a Primary Photo
                if db_save:
                                        
                    # Save to PostgreSQL
                    new_photo = UserPhoto(user_id=user_id, file_url=file_url,is_main_photo=is_main_photo)
                    db.session.add(new_photo)
                    db.session.commit()
                    db.session.refresh(new_photo)
                    db.session.close()
     
            except Exception as e:
                print(e)
                return None
                    
            return file_url
        
        except ClientError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None

    def retrieve_file_url(self, user_id, file_name, folder=None):
        """
        Retrieves the public URL of a stored file.

        Args:
            user_id: The ID of the user who owns the file.
            file_name: The name of the file in the S3 bucket.
            folder: The folder within the S3 bucket where the file is stored (optional).

        Returns:
            The public URL of the file in the S3 bucket.
        """
        file_path = self._make_file_path(user_id=user_id, file_name=file_name, folder=folder)
        return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_path}"

    def _validate_folder(self, folder):
        """
        Validates if a folder exists in the predefined list.

        Args:
            folder: The folder name to validate.

        Returns:
            True if the folder is valid, False otherwise.

        Raises:
            ValueError: If the folder does not exist in the predefined list.
        """
        if folder:
            if folder in self.folders:
                return True
            raise ValueError(f"Invalid folder: {folder}")
        return False

    def _make_file_path(self, user_id, file_name, folder=None):
        """
        Constructs the file path in the S3 bucket.

        Args:
            user_id: The ID of the user who owns the file.
            file_name: The name of the file.
            folder: The folder within the S3 bucket (optional).

        Returns:
            The complete file path for storage in the S3 bucket.
        """
        if self._validate_folder(folder):
            return f"{folder}/{user_id}/{file_name}"
        return f"{user_id}/{file_name}"

    def delete_file(self, file_name, user_id, folder=None):
        """
        Deletes a file from the media storage service.

        Args:
            file_name: The name of the file to delete.
            user_id: The ID of the user who owns the file.
            folder: The folder where the file is located (optional).

        Returns:
            The result of the deletion operation.
        """
        file_path = self._make_file_path(user_id=user_id, file_name=file_name, folder=folder)
        del_success = super().delete_file(file_path)
        
        # Deletion of File From S3 Was Successful
        if del_success:
            url = self.retrieve_file_url(user_id=user_id,file_name=file_name,folder=folder)
            # Delete from DB
            user_photo = UserPhoto.query.filter(UserPhoto.user_id == user_id, UserPhoto.url == url).first()
            
            # If Photo is a Profile Main Picture, Update User Reference to Point to None IMAGE for Now
            if user_photo.is_main_photo:
                user = User.query.filter(User.user_id == user_id).first()
                user.profile_picture = EnvManager().load_env_var("DEFAULT_PROFILE_PICTURE")
                
            db.session.delete(user_photo)
            
            return True
        
        # File Could not Deleted from S3
        else:
            return False
    
    def get_user_photo_urls(self, user_id, folder=None):
        
        # Construct Base_Url and Prefix of Folder if Given
        base_url =  f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/"
        prefix = f"{folder}/{user_id}/" if folder else f"{user_id}/"
        
        # List All Objects in Bucket that are within the Given Folder and under user_id
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            
            # Return Empty if No Response
            if 'Contents' not in response:
                return []
            
            # Return URL of Each Object
            photos_urls = [base_url.join(obj['Key']) for obj in response['Contents']]
            return photos_urls
        
        except ClientError as e:
            print(e)
            return []
    