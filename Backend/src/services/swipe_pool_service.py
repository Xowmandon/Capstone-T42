"""Author: Joshua Ferguson

Service for Generating and Caching Potential Matches in a Redis DB, to be retrieved and used by the Client
TODO - Testing and Validating Swipe Pool Generation and Cache

"""

import json, asyncio
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, exists, not_, or_


from Backend.src.extensions import db, redis_client # Import the DB Instance
from Backend.src.models.user import User, UserSchema
from Backend.src.models.swipe import Swipe
from Backend.src.models.datingPreference import DatingPreference  
from datetime import datetime, timedelta

SWIPE_POOL_ENSURED_SIZE = 100
# TODO Add Pagination (Page and Page_Size) to Swipe Pool Generation
# TODO Develop Match Scoring Algorithm for Swipe Pool Generation
    # - Location Proximity
    # - Age Proximity
    # - Last Active
    # - Interests
    # - Profile Completeness
    # - Profile Picture
# END TODO

class SwipePoolService:
    """
    Service class for managing the swipe pool and potential matches for a user.
    """

    def __init__(self):
        pass
        
    async def ensure_swipe_pool(self, user_id):
        """
        Asynchronous background task to ensure the user's swipe pool remains at the desired size.
        
        Parameters:
            user_id (int): The ID of the user.
        """
        while True:
            current_size = redis_client.llen(f"swipe_pool:{user_id}")
            if current_size >= SWIPE_POOL_ENSURED_SIZE:
                break
            await self.generate_and_cache_swipe_pool(user_id, limit=(SWIPE_POOL_ENSURED_SIZE - current_size))
            await asyncio.sleep(10)
    
    def generate_swipe_pool(self, user_id, limit=20):
        """
        Generates the swipe pool and finds potential matches for the user.
        
        Parameters:
            user_id (int): The ID of the user.
            limit (int, optional): The maximum number of potential matches to generate. Defaults to 20.
        
        Returns:
            list: A list of potential matches for the user.
        """
        current_user = User.query.get(user_id)
        if not current_user:
            return []
         
        # Get current user's dating preferences
        current_user_preferences = DatingPreference.query.filter_by(user_id=user_id).first()
        if not current_user_preferences:
            return []  # If user has no preferences set, return empty list
        
        active_date = datetime.now() - timedelta(weeks=2)
        
        #----- Raw, Basic Potential Matchmaking, filtered over Minimal Discriminants-----
        
        # Check if a user has already been swiped on
        current_user_already_swiped_exists = exists().where(
            and_(Swipe.swiper_id == user_id, Swipe.swipee_id == User.id)
        )

        # Check if a user has rejected the current user
        current_user_rejected_exists = exists().where(
            and_(Swipe.swiper_id == User.id, Swipe.swipee_id == user_id, Swipe.swipe_result == "REJECTED")
        )

        # Base query for potential matches
        # filter Only Users in the Same City and State, and Active in the Last Two Weeks
        # Exclude users the current user has swiped on and users who rejected the current user
        base_query = User.query.filter(
            User.id != user_id,
            User.state_code == current_user.state_code,  # Same City and State
            User.city == current_user.city,
            #User.last_active >= active_date, # Active in the Last Two Weeks
            not_(current_user_already_swiped_exists),  # Exclude users the current user has swiped on
            not_(current_user_rejected_exists)  # Exclude users who rejected the current user
        )

        # Filtered Query for potnetial matches with Additional Dating Preferences
        filtered_query = base_query.join(DatingPreference, DatingPreference.user_id == User.id).filter(
            or_(
            current_user_preferences.interested_in == "any",
            current_user_preferences.interested_in == User.gender  # Gender interest
            ),
            or_(
            DatingPreference.interested_in == "any",
            DatingPreference.interested_in == current_user.gender
            ),
            current_user_preferences.age_preference_lower <= User.age,  # Age preference Validations
            current_user_preferences.age_preference_upper >= User.age,
            DatingPreference.age_preference_lower <= current_user.age,
            DatingPreference.age_preference_upper >= current_user.age
        )

        #  Fetch Results from Filtered Query with Limit
        potential_matches = filtered_query.limit(limit).all()

        # Serialize and Return List of Potential Matches  (Users)
        schema_populated = UserSchema(many=True).dump(potential_matches)
        return schema_populated




    async def cache_swipe_pool(self, user_id, swipe_pool):
        """
        Caches the pre-computed potential swipes in Redis.
        
        Parameters:
            user_id (int): The ID of the user.
            swipe_pool (list): The list of potential swipes to cache.
        """
        pipeline = redis_client.pipeline()
        
        for match in swipe_pool:
            pipeline.lpush(f"swipe_pool:{user_id}", json.dumps(match))
            
        pipeline.expire(f"swipe_pool:{user_id}", timedelta(hours=12))
        
        await asyncio.to_thread(pipeline.execute)
    
    async def generate_and_cache_swipe_pool(self, user_id, limit=20):
        """
        Generates and caches the potential matches for the user.
        
        Parameters:
            user_id (int): The ID of the user.
            limit (int, optional): The maximum number of potential matches to generate. Defaults to 20.
        
        Returns:
            dict: A dictionary containing the status of the operation and the number of cached potential matches.
        """
        swipe_pool = self.generate_swipe_pool(user_id, limit=limit)
        if swipe_pool:
            await self.cache_swipe_pool(user_id, swipe_pool)
            
        response = {"status": "success", "swipe_pool_cached": len(swipe_pool)}
        
        return response
    
    async def get_swipe_pool(self, user_id, limit=20):
        """
        Retrieves the swipe pool for the user.
        
        Parameters:
            user_id (int): The ID of the user.
            limit (int, optional): The maximum number of users to retrieve from the swipe pool. Defaults to 20.
        
        Returns:
            dict: A dictionary containing the swipe pool for the user.
        """
        pipeline = redis_client.pipeline()
        
        pipeline.lrange(f"swipe_pool:{user_id}", 0, limit - 1)
        result = await asyncio.to_thread(pipeline.execute)
        
        selected_swipe_pool = [json.loads(user) for user in result[0]] if result[0] else []
        
        pipeline.ltrim(f"swipe_pool:{user_id}", limit, -1)  
        await asyncio.to_thread(pipeline.execute)
        
        if user_id not in self.background_tasks:
            self.background_tasks.add(user_id)
            asyncio.create_task(self.ensure_swipe_pool(user_id))
        
        return {"swipe_pool": selected_swipe_pool}


