"""
API Connector abstractions for integrating CRM, ERP, and e-commerce platforms.
Currently supports CSV; can be extended with REST/GraphQL adapters.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

class DataConnector(ABC):
    """Base class for all data connectors."""

    @abstractmethod
    def fetch_customers(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def fetch_orders(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def fetch_products(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def fetch_invoices(self) -> List[Dict[str, Any]]:
        pass


class CSVConnector(DataConnector):
    """Local CSV-based connector (default for demo)."""

    def fetch_customers(self) -> List[Dict[str, Any]]:
        df = pd.read_csv(DATA_DIR / "customers.csv")
        return df.to_dict("records")

    def fetch_orders(self) -> List[Dict[str, Any]]:
        df = pd.read_csv(DATA_DIR / "orders.csv")
        return df.to_dict("records")

    def fetch_products(self) -> List[Dict[str, Any]]:
        # Mock data if not available
        return [
            {"sku": "SKU-001", "name": "Product A", "category": "Electronics"},
            {"sku": "SKU-002", "name": "Product B", "category": "Software"},
        ]

    def fetch_invoices(self) -> List[Dict[str, Any]]:
        # Mock data
        return [
            {"invoice_id": "INV-001", "amount": 15000, "status": "overdue"},
            {"invoice_id": "INV-002", "amount": 8500, "status": "due_within_7_days"},
        ]


class SalesforceConnector(DataConnector):
    """Salesforce CRM connector (placeholder for REST API)."""

    def __init__(self, api_key: str, instance_url: str):
        self.api_key = api_key
        self.instance_url = instance_url

    def fetch_customers(self) -> List[Dict[str, Any]]:
        # TODO: Implement Salesforce API call
        pass

    def fetch_orders(self) -> List[Dict[str, Any]]:
        pass

    def fetch_products(self) -> List[Dict[str, Any]]:
        pass

    def fetch_invoices(self) -> List[Dict[str, Any]]:
        pass


class ShopifyConnector(DataConnector):
    """Shopify e-commerce connector (placeholder for REST API)."""

    def __init__(self, api_key: str, store_url: str):
        self.api_key = api_key
        self.store_url = store_url

    def fetch_customers(self) -> List[Dict[str, Any]]:
        # TODO: Implement Shopify API call
        pass

    def fetch_orders(self) -> List[Dict[str, Any]]:
        pass

    def fetch_products(self) -> List[Dict[str, Any]]:
        pass

    def fetch_invoices(self) -> List[Dict[str, Any]]:
        pass


class SchemaMapper:
    """Unified semantic model via schema matching and entity resolution."""

    @staticmethod
    def normalize_customer(raw_customer: Dict[str, Any]) -> Dict[str, Any]:
        """Map any customer format to unified model."""
        return {
            "id": raw_customer.get("customer_id") or raw_customer.get("id"),
            "name": raw_customer.get("customer_name") or raw_customer.get("name"),
            "segment": raw_customer.get("segment", "unknown"),
            "last_order_date": raw_customer.get("last_order_date"),
            "total_spend": raw_customer.get("total_spend", 0.0),
        }

    @staticmethod
    def normalize_order(raw_order: Dict[str, Any]) -> Dict[str, Any]:
        """Map any order format to unified model."""
        return {
            "id": raw_order.get("order_id") or raw_order.get("id"),
            "customer_id": raw_order.get("customer_id"),
            "date": raw_order.get("date") or raw_order.get("order_date"),
            "amount": raw_order.get("order_value") or raw_order.get("amount"),
            "status": raw_order.get("status", "completed"),
        }

    @staticmethod
    def normalize_product(raw_product: Dict[str, Any]) -> Dict[str, Any]:
        """Map any product format to unified model."""
        return {
            "sku": raw_product.get("sku"),
            "name": raw_product.get("name"),
            "category": raw_product.get("category"),
            "price": raw_product.get("price", 0.0),
        }

    @staticmethod
    def normalize_invoice(raw_invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Map any invoice format to unified model."""
        return {
            "id": raw_invoice.get("invoice_id") or raw_invoice.get("id"),
            "customer_id": raw_invoice.get("customer_id"),
            "amount": raw_invoice.get("amount", 0.0),
            "status": raw_invoice.get("status", "pending"),
            "due_date": raw_invoice.get("due_date"),
        }


# Global connector (pluggable)
_connector: DataConnector = CSVConnector()

def set_connector(connector: DataConnector):
    """Allow swapping connectors at runtime."""
    global _connector
    _connector = connector

def get_connector() -> DataConnector:
    return _connector
