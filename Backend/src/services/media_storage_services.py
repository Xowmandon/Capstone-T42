
"""
Author: Joshua Ferguson
- Services for Media Storage and Bucket Services
- Used to Store and Retrieve Profile Images of Users by URLs of Objects stored on AWS s3
"""

from datetime import datetime, timezone
import logging
import os
from urllib.parse import urlparse
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
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
    
    def upload_file_obj(self, file):
        """
        Uploads a file to the S3 bucket.

        Args:
            file: The local file path to be uploaded.
        """
        self.s3_client.upload_fileobj(file, self.bucket_name, file)

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

    def upload_user_photo(self, file, user_id, file_name, db_save=True, is_main_photo=False,folder=None,title=None,description=None, content_type="image/jpeg"):
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
        # Add UUID_ to the Start OFfile name to ensure uniqueness
        #file_name = str(uuid4()) + "_" + file_name # Append UUID to the file name (prefix)
        file_path = self._make_file_path(user_id=user_id, file_name=file_name, folder=folder)
        file_url = self.retrieve_file_url(user_id=user_id, file_name=file_name, folder=folder)
        print(f"File Path: {file_path}")
        print(f"File URL: {file_url}")
        print(f"File Type: {type(file)}")
          
        try:
            
            # Validates Image According to Size, Format, and Profanity 
            #if not ImageValidator().val_all(file_url):
                #raise ValidationError("error: Image Validation Failed!")
            print(f"File Type: {type(file)}")
            try:
                # Upload to S3 Bucket with file_data and Full Path with Folder,etc

                self.s3_client.upload_file(
                    file,
                    self.bucket_name, 
                    file_path,
                    ExtraArgs={"ACL": "public-read","ContentType": content_type}, 
                )
   
                print(f"File uploaded to S3: {file_path}")
              
                #file_url = self.retrieve_file_url(user_id=user_id, file_name=file_name, folder=folder)
                #print(f"File URL: {file_url}")
                
                
            except Exception as e:
                print(f"Error uploading file to S3: {e}")
                return None
            
            # If Saving to DB, create new UserPhoto, add the File URL, and decide if its a Primary Photo
            if db_save and file_url:
                
                # Check if the user already has a main photo
                # If the user already has a main photo, Remove Record
                existing_main_photo = UserPhoto.query.filter_by(user_id=user_id, is_main_photo=True).first()
                
                # If the user already has a main photo, Update URL
                # Remove S3 Object  from Bucket
                if existing_main_photo and is_main_photo:
                    
                
                    # Get the old URL and filename TO Delete Old Object from S3
                    old_url = existing_main_photo.url
                    old_parsed_url = urlparse(old_url)
                    old_filename = os.path.basename(old_parsed_url.path)
                    
                    # Update the existing main photo URL and upload date
                    existing_main_photo.url = file_url
                    existing_main_photo.upload_date = datetime.now(timezone.utc)
                    db.session.commit()
                    
                    # Delete Old Object from S3
                    file_path = self._make_file_path(user_id=user_id, file_name=old_filename, folder=folder)
                    super().delete_file(file_path)
                    return file_url
                
                # LIMITS 1 GALLERY PHOTO
                # If the user already has a gallery photo, Update URL and Upload_date
                TESTING_EXISTING_GALLERY_PHOTO = UserPhoto.query.filter_by(user_id=user_id, is_main_photo=False).first()
                if TESTING_EXISTING_GALLERY_PHOTO and not is_main_photo:
                    
                    # Get the old URL and filename TO Delete Old Object from S3
                    old_url = TESTING_EXISTING_GALLERY_PHOTO.url
                    old_parsed_url = urlparse(old_url)
                    old_filename = os.path.basename(old_parsed_url.path)
                    
                    TESTING_EXISTING_GALLERY_PHOTO.url = file_url
                    db.session.commit()
                    
                    # Delete Old Object from S3
                    file_path = self._make_file_path(user_id=user_id, file_name=old_filename, folder=folder)
                    super().delete_file(file_path)
                    return file_url
                
                
                # Save to PostgreSQL
                new_photo = UserPhoto(
                    user_id=user_id, 
                    url=file_url,
                    is_main_photo=is_main_photo,
                    title=title,
                    description=description
                )
                
                db.session.add(new_photo)
                db.session.commit()
     
          
            return file_url
        
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return None
        except SQLAlchemyError as e:
            # Rollback the session in case of an error
            db.session.rollback()
            print(f"Error saving file to database: {e}")
            return None
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
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
        if not del_success:
            return False
        
        try:
    
            # Retrieve File URL from S3
            url = self.retrieve_file_url(user_id=user_id,file_name=file_name,folder=folder)
            
            # Retrieve User Photo from DB
            user_photo = UserPhoto.query.filter(UserPhoto.user_id == user_id, UserPhoto.url == url).first()
            
            # If Photo is a Profile Main Picture, Update User Reference to Point to None IMAGE for Now
            if user_photo.is_main_photo:
                user = User.query.filter(User.user_id == user_id).first()
                user.profile_picture = EnvManager().load_env_var("DEFAULT_PROFILE_PICTURE")
                
            # Delete Photo from DB
            db.session.delete(user_photo)
            db.session.commit()
            db.session.close()
            
            return True

        except Exception as e:
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
    
    
    class PhotoManager:
        """
        A class for managing user photos.
        """
        def __init__(self):
            
            self.USER_PHOTOS_BASE_PATH = "./Data/Uploads/"
            self.USER_PHOTOS_MAIN_PATH = self.USER_PHOTOS_BASE_PATH + "MainPhotos/"
            self.USER_PHOTOS_GALLERY_PATH = self.USER_PHOTOS_BASE_PATH + "GalleryPhotos/"
            
            self.FAKE_PHOTOS_MAIN_PATH= self.USER_PHOTOS_BASE_PATH + "FakeMainPhotos/"
            self.FAKE_PHOTOS_GALLERY_PATH = self.USER_PHOTOS_BASE_PATH + "FakeGalleryPhotos/"
            
            self._validate_directories([
                self.USER_PHOTOS_BASE_PATH, 
                self.USER_PHOTOS_MAIN_PATH, 
                self.USER_PHOTOS_GALLERY_PATH,
                self.FAKE_PHOTOS_MAIN_PATH,
                self.FAKE_PHOTOS_GALLERY_PATH
                ]
            )
            
        def get_path(self,filename,is_main_photo, is_fake_photo=False):
            """Return the appropriate path based on the photo type."""
            full_path = ""
            if is_main_photo and is_fake_photo:
                full_path = self.FAKE_PHOTOS_MAIN_PATH
            elif is_main_photo:
                full_path = self.USER_PHOTOS_MAIN_PATH
            elif is_fake_photo:
                full_path = self.FAKE_PHOTOS_GALLERY_PATH
            else:
                full_path = self.USER_PHOTOS_GALLERY_PATH
          
            # Construct the full path
            full_path = os.path.join(full_path, filename)
            return full_path
        
        def _validate_directories(self, directories):
            """Validate the existence of required directories."""
            
            for directory in directories:
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    logging.info(f"PhotoManager: Directory created: {directory}")
         
        def locally_upload_user_photo(self,profile_photo, is_main_photo, is_fake_photo=False):
            """Construct the upload path for User Photo Upload file."""
                
            save_path =  self.get_path(
                filename=profile_photo.filename,
                is_main_photo=is_main_photo, 
                is_fake_photo=is_fake_photo
            )
        
            # Save the file locally
            profile_photo.save(save_path)
            profile_photo.close()
            
            logging.info(f"Profile Picture Saved Locally at: {save_path}")
            # Return the path to the saved file
            return save_path
        
        def locally_delete_user_photo(file_path):
            """Delete the locally saved user photo."""
            try:
                os.remove(file_path)
                logging.info(f"Successfully deleted User Photo: {file_path}")
                return True
            except OSError as e:
                logging.error(f"Error deleting User Photo {file_path}: {e}")
                return False