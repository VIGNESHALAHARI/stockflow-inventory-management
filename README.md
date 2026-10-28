StockFlow – Inventory Management System

StockFlow is a lightweight inventory management web application built with Python and Flask. It helps small businesses manage products, track stock quantities, and identify items that need restocking.

The application provides a dashboard for monitoring inventory, product search and management, and organization-level settings. Each organization manages its own products, keeping inventory data separated between accounts.

This project was developed as part of a Software Development Engineer Intern assessment to demonstrate practical skills in backend development, database management, authentication, and CRUD operations.

Features

1. User Authentication

- Register with an email address, password, and organization name.
- Log in and log out.
- Protect application pages that require authentication.
- Store passwords as hashes rather than plain text.

2. Organization-Based Inventory

- Create an organization during registration.
- Associate each user with an organization.
- Restrict product operations to the logged-in user's organization.
- Allow different organizations to use the same SKU independently.

3. Product Management

Create, view, update, search, and delete products.

Each product supports:

- Product name and SKU
- Description
- Available quantity
- Cost price and selling price
- Optional product-specific low-stock threshold
- Creation and last-updated timestamps

Product names and SKUs are required, quantities and thresholds cannot be negative, and duplicate SKUs are not allowed within the same organization.

4. Inventory Dashboard

The dashboard provides a quick overview of inventory, including:

- Total number of products
- Total units in stock
- Low-stock products
- Product names, SKUs, quantities, and applicable thresholds for items requiring attention

5. Low-Stock Monitoring

StockFlow identifies products whose available quantity is less than or equal to their effective low-stock threshold.

Each product can have its own threshold. If no product-specific threshold is configured, the organization's default threshold is used.

Example: If a product has 8 units in stock and its threshold is 10, it appears in the low-stock list.

6. Product Search

Search the product list by product name or SKU to find inventory items quickly.

7. Organization Settings

- Update the organization name.
- Configure the default low-stock threshold.
- Apply the default threshold to products without an individual threshold.

8. Input Validation

The application validates submitted data and handles common errors, including missing required fields, invalid quantities, invalid prices, negative thresholds, and duplicate SKUs within an organization.

---

Technology Stack

Technology| Purpose
Python| Main programming language
Flask| Web application framework
Flask-Login| Authentication and session management
Flask-SQLAlchemy| Database integration
SQLAlchemy| Database models, relationships, and queries
SQLite| Local development database
Jinja2| Dynamic HTML template rendering
HTML5| Web page structure
Bootstrap| UI components and responsive styling, where used
CSS| Page styling
JavaScript| Client-side interactions, where used
python-dotenv| Loading environment variables from ".env"

Project Structure

stockflow-inventory-management/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── signup.html
│       ├── dashboard.html
│       ├── products.html
│       ├── product_form.html
│       └── settings.html
├── config.py
├── requirements.txt
├── run.py
├── .gitignore
└── README.md

The ".env" file, virtual environment, and local database are excluded from version control. The database may be created automatically when the application initializes.

Getting Started

Follow these steps to run StockFlow locally.

Prerequisites

Install:

- Python 3.10 or later
- pip
- Git
- Visual Studio Code or another code editor (optional)

1. Clone the Repository

git clone https://github.com/VIGNESHALAHARI/stockflow-inventory-management.git
cd stockflow-inventory-management

If the repository is already cloned, open the project directory in your terminal instead.

2. Create a Virtual Environment

Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

If PowerShell blocks activation for the current session, run:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

Then activate the virtual environment again.

macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies

python -m pip install -r requirements.txt

4. Configure Environment Variables

Create a ".env" file in the project root and configure a secret key:

SECRET_KEY=replace-with-a-strong-random-secret

Use a strong, randomly generated value. Never commit your actual ".env" file or expose your secret key publicly.

For local development, StockFlow uses SQLite by default.

5. Run the Application

From the project root, execute:

python run.py

Open your browser and visit:

http://127.0.0.1:5000

The application initializes its database tables when it starts, if they do not already exist.

6. Create an Account

1. Open the signup page.
2. Enter your email address and password.
3. Provide an organization name.
4. Complete registration and log in.
5. Start adding and managing products.

Using StockFlow

Add a Product

Open the Products page and select the option to add a product. Enter its name, SKU, and quantity. You can also provide a description, prices, and a custom low-stock threshold.

Update Inventory

Open an existing product, change its quantity or other details, and save your changes.

Search Products

Use the search field to find products by name or SKU.

Monitor Low Stock

Check the dashboard for products whose quantities have reached or fallen below their effective thresholds.

Change Organization Settings

Open Settings to update the organization name or default low-stock threshold.

Delete a Product

Select the delete action for the relevant product and confirm the deletion when prompted.

Database Design

StockFlow uses three main models.

Model| Purpose
"Organization"| Stores the organization name and default low-stock threshold.
"User"| Stores account details, password hashes, and the associated organization.
"Product"| Stores product information, quantities, pricing, thresholds, and timestamps.

Each product belongs to an organization. SKU uniqueness is enforced within an organization rather than across the entire application.

Security and Validation

The application includes several basic safeguards:

- Passwords are stored as hashes.
- Authentication is required for protected pages.
- Product operations are scoped to the current user's organization.
- Required fields are validated.
- Negative quantities and thresholds are rejected.
- Prices are validated when provided.
- Duplicate SKUs within an organization are rejected.
- Environment files and local database files are excluded from Git.

These safeguards support the scope of this assessment. Additional security review and production configuration would be necessary before using the application with sensitive business data.

Scope and Limitations

StockFlow focuses on the core inventory management requirements of the assessment.

The current scope does not include:

- Multiple warehouse or inventory locations
- Purchase orders or supplier management
- Stock movement history
- Advanced user roles and permissions
- Billing or external integrations

The application uses SQLite for local development. A deployed version must use a database configuration suitable for its hosting environment and data-persistence requirements.

Future Improvements

Potential improvements include:

- Automated tests for authentication and inventory operations
- Pagination for larger product lists
- Advanced search and filtering
- Stock movement history
- CSV import and export
- Support for multiple users per organization
- Production logging and monitoring

These are possible future enhancements and are not represented as existing features.

What This Project Demonstrates

StockFlow brings together several practical web development concepts:

- Building web routes with Flask
- Managing authentication and sessions
- Designing relational database models
- Implementing CRUD operations
- Validating user input
- Separating organization-specific data
- Calculating and displaying inventory metrics

The goal is to provide a simple, usable inventory management application while demonstrating how these components work together in a real project.

Author

Alahari Govinda Sai Vigneswar

Software Development Engineer Intern Candidate

GitHub: https://github.com/VIGNESHALAHARI

License

Developed for a software development assessment. No open-source license has been specified.