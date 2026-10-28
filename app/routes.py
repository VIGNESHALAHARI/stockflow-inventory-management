from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app import db
from app.models import Organization, Product, User


main = Blueprint("main", __name__)


# HOME

@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    return redirect(url_for("main.login"))


# SIGNUP

@main.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        organization_name = request.form.get(
            "organization_name", ""
        ).strip()

        if not email or not password or not confirm_password or not organization_name:
            flash("Please complete all required fields.", "danger")
            return render_template("signup.html")

        if len(email) > 255:
            flash("Email address is too long.", "danger")
            return render_template("signup.html")

        if len(organization_name) > 150:
            flash(
                "Organization name must be 150 characters or fewer.",
                "danger",
            )
            return render_template("signup.html")

        if len(password) < 8:
            flash(
                "Password must contain at least 8 characters.",
                "danger",
            )
            return render_template("signup.html")

        # Confirm that both passwords match.
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("signup.html")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash(
                "An account with this email already exists.",
                "danger",
            )
            return render_template("signup.html")

        organization = Organization(
            name=organization_name,
            default_low_stock_threshold=5,
        )

        try:
            db.session.add(organization)
            db.session.flush()

            user = User(
                email=email,
                password_hash=generate_password_hash(password),
                organization_id=organization.id,
            )

            db.session.add(user)
            db.session.commit()

            login_user(user)

            flash("Account created successfully!", "success")
            return redirect(url_for("main.dashboard"))

        except IntegrityError:
            db.session.rollback()
            flash(
                "An account with this email may already exist.",
                "danger",
            )

        except Exception:
            db.session.rollback()
            current_app.logger.exception("Signup failed.")
            flash(
                "Unable to create your account. Please try again.",
                "danger",
            )

    return render_template("signup.html")


# LOGIN

@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


# LOGOUT

@main.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.login"))


# DASHBOARD

@main.route("/dashboard")
@login_required
def dashboard():
    organization_id = current_user.organization_id

    # Get the current user's organization.
    organization = current_user.organization

    # Count products belonging to this organization.
    total_products = Product.query.filter_by(
        organization_id=organization_id
    ).count()

    # Calculate the total quantity of inventory.
    total_quantity = (
        db.session.query(
            func.coalesce(func.sum(Product.quantity_on_hand), 0)
        )
        .filter(Product.organization_id == organization_id)
        .scalar()
    )

    # Get this organization's products.
    products = Product.query.filter_by(
        organization_id=organization_id
    ).order_by(Product.name.asc()).all()

    # Identify products that are low in stock.
    low_stock_products = [
        product for product in products if product.is_low_stock
    ]

    return render_template(
        "dashboard.html",
        organization=organization,
        total_products=total_products,
        total_quantity=total_quantity,
        low_stock_products=low_stock_products,
    )

# PRODUCT LIST

@main.route("/products")
@login_required
def products():
    organization_id = current_user.organization_id

    product_list = Product.query.filter_by(
        organization_id=organization_id
    ).order_by(Product.created_at.desc()).all()

    return render_template(
        "products.html",
        products=product_list,
    )


# GET A PRODUCT BELONGING TO THE CURRENT ORGANIZATION

def get_organization_product(product_id):
    product = Product.query.filter_by(
        id=product_id,
        organization_id=current_user.organization_id,
    ).first()

    if product is None:
        abort(404)

    return product


# VALIDATE PRODUCT FORM

def read_product_form():
    name = request.form.get("name", "").strip()
    sku = request.form.get("sku", "").strip()
    description = request.form.get("description", "").strip()

    quantity_text = request.form.get("quantity_on_hand", "0").strip()
    threshold_text = request.form.get("low_stock_threshold", "").strip()
    cost_price_text = request.form.get("cost_price", "").strip()
    selling_price_text = request.form.get("selling_price", "").strip()

    if not name:
        raise ValueError("Product name is required.")

    if len(name) > 150:
        raise ValueError("Product name must be 150 characters or fewer.")

    if not sku:
        raise ValueError("SKU is required.")

    if len(sku) > 100:
        raise ValueError("SKU must be 100 characters or fewer.")

    try:
        quantity = int(quantity_text)
    except (ValueError, TypeError):
        raise ValueError("Quantity must be a whole number.")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    # A blank threshold uses the organization's default.
    if threshold_text == "":
        threshold = None
    else:
        try:
            threshold = int(threshold_text)
        except (ValueError, TypeError):
            raise ValueError(
                "Low-stock threshold must be a whole number."
            )

        if threshold < 0:
            raise ValueError("Low-stock threshold cannot be negative.")

    if cost_price_text == "":
        cost_price = None
    else:
        try:
            cost_price = Decimal(cost_price_text)
        except (InvalidOperation, ValueError):
            raise ValueError("Cost price must be a valid number.")

        if not cost_price.is_finite() or cost_price < 0:
            raise ValueError("Cost price cannot be negative.")

    if selling_price_text == "":
        selling_price = None
    else:
        try:
            selling_price = Decimal(selling_price_text)
        except (InvalidOperation, ValueError):
            raise ValueError("Selling price must be a valid number.")

        if not selling_price.is_finite() or selling_price < 0:
            raise ValueError("Selling price cannot be negative.")

    return {
        "name": name,
        "sku": sku,
        "description": description or None,
        "quantity_on_hand": quantity,
        "low_stock_threshold": threshold,
        "cost_price": cost_price,
        "selling_price": selling_price,
    }


# ADD PRODUCT

@main.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    if request.method == "POST":
        try:
            data = read_product_form()

            product = Product(
                organization_id=current_user.organization_id,
                **data,
            )

            db.session.add(product)
            db.session.commit()

            flash("Product added successfully!", "success")
            return redirect(url_for("main.products"))

        except ValueError as error:
            db.session.rollback()
            flash(str(error), "danger")

        except IntegrityError:
            db.session.rollback()
            flash(
                "This SKU already exists in your organization.",
                "danger",
            )

        except Exception:
            db.session.rollback()
            current_app.logger.exception("Adding product failed.")
            flash(
                "Unable to add the product. Please try again.",
                "danger",
            )

    return render_template(
        "product_form.html",
        product=None,
        page_title="Add Product",
    )


# EDIT PRODUCT

@main.route(
    "/products/<int:product_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_product(product_id):
    product = get_organization_product(product_id)

    if request.method == "POST":
        try:
            data = read_product_form()

            for field, value in data.items():
                setattr(product, field, value)

            db.session.commit()

            flash("Product updated successfully!", "success")
            return redirect(url_for("main.products"))

        except ValueError as error:
            db.session.rollback()
            flash(str(error), "danger")

        except IntegrityError:
            db.session.rollback()
            flash(
                "This SKU already exists in your organization.",
                "danger",
            )

        except Exception:
            db.session.rollback()
            current_app.logger.exception("Updating product failed.")
            flash(
                "Unable to update the product. Please try again.",
                "danger",
            )

    return render_template(
        "product_form.html",
        product=product,
        page_title="Edit Product",
    )


# DELETE PRODUCT

@main.route(
    "/products/<int:product_id>/delete",
    methods=["POST"],
)
@login_required
def delete_product(product_id):
    product = get_organization_product(product_id)

    try:
        db.session.delete(product)
        db.session.commit()

        flash("Product deleted successfully.", "success")

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Deleting product failed.")
        flash(
            "Unable to delete the product. Please try again.",
            "danger",
        )

    return redirect(url_for("main.products"))


# ORGANIZATION SETTINGS

@main.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    organization = current_user.organization

    if request.method == "POST":
        organization_name = request.form.get(
            "organization_name", ""
        ).strip()

        threshold_text = request.form.get(
            "default_low_stock_threshold", ""
        ).strip()

        if not organization_name:
            flash("Organization name is required.", "danger")

        elif len(organization_name) > 150:
            flash(
                "Organization name must be 150 characters or fewer.",
                "danger",
            )

        else:
            try:
                threshold = int(threshold_text)

                if threshold < 0:
                    raise ValueError

                organization.name = organization_name
                organization.default_low_stock_threshold = threshold

                db.session.commit()

                flash("Settings saved successfully!", "success")
                return redirect(url_for("main.settings"))

            except ValueError:
                db.session.rollback()
                flash(
                    "Default low-stock threshold must be a "
                    "non-negative whole number.",
                    "danger",
                )

            except Exception:
                db.session.rollback()
                current_app.logger.exception("Saving settings failed.")
                flash(
                    "Unable to save settings. Please try again.",
                    "danger",
                )

    return render_template(
        "settings.html",
        organization=organization,
    )


# HEALTH CHECK

@main.route("/health")
def health():
    return {
        "status": "ok",
        "application": "StockFlow",
    }, 200