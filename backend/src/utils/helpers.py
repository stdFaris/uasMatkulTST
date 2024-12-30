# src/utils/helpers.py
from datetime import datetime, date
from typing import Any, Dict, List
import json

def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO 8601 string."""
    return dt.isoformat()

def parse_datetime(dt_str: str) -> datetime:
    """Parse ISO 8601 string to datetime."""
    return datetime.fromisoformat(dt_str)

def calculate_date_range(start_date: date, end_date: date) -> List[date]:
    """Calculate list of dates between start and end date."""
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

def format_price(amount: float) -> str:
    """Format price with currency symbol."""
    return f"${amount:,.2f}"

def to_camel(string: str) -> str:
    """Convert snake_case to camelCase."""
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_snake(string: str) -> str:
    """Convert camelCase to snake_case."""
    return ''.join(['_'+c.lower() if c.isupper() else c for c in string]).lstrip('_')

class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

def serialize_model(model: Any) -> Dict[str, Any]:
    """Serialize SQLAlchemy model to dictionary."""
    result = {}
    for key in model.__mapper__.c.keys():
        result[key] = getattr(model, key)
    return result