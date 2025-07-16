from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class TopProduct(BaseModel):
    product_name: str
    mention_count: int
    channels: List[str]
    
class TrendPoint(BaseModel):
    period: str
    message_count: int
    with_images: int
    
class ChannelActivity(BaseModel):
    channel_name: str
    message_count: int
    avg_message_length: float
    media_percentage: float
    top_products: List[str]
    
class MessageResult(BaseModel):
    message_id: int
    channel: str
    date: str
    message: str
    has_media: bool
    products: List[str]