from src.database_adapter import db_adapter, get_collection as get_adapter_collection
import logging

logger = logging.getLogger(__name__)

class Database:
    """Legacy Database class for backward compatibility"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Use the new database adapter
        pass
    
    def connect(self):
        """Connect using the new database adapter"""
        # Connection is handled automatically by the adapter
        logger.info("Database connection handled by adapter")
    
    def get_database(self):
        """Get the database instance"""
        if db_adapter.is_connected():
            return "connected"
        return None
    
    def get_collection(self, collection_name):
        """Get a specific collection"""
        return get_adapter_collection(collection_name)
    
    def close_connection(self):
        """Close the database connection"""
        db_adapter.close()
        logger.info("Database connection closed")

# Global database instance for backward compatibility
db_instance = Database()

def get_db():
    """Get the global database instance"""
    return db_instance.get_database()

def get_collection(collection_name):
    """Get a specific collection from the global database instance"""
    return db_instance.get_collection(collection_name)

