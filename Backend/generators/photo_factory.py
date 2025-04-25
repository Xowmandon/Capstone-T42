
import logging
import os
import random
from uuid import uuid4

import requests
import urllib

import Backend.src.models as models
from Backend.src.utils import EnvManager
from Backend.src.extensions import db
from Backend.generators.factory_helpers import construct_dicebear_api_url

class PhotoPaths:
    def __init__(self):
        
        # Base path for user photos
        self.USER_PHOTOS_BASE_PATH = "./Backend/Data/Uploads/"
        self.USER_PHOTOS_MAIN_PATH = os.path.join(self.USER_PHOTOS_BASE_PATH, "MainPhotos/")
        self.USER_PHOTOS_GALLERY_PATH = os.path.join(self.USER_PHOTOS_BASE_PATH, "GalleryPhotos/")
        self.FAKE_PHOTOS_MAIN_PATH = os.path.join(self.USER_PHOTOS_BASE_PATH, "FakeMainPhotos/")
        self.FAKE_PHOTOS_GALLERY_PATH = os.path.join(self.USER_PHOTOS_BASE_PATH, "FakeGalleryPhotos/")
        

        self._validate_directories([
            self.USER_PHOTOS_MAIN_PATH, 
            self.USER_PHOTOS_GALLERY_PATH,
            self.FAKE_PHOTOS_MAIN_PATH,
            self.FAKE_PHOTOS_GALLERY_PATH
        ])
        
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

    

class PhotoFactory:
    
    def __init__(self,image_format="svg"):
        self.image_format = image_format
        self.path_manager = PhotoPaths()
        self.dice_bear_api = "https://api.dicebear.com/9.x/"
        self.unsplash_api = "https://api.unsplash.com/search/photos"
        self.unsplash_secret = EnvManager().load_env_var("UNSPLASH_SECRET")
        self.pexels_key = EnvManager().load_env_var("PEXELS_API_KEY")
        
        
    def construct_gen_filename(self):
        return f"avatar_{str(uuid4())}.{self.image_format}"

    def locally_upload_user_photo(self,data,file_path,filename, is_main_photo, is_fake_photo=False):
        """Construct the upload path for User Photo Upload file."""
            
        save_path =  self.path_manager.get_path(
            filename=filename,
            is_main_photo=is_main_photo, 
            is_fake_photo=is_fake_photo
        )
    
        with open(file_path, "wb") as f:
            f.write(data.content)
        
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
    

    def gen_photos(self, is_main_photo, is_fake_photo=True, style='notionists-neutral',
                   seed=None, count=1) -> list:
        """Generate fake user photos using Dicebear or Unsplash."""
        local_file_paths = []

        """Generate a fake user profile with an avatar."""
        
        local_file_paths = []
        for _ in range(count):
            
            # Generate a unique filename for the photo
            filename =  self.construct_gen_filename()
            
        
            photo_url = construct_dicebear_api_url(style, seed)
            filename = f"avatar_{str(uuid4())}.{self.image_format}"
            
            filename = f"avatar_{str(uuid4())}.{self.image_format}"
            file_path = self.path_manager.get_path(
                filename=filename,
                is_main_photo=is_main_photo,
                is_fake_photo=is_fake_photo
            )
            
            try:
                # Download the photo from the URL
                response = requests.get(photo_url)
                response.raise_for_status()
                # Save the photo locally
                self.locally_upload_user_photo(
                    data=response,
                    file_path=file_path,
                    filename=filename,
                    is_main_photo=is_main_photo,
                    is_fake_photo=is_fake_photo
                )
                
            # Handle potential errors
            except requests.RequestException as e:
                logging.error(f"Error generating photo: {e}")
                return None
            except OSError as e:
                logging.error(f"Error saving photo: {e}")
                return None
            
            logging.info(f"Generated photo saved at: {file_path}")
            local_file_paths.append(file_path)
            
        # Return the list of local file paths
        return local_file_paths

    def get_unsplash_photos(self, query="8-bit landscape"):
        """Fetch a single Unsplash photo URL matching the query."""
        base_url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": 3, # 1 photos per page
            "orientation": "landscape",
            "content_filter": "high",
            "client_id": self.unsplash_key,
        }

        photo_metadatas = []
        try:
        
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Automatically throws an exception for non-200 responses
            results = response.json().get("results", [])
            
            if not results:
                logging.warning(f"No Unsplash results found for query: {query}")
                return None
                
            for result in results:
                
                tags = result["tags"]
                # Extract the first 3 tags
                tags = [tag["title"] for tag in tags[:3]]
                # Join the tags into a single string
                tags = ",".join(tags)
                photo_metadata = {
                    "url":result["urls"]["regular"],
                    "description": result[0]["description"],
                    "title": tags
                    }

                photo_metadatas.append(photo_metadata)
           
            # Return the Photo Metadata
            return photo_metadatas
        

        except requests.RequestException as e:
            print("Get Unsplash Photos Error: ", e)
            return None

    def get_pexels_photos(self,query="8-bit landscape",page=1,count=3):
        """Fetch a single photo from Pexels matching the query."""
        print("get_pexels_photos -Page: ",page)
        # Pexels API URL and headers
        base_url = "https://api.pexels.com/v1/search"
        headers = {
            "Authorization": self.pexels_key 
        }
        params = {
            "query": query,
            "per_page": count,
            "page": page,
        }

        photos_data = []
        
        try:
    
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            next_page = response.json().get("next_page", None)
            # Check if the response contains photos
            photos = response.json().get("photos", [])

            if not photos:
                logging.warning(f"No Pexels results found for query: {query}")
                return None

            for i in range(count):
                
                photo = photos[i]
                photo_metadata = {
                    "url": photo["src"]["large"],
                    "description": photo.get("alt", "No description"),
                    "title": photo.get("photographer", "Untitled")
                }

                # Add the photo metadata to the list
                photos_data.append(photo_metadata)

            # Return the list of photo metadata
            return photos_data
    
        except requests.RequestException as e:
            print(f"Error fetching Pexels photos: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def gen_gallery_photos(self,page,query="8-bit landscape", api="pexels",per_page=3) -> list:
        """Generate fake user photos using Unsplash."""
        local_file_paths = []

        try:
            
            # Fetch Unsplash photos
            if api == "pexels":
                data = self.get_pexels_photos(query,page=page,count=3)
                
                 #Convert Pexels Data to DB Photo Representations
                photos = self.pexels_data_to_db_photo(data)
                print(f"Photos: {photos}")
                # Create a List of Gallery Photo Objects
            
            # Fetch Unsplash photos
            elif api == "unsplash":
                data = self.get_unsplash_photos(query)
                
                # Create a List of Gallery Photo Objects
                photos = [models.photo.UserPhoto(
                    url=datum["url"],
                    is_main_photo=False,
                    title=datum["title"],
                    description=datum["description"] 
                ) for datum in data]
                
            else:
                raise ValueError("Invalid API specified. Use 'pexels' or 'unsplash'.")
                
            if not photos:
                print("Failed to Fetch Photos from Unsplash/Pexels")
                return None
        
            return photos

        except Exception as e:
            print(f"Error generating Gallery API photo: {e}")
            db.session.rollback()
            return None
            
    def pexels_data_to_db_photo(self,pexels_json):
        """
        Parse the JSON response from Pexels and extract relevant photo data.
        """
        photos = []
        print(f"pexels_data_to_db_photo - Pexels JSON: {pexels_json}")
        
        for data in pexels_json:
            
            
            title = "Photographed By " + data.get("photographer", "Untitled")
            photo = models.photo.UserPhoto(
                url=data["url"],
                is_main_photo=False,
                title=title,
                description=data["description"]
            )
            
            print(f"pexels_data_to_db_photo - Photo: {photo}")
            photos.append(photo)
       
        return photos
    
    


"""
for data in pexels_json.get("photos", []):
    print(f"pexels_data_to_db_photo - Data: {data}")
    photo = models.photo.Photo(
        photo_url= data["src"]["large"],
        is_main_photo=False,
        title=data["title"],
        description=("Photographed By " + data.get("photographer", "Untitled"))
    )
"""