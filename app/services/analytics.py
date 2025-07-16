from sqlalchemy.orm import Session
from ..models.schemas import TopProduct, TrendPoint
from typing import List

def get_top_products(db: Session, limit: int = 10) -> List[TopProduct]:
    query = """
        SELECT 
            UNNEST(product_mentions) AS product,
            COUNT(*) AS mentions,
            ARRAY_AGG(DISTINCT channel_name) AS channels
        FROM analytics.fct_messages
        WHERE product_mentions IS NOT NULL
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT :limit
    """
    result = db.execute(query, {'limit': limit})
    return [
        TopProduct(
            product_name=row[0],
            mention_count=row[1],
            channels=row[2]
        )
        for row in result
    ]

def get_posting_trends(db: Session, period: str = "day") -> List[TrendPoint]:
    if period == "week":
        group_expr = "TO_CHAR(date, 'YYYY-WW')"
    elif period == "month":
        group_expr = "TO_CHAR(date, 'YYYY-MM')"
    else:
        group_expr = "date::date"
        
    query = f"""
        SELECT 
            {group_expr} AS period,
            COUNT(*) AS message_count,
            SUM(CASE WHEN has_media THEN 1 ELSE 0 END) AS with_images
        FROM analytics.fct_messages
        JOIN analytics.dim_dates ON date_key = date
        GROUP BY 1
        ORDER BY 1
    """
    result = db.execute(query)
    return [
        TrendPoint(
            period=row[0],
            message_count=row[1],
            with_images=row[2]
        )
        for row in result
    ]