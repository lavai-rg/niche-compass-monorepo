"""
Base Model with common helper methods for database operations
Compatible with both MongoDB and TinyDB via database adapter
"""

from datetime import datetime

class BaseModel:
    """Base model with common database operation helpers"""
    
    @staticmethod
    def format_datetime(dt):
        """Format datetime for JSON serialization"""
        if dt is None:
            return None
        if isinstance(dt, str):
            return dt
        return dt.isoformat() if hasattr(dt, 'isoformat') else str(dt)
    
    @staticmethod
    def find_all_with_pagination(collection, limit=20, skip=0, sort_field=None, sort_desc=True):
        """Get all items with pagination and sorting"""
        all_items = collection.find({})
        
        # Convert to list for sorting
        items_list = list(all_items)
        
        # Sort if sort_field is provided
        if sort_field and items_list:
            try:
                items_list.sort(
                    key=lambda x: x.get(sort_field, 0) or 0, 
                    reverse=sort_desc
                )
            except (TypeError, KeyError):
                pass  # Skip sorting if field doesn't exist or can't be sorted
        
        # Apply pagination
        start_idx = skip
        end_idx = start_idx + limit
        return items_list[start_idx:end_idx]
    
    @staticmethod
    def find_by_field(collection, field_name, value, limit=None):
        """Find items by a specific field value"""
        items = collection.find({field_name: value})
        items_list = list(items)
        
        if limit:
            return items_list[:limit]
        return items_list
    
    @staticmethod
    def search_by_text(collection, search_fields, query, limit=20, sort_field=None):
        """Search items by text in multiple fields"""
        all_items = collection.find({})
        filtered_items = []
        query_lower = query.lower()
        
        for item in all_items:
            # Check if query matches any of the search fields
            for field in search_fields:
                field_value = str(item.get(field, '')).lower()
                if query_lower in field_value:
                    filtered_items.append(item)
                    break  # Found match, no need to check other fields
        
        # Sort if sort_field is provided
        if sort_field and filtered_items:
            try:
                filtered_items.sort(
                    key=lambda x: x.get(sort_field, 0) or 0, 
                    reverse=True
                )
            except (TypeError, KeyError):
                pass
        
        return filtered_items[:limit]
    
    @staticmethod
    def filter_by_field_values(collection, field_name, allowed_values, limit=20, sort_field=None):
        """Filter items where field value is in allowed_values list"""
        all_items = collection.find({})
        filtered_items = []
        
        for item in all_items:
            if item.get(field_name) in allowed_values:
                filtered_items.append(item)
        
        # Sort if sort_field is provided
        if sort_field and filtered_items:
            try:
                filtered_items.sort(
                    key=lambda x: x.get(sort_field, 0) or 0, 
                    reverse=True
                )
            except (TypeError, KeyError):
                pass
        
        return filtered_items[:limit]