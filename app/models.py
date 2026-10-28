from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import CheckConstraint, UniqueConstraint

from app import db


class Organization(db.Model):
    __tablename__ = "organizations"

    __table_args__ = (
        CheckConstraint(
            "default_low_stock_threshold >= 0",
            name="check_default_threshold_nonnegative",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(150),
        nullable=False,
    )

    default_low_stock_threshold = db.Column(
        db.Integer,
        nullable=False,
        default=5,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    users = db.relationship(
        "User",
        back_populates="organization",
    )

    products = db.relationship(
        "Product",
        back_populates="organization",
        cascade="all, delete-orphan",
    )


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    organization_id = db.Column(
        db.Integer,
        db.ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    organization = db.relationship(
        "Organization",
        back_populates="users",
    )


class Product(db.Model):
    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "sku",
            name="unique_sku_per_organization",
        ),
        CheckConstraint(
            "quantity_on_hand >= 0",
            name="check_quantity_nonnegative",
        ),
        CheckConstraint(
            "low_stock_threshold IS NULL "
            "OR low_stock_threshold >= 0",
            name="check_product_threshold_nonnegative",
        ),
        CheckConstraint(
            "cost_price IS NULL OR cost_price >= 0",
            name="check_cost_price_nonnegative",
        ),
        CheckConstraint(
            "selling_price IS NULL OR selling_price >= 0",
            name="check_selling_price_nonnegative",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    organization_id = db.Column(
        db.Integer,
        db.ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    name = db.Column(
        db.String(150),
        nullable=False,
    )

    sku = db.Column(
        db.String(100),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    quantity_on_hand = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    cost_price = db.Column(
        db.Numeric(12, 2),
        nullable=True,
    )

    selling_price = db.Column(
        db.Numeric(12, 2),
        nullable=True,
    )

    # None means use the organization's default threshold.
    low_stock_threshold = db.Column(
        db.Integer,
        nullable=True,
        default=None,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    organization = db.relationship(
        "Organization",
        back_populates="products",
    )

    @property
    def effective_low_stock_threshold(self):
        """
        Use the product threshold when specified.
        Otherwise, use the organization's default threshold.
        """
        if self.low_stock_threshold is not None:
            return self.low_stock_threshold

        return self.organization.default_low_stock_threshold

    @property
    def is_low_stock(self):
        """
        A product is low on stock when its quantity
        is less than or equal to its effective threshold.
        """
        return (
            self.quantity_on_hand
            <= self.effective_low_stock_threshold
        )