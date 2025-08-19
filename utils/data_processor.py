import json
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class DataProcessor:
    """Utility class for data processing operations"""
    
    def __init__(self):
        self.processed_count = 0
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate input data structure"""
        required_fields = ['id', 'timestamp', 'value']
        return all(field in data for field in required_fields)
    
    def process_batch(self, data_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a batch of data records"""
        processed_data = []
        
        for record in data_batch:
            if self.validate_data(record):
                processed_record = self._process_single_record(record)
                processed_data.append(processed_record)
                self.processed_count += 1
            else:
                logger.warning(f"Invalid record skipped: {record}")
        
        logger.info(f"Processed {len(processed_data)} records")
        return processed_data
    
    def _process_single_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single data record"""
        processed = {
            'id': record['id'],
            'timestamp': record['timestamp'],
            'original_value': record['value'],
            'processed_value': record['value'] * 1.1,  # Sample processing
            'status': 'processed'
        }
        
        # Add additional processing logic here
        if record['value'] > 100:
            processed['category'] = 'high'
        elif record['value'] > 50:
            processed['category'] = 'medium'
        else:
            processed['category'] = 'low'
        
        return processed
    
    def get_statistics(self) -> Dict[str, int]:
        """Get processing statistics"""
        return {
            'total_processed': self.processed_count,
            'status': 'active'
        }