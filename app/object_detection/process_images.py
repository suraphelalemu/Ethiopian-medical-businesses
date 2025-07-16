import os
import json
from ultralytics import YOLO
from PIL import Image
import psycopg2
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.model = YOLO(os.getenv('YOLO_MODEL_PATH', 'yolov8n.pt'))
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
    def process_new_images(self):
        """Process images not yet analyzed"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT file_path 
                FROM raw.telegram_images
                WHERE message_id NOT IN (
                    SELECT DISTINCT message_id 
                    FROM analytics.fct_image_detections
                )
                AND file_path LIKE '%.jpg'
            """)
            image_paths = [row[0] for row in cur.fetchall()]
            
        for img_path in image_paths:
            if not os.path.exists(img_path):
                logger.warning(f"Image not found: {img_path}")
                continue
                
            try:
                results = self.model(img_path)
                detections = []
                
                for result in results:
                    for box in result.boxes:
                        detections.append({
                            'message_id': self._extract_message_id(img_path),
                            'class_id': int(box.cls),
                            'class_name': result.names[int(box.cls)],
                            'confidence': float(box.conf),
                            'bbox': json.dumps(box.xywh.tolist())
                        })
                
                self._save_detections(detections)
                logger.info(f"Processed {img_path}: {len(detections)} detections")
                
            except Exception as e:
                logger.error(f"Error processing {img_path}: {str(e)}")
    
    def _extract_message_id(self, file_path):
        """Extract message ID from file path"""
        return int(os.path.basename(file_path).split('.')[0])
    
    def _save_detections(self, detections):
        """Save detections to database"""
        with self.conn.cursor() as cur:
            for det in detections:
                cur.execute("""
                    INSERT INTO analytics.fct_image_detections (
                        message_id, class_id, class_name, confidence, bbox
                    ) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    det['message_id'],
                    det['class_id'],
                    det['class_name'],
                    det['confidence'],
                    det['bbox']
                ))
            self.conn.commit()

if __name__ == '__main__':
    processor = ImageProcessor()
    processor.process_new_images()