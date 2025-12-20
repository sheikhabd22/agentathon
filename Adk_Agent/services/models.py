"""
Unified semantic models for Customer 360, Order 360, etc.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Customer360:
    """360-degree customer view."""
    id: str
    name: str
    segment: str
    last_order_date: Optional[datetime]
    total_spend: float
    order_count: int = 0
    avg_order_value: float = 0.0
    lifecycle_status: str = "active"  # active, at-risk, churned
    ltv_score: float = 0.0
    engagement_score: float = 0.0

@dataclass
class Order360:
    """360-degree order view."""
    id: str
    customer_id: str
    date: datetime
    amount: float
    status: str
    items: List[str]  # SKUs
    payment_status: str = "pending"
    fulfillment_status: str = "pending"
    channel: str = "unknown"  # web, mobile, retail

@dataclass
class Invoice360:
    """360-degree invoice view."""
    id: str
    customer_id: str
    order_id: Optional[str]
    amount: float
    status: str
    due_date: datetime
    payment_date: Optional[datetime] = None
    days_outstanding: int = 0

@dataclass
class Product360:
    """360-degree product view."""
    sku: str
    name: str
    category: str
    price: float
    inventory_qty: int = 0
    ytd_sales: float = 0.0
    margin_pct: float = 0.0
