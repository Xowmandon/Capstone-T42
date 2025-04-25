from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import numpy as np

import Backend.src.models as models


class UserClusteringService():
    
    def __init__(self):
        self.df = pd.DataFrame()
        self.model = SentenceTransformer("all-MiniLM-L6-v2") # Lightweight - Small Dims
        self.embeddings = None
        
    def gen_user_dset(self):
        """
        Generate a dataset of user bios for clustering.
        
        Parameters:
            users (list): List of user objects.
        
        Returns:
            list: List of user bios.
        """
        
        # Retrieve Bios from SqlAlchemy of Users
        users = models.user.User.query.filter(models.user.User.bio != None).all()
        bios = [user.bio for user in users]
        
        # Construct DataFrame from Bios and Messages
        
        # Get All MEssages of Users, Group by User ID and Concatenate Messages
        messages = models.message.Message.query.filter(messager_id=models.user.User.id).all()
        messages_dict = {}
        for message in messages:
            if message.messager_id not in messages_dict:
                messages_dict[message.sender_id] = []
            messages_dict[message.messager_id_id].append(message.message_content)
        
        # Concatenate Messages for each User
        self.df = pd.DataFrame({
            "user_ids": [user.id for user in users],
            "bios": bios,
            "messages": [" ".join(messages_dict[user.id]) for user in users]
        })
        
        
    def embedding(self):
        """
        Generate embeddings for user bios and messages.
        
        Parameters:
            bios (list): List of user bios.
            messages (list): List of user messages.
        
        Returns:
            np.ndarray: Array of embeddings.
        """
        if self.df.empty:
            print("DataFrame is empty. Generate First...")
            
        # Concatenate Bios and Messages
        self.df["combined"] = self.df["bios"] + " " + self.df["messages"]
        
        # Generate Embeddings
        embeddings = self.model.encode(list(self.df["combined"]))
        
        return self.embeddings
        
    def cluster(self, n_clusters=None):
        """
        Cluster the user bios and messages using Agglomerative Clustering.
        
        Parameters:
            n_clusters (int): Number of clusters to form.
        
        Returns:
            list: List of cluster labels for each user.
        """
        
        # Perform Agglomerative Clustering
        clustering = AgglomerativeClustering(
            n_clusters=n_clusters, # Leave None for automatic
            distance_threshold=0.2, #
            linkage="ward", # Euclid
            
            )
        self.labels = clustering.fit_predict(self.embeddings)
        
    def label_users(self):
        
        for idx, (self.df["combined"], label) in enumerate(zip(self.df["combined"], self.labels)):
            print(f"Cluster {label}: {self.df['user_ids'][idx]}")
            # Add the label to the DataFrame
            self.df.at[idx, "cluster"] = label
            
            
    def _group_users_by_label(self):
        """
        Group users by their cluster labels.
        
        Returns:
            dict: Dictionary of clusters with user IDs.
        """
        clusters = {}
        
        for idx, label in enumerate(self.labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(self.df["user_ids"][idx])
            
        return clusters
    
    def get_users_clusters(self):
        # Get the user clusters
        if self.df.empty:
            print("DataFrame is empty. Generate First...")
            
        return self.group_users_by_label()


    def get_user_label(self, user_id):
        """
        Get the cluster label for a specific user.
        """
        if self.df.empty:
            print("DataFrame is empty. Generate First...")
            
        # Check if user_id exists in the DataFrame
        if user_id in self.df["user_ids"].values:
            return self.df.loc[self.df["user_ids"] == user_id, "cluster"].values[0]
        else:
            return None
        
        
