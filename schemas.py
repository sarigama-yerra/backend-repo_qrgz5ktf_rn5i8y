"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Coins Guard specific schemas

class RecoveryRequest(BaseModel):
    """
    Recovery requests for lost crypto assets
    Collection name: "recoveryrequest" -> typically queried as "recoveryrequest"
    """
    name: str = Field(..., min_length=2, description="Full name of requester")
    email: EmailStr = Field(..., description="Contact email")
    wallet_type: str = Field(..., description="Wallet/Exchange/Chain type")
    asset: str = Field(..., description="Asset or Token (e.g., BTC, ETH)")
    amount: Optional[str] = Field(None, description="Approximate amount")
    incident_type: str = Field(..., description="Type of incident (Phishing, Seed verloren, Betrug, Technischer Fehler, Sonstiges)")
    details: str = Field(..., min_length=10, description="Kurzbeschreibung des Vorfalls")
    contact_preference: Optional[str] = Field(None, description="Phone/Email/Telegram etc.")

class ContactMessage(BaseModel):
    """
    General contact messages
    Collection name: "contactmessage"
    """
    name: str = Field(..., min_length=2, description="Name")
    email: EmailStr = Field(..., description="Email")
    message: str = Field(..., min_length=5, description="Nachricht")
