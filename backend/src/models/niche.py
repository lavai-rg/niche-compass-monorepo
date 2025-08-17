from datetime import datetime
from bson import ObjectId
from src.database import get_collection
from src.config import Config
from src.models.base_model import BaseModel

class Niche(BaseModel):
    def __init__(self, name, category=None, description=None, trend_data=None, 
                 competition_score=None, demand_score=None, visual_analysis=None,
                 top_products=None, price_analysis=None, created_at=None, updated_at=None, _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.category = category
        self.description = description
        self.trend_data = trend_data or {}
        self.competition_score = competition_score  # 1-100 scale
        self.demand_score = demand_score  # 1-100 scale
        self.visual_analysis = visual_analysis or {}
        self.top_products = top_products or []
        self.price_analysis = price_analysis or {}
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            '_id': str(self._id),
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'trend_data': self.trend_data,
            'competition_score': self.competition_score,
            'demand_score': self.demand_score,
            'visual_analysis': self.visual_analysis,
            'top_products': self.top_products,
            'price_analysis': self.price_analysis,
            'created_at': self.format_datetime(self.created_at),
            'updated_at': self.format_datetime(self.updated_at)
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Niche instance from dictionary"""
        return cls(
            _id=data.get('_id'),
            name=data.get('name'),
            category=data.get('category'),
            description=data.get('description'),
            trend_data=data.get('trend_data', {}),
            competition_score=data.get('competition_score'),
            demand_score=data.get('demand_score'),
            visual_analysis=data.get('visual_analysis', {}),
            top_products=data.get('top_products', []),
            price_analysis=data.get('price_analysis', {}),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def save(self):
        """Save niche to database"""
        collection = get_collection(Config.COLLECTION_NICHES)
        if collection is None:
            return None
            
        self.updated_at = datetime.utcnow()
        data = self.to_dict()
        data['_id'] = self._id
        
        result = collection.replace_one(
            {'_id': self._id},
            data,
            upsert=True
        )
        return result
    
    @classmethod
    def find_by_id(cls, niche_id):
        """Find niche by ID"""
        collection = get_collection(Config.COLLECTION_NICHES)
        if collection is None:
            return None
            
        data = collection.find_one({'_id': ObjectId(niche_id)})
        if data:
            return cls.from_dict(data)
        return None
    
    @classmethod
    def find_by_name(cls, name):
        """Find niche by name"""
        collection = get_collection(Config.COLLECTION_NICHES)
        if collection is None:
            return None
        
        # Try exact match first
        data = collection.find_one({'name': name})
        if data:
            return cls.from_dict(data)
        
        # Try partial match using search helper
        matches = cls.search_by_text(collection, ['name'], name, limit=1)
        if matches:
            return cls.from_dict(matches[0])
        
        return None
    
    @classmethod
    def find_all(cls, limit=50, skip=0):
        """Find all niches with pagination"""
        collection = get_collection(Config.COLLECTION_NICHES)
        if collection is None:
            return []
        
        # Use BaseModel helper for pagination and sorting
        data_list = cls.find_all_with_pagination(collection, limit, skip, 'updated_at', True)
        return [cls.from_dict(data) for data in data_list]
    
    @classmethod
    def search_by_category(cls, category, limit=20):
        """Search niches by category"""
        collection = get_collection(Config.COLLECTION_NICHES)
        if collection is None:
            return []
        
        # Use BaseModel helper for text search
        data_list = cls.search_by_text(collection, ['category'], category, limit, 'competition_score')
        return [cls.from_dict(data) for data in data_list]
    
    def delete(self):
        """Delete niche from database"""
        collection = get_collection(Config.COLLECTION_NICHES)
        if collection is None:
            return None
            
        result = collection.delete_one({'_id': self._id})
        return result

