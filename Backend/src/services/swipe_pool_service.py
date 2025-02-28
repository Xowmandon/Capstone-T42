"""Author: Joshua Ferguson

Service for Generating and Caching Potential Matches in a Redis DB, to be retrieved and used by the Client
TODO - Testing and Validating Swipe Pool Generation and Cache

"""

import json, asyncio
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager

from Backend.src.extensions import db, redis_client # Import the DB Instance
from Backend.src.models.user import User
from Backend.src.models.swipe import Swipe
from datetime import datetime, timedelta

SWIPE_POOL_ENSURED_SIZE = 100

class SwipePoolService:
    """
    Service class for managing the swipe pool and potential matches for a user.
    """

    def __init__(self):
        self.setup_routes()
        
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
        user = User.query.get(user_id)
        if not user:
            return []
        
        active_date = datetime.now() - timedelta(weeks=2)
        
        # Raw, Basic Potential Matchmaking, filtered over Minimal Discriminants
        # Each Potential Also Has Dating Preferences matching Current User (Age, Location, Etc)
        potential_matches = User.query.filter(
            User.id != user_id, # Cannot Swipe on Themselves
            
            # TODO - Change to Dating Preferences Class - Ensure Matched User Schema 
            User.gender == user.interested_in, # Potential and Current User are interested in each other's Gender
            User.interested_in == user.gender,
            
            User.age >= user.min_age, # Current User is within Age Range of Potential
            User.age <= user.max_age,
            User.min_age <= user.age,  # Potential Match is within Age Range of Current User
            User.max_age >= user.age,
            
            User.state == user.state, # Same State
            User.city == user.city, # Cities Match
            
            User.last_active >= active_date # Ensure User has been Active in the Last Two Weeks From Current Date
            
        ).order_by(db.func.random()).limit(limit).all()
        
        for potentials, idx in enumerate(potential_matches):
            swiper_swipe_exists = Swipe.query.filter_by(swiper_id=user_id, swipee_id=potentials.id).first()
            swipee_swipe_exists = Swipe.query.filter_by(swiper_id=potentials.id, swipee_id=user_id).first()
            
            if swiper_swipe_exists or (swipee_swipe_exists and swipee_swipe_exists.swipe_result == "REJECTED"):
                potential_matches.pop(idx)

        return User.users_schema.dump(potential_matches)
    
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


