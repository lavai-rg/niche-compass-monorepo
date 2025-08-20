"""
Database Adapter for Niche Compass
Supports both TinyDB (local development) and MongoDB (production)
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from bson import ObjectId
import json

logger = logging.getLogger(__name__)

class DatabaseAdapter:
    """Database adapter that works with both TinyDB and MongoDB"""
    
    def __init__(self):
        self.db_type = None
        self.db = None
        self.client = None
        self._setup_database()
    
    def _setup_database(self):
        """Setup database connection based on available options"""
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        connection_string = os.getenv('COSMOS_DB_CONNECTION_STRING')
        
        # Try MongoDB first (production)
        if connection_string and self._is_valid_connection_string(connection_string):
            try:
                self._setup_mongodb(connection_string)
                return
            except Exception as e:
                logger.warning(f"MongoDB connection failed: {e}")
        
        # Fallback to TinyDB (development)
        logger.info("Using TinyDB for local development")
        self._setup_tinydb()
    
    def _is_valid_connection_string(self, connection_string):
        """Check if connection string is valid (not placeholder)"""
        if not connection_string:
            return False
        placeholders = ['your_password', 'YOUR_PRIMARY_KEY', 'temp_password']
        return not any(placeholder in connection_string for placeholder in placeholders)
    
    def _setup_mongodb(self, connection_string):
        """Setup MongoDB connection"""
        from pymongo import MongoClient
        
        self.client = MongoClient(
            connection_string,
            serverSelectionTimeoutMS=5000,
            ssl=True,
            retryWrites=False
        )
        
        # Test connection
        self.client.admin.command('ping')
        
        database_name = os.getenv('DATABASE_NAME', 'nichecompass')
        self.db = self.client[database_name]
        self.db_type = 'mongodb'
        
        logger.info(f"Connected to MongoDB: {database_name}")
    
    def _setup_tinydb(self):
        """Setup TinyDB for local development"""
        from tinydb import TinyDB
        
        # Use current directory for Windows compatibility
        db_path = os.path.join(os.getcwd(), 'data', 'niche_compass.json')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db = TinyDB(db_path)
        self.db_type = 'tinydb'
        
        logger.info(f"Connected to TinyDB: {db_path}")
    
    def get_collection(self, collection_name: str):
        """Get collection/table for the specified name"""
        if self.db_type == 'mongodb':
            return MongoCollection(self.db[collection_name])
        elif self.db_type == 'tinydb':
            return TinyCollection(self.db, collection_name)
        else:
            raise RuntimeError("Database not initialized")
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        try:
            if self.db_type == 'mongodb':
                self.client.admin.command('ping')
                return True
            elif self.db_type == 'tinydb':
                return self.db is not None
            return False
        except:
            return False
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
        if self.db and hasattr(self.db, 'close'):
            self.db.close()

class MongoCollection:
    """MongoDB collection wrapper"""
    
    def __init__(self, collection):
        self.collection = collection
    
    def find_one(self, query: Dict) -> Optional[Dict]:
        return self.collection.find_one(query)
    
    def find(self, query: Dict = None, limit: int = None, skip: int = None) -> List[Dict]:
        cursor = self.collection.find(query or {})
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    
    def insert_one(self, document: Dict) -> str:
        result = self.collection.insert_one(document)
        return str(result.inserted_id)
    
    def replace_one(self, filter_query: Dict, replacement: Dict, upsert: bool = False) -> Dict:
        result = self.collection.replace_one(filter_query, replacement, upsert=upsert)
        return {
            'matched_count': result.matched_count,
            'modified_count': result.modified_count,
            'upserted_id': str(result.upserted_id) if result.upserted_id else None
        }
    
    def delete_one(self, query: Dict) -> Dict:
        result = self.collection.delete_one(query)
        return {'deleted_count': result.deleted_count}
    
    def count_documents(self, query: Dict = None) -> int:
        """Count documents matching the query"""
        return self.collection.count_documents(query or {})
    
    def count(self, query: Dict = None) -> int:
        """Count documents matching the query (alias for count_documents)"""
        return self.count_documents(query or {})

class TinyCollection:
    """TinyDB table wrapper to mimic MongoDB interface"""
    
    def __init__(self, db, table_name: str):
        self.table = db.table(table_name)
    
    def find_one(self, query: Dict) -> Optional[Dict]:
        from tinydb import Query
        q = Query()
        
        # Convert MongoDB-style query to TinyDB query
        if '_id' in query:
            # Convert ObjectId string to int for TinyDB
            doc_id = self._convert_id(query['_id'])
            try:
                doc = self.table.get(doc_id=doc_id)
                if doc:
                    doc['_id'] = str(doc.doc_id)
                return doc
            except:
                return None
        
        # Handle other queries
        for key, value in query.items():
            if key == '_id':
                continue
            result = self.table.search(q[key] == value)
            if result:
                doc = result[0]
                doc['_id'] = str(doc.doc_id)
                return doc
        
        return None
    
    def find(self, query: Dict = None, limit: int = None, skip: int = None) -> List[Dict]:
        if not query:
            docs = self.table.all()
        else:
            from tinydb import Query
            q = Query()
            
            # Simple query support
            conditions = []
            for key, value in query.items():
                if key != '_id':
                    conditions.append(q[key] == value)
            
            if conditions:
                condition = conditions[0]
                for cond in conditions[1:]:
                    condition = condition & cond
                docs = self.table.search(condition)
            else:
                docs = self.table.all()
        
        # Add _id field and handle pagination
        for doc in docs:
            doc['_id'] = str(doc.doc_id)
        
        if skip:
            docs = docs[skip:]
        if limit:
            docs = docs[:limit]
        
        return docs
    
    def insert_one(self, document: Dict) -> str:
        # Remove _id if present (TinyDB auto-generates)
        doc_copy = document.copy()
        doc_copy.pop('_id', None)
        
        # Convert datetime objects to ISO strings for TinyDB
        doc_copy = self._serialize_datetime(doc_copy)
        
        doc_id = self.table.insert(doc_copy)
        return str(doc_id)
    
    def replace_one(self, filter_query: Dict, replacement: Dict, upsert: bool = False) -> Dict:
        from tinydb import Query
        
        # Serialize datetime objects
        replacement = self._serialize_datetime(replacement)
        
        if '_id' in filter_query:
            doc_id = self._convert_id(filter_query['_id'])
            try:
                existing = self.table.get(doc_id=doc_id)
                if existing:
                    self.table.update(replacement, doc_ids=[doc_id])
                    return {'matched_count': 1, 'modified_count': 1, 'upserted_id': None}
                elif upsert:
                    new_id = self.table.insert(replacement)
                    return {'matched_count': 0, 'modified_count': 0, 'upserted_id': str(new_id)}
                else:
                    return {'matched_count': 0, 'modified_count': 0, 'upserted_id': None}
            except:
                if upsert:
                    new_id = self.table.insert(replacement)
                    return {'matched_count': 0, 'modified_count': 0, 'upserted_id': str(new_id)}
                return {'matched_count': 0, 'modified_count': 0, 'upserted_id': None}
        
        # Handle other filter queries
        q = Query()
        conditions = []
        for key, value in filter_query.items():
            if key != '_id':
                conditions.append(q[key] == value)
        
        if conditions:
            condition = conditions[0]
            for cond in conditions[1:]:
                condition = condition & cond
            
            existing_docs = self.table.search(condition)
            if existing_docs:
                doc_ids = [doc.doc_id for doc in existing_docs[:1]]  # Replace only first match
                self.table.update(replacement, doc_ids=doc_ids)
                return {'matched_count': 1, 'modified_count': 1, 'upserted_id': None}
            elif upsert:
                new_id = self.table.insert(replacement)
                return {'matched_count': 0, 'modified_count': 0, 'upserted_id': str(new_id)}
        
        return {'matched_count': 0, 'modified_count': 0, 'upserted_id': None}
    
    def delete_one(self, query: Dict) -> Dict:
        if '_id' in query:
            doc_id = self._convert_id(query['_id'])
            try:
                removed = self.table.remove(doc_ids=[doc_id])
                return {'deleted_count': len(removed)}
            except:
                return {'deleted_count': 0}
        
        from tinydb import Query
        q = Query()
        
        # Handle other queries
        conditions = []
        for key, value in query.items():
            if key != '_id':
                conditions.append(q[key] == value)
        
        if conditions:
            condition = conditions[0]
            for cond in conditions[1:]:
                condition = condition & cond
            
            docs = self.table.search(condition)
            if docs:
                removed = self.table.remove(doc_ids=[docs[0].doc_id])
                return {'deleted_count': len(removed)}
        
        return {'deleted_count': 0}
        
    def delete_many(self, query: Dict) -> Dict:
        """Delete multiple documents matching the query"""
        from tinydb import Query
        q = Query()
        
        # Handle other queries
        conditions = []
        for key, value in query.items():
            if key != '_id':
                conditions.append(q[key] == value)
        
        if conditions:
            condition = conditions[0]
            for cond in conditions[1:]:
                condition = condition & cond
            
            docs = self.table.search(condition)
            if docs:
                doc_ids = [doc.doc_id for doc in docs]
                removed = self.table.remove(doc_ids=doc_ids)
                return {'deleted_count': len(removed)}
        
        return {'deleted_count': 0}
    
    def count_documents(self, query: Dict = None) -> int:
        """Count documents matching the query (MongoDB compatibility)"""
        if query is None:
            return len(self.table)
        
        from tinydb import Query
        q = Query()
        
        # Handle query conditions
        conditions = []
        for key, value in query.items():
            if key != '_id':
                conditions.append(q[key] == value)
        
        if conditions:
            condition = conditions[0]
            for cond in conditions[1:]:
                condition = condition & cond
            
            docs = self.table.search(condition)
            return len(docs)
        
        return len(self.table)
    
    def count(self, query: Dict = None) -> int:
        """Count documents matching the query (alias for count_documents)"""
        return self.count_documents(query)
    
    def _convert_id(self, id_value):
        """Convert string ID to int for TinyDB"""
        if isinstance(id_value, str):
            try:
                return int(id_value)
            except ValueError:
                # If not a number, try to extract number from ObjectId-like string
                return hash(id_value) % 1000000
        return id_value
    
    def _serialize_datetime(self, obj):
        """Recursively convert datetime objects to ISO strings"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: self._serialize_datetime(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_datetime(item) for item in obj]
        else:
            return obj

# Global database adapter instance
db_adapter = DatabaseAdapter()

def get_db_adapter():
    """Get the global database adapter instance"""
    return db_adapter

def get_collection(collection_name: str):
    """Get a collection from the global database adapter"""
    return db_adapter.get_collection(collection_name)