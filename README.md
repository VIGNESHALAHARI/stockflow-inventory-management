StockFlow – Inventory Management System

StockFlow is a simple inventory management web application built to help small businesses keep track of their products and stock levels in one place.

The idea behind this project is straightforward: business owners should be able to manage their inventory without depending on spreadsheets or manually checking every product. With StockFlow, users can add products, update quantities, monitor low-stock items, and view important inventory information from a dashboard.

I built this project as part of a software development assessment to demonstrate my understanding of Python, Flask, database management, authentication, CRUD operations, and web application development.

Features

1. User Authentication

- Create an account using an email address and password.
- Register an organization during signup.
- Log in and log out securely.
- Protect pages that require authentication.
- Store passwords as password hashes instead of plain text.

2. Organization-Based Inventory

- Each user is associated with an organization.
- Products belong to the organization that created them.
- Users can manage their own organization's inventory.
- Product queries are scoped to the logged-in user's organization to prevent access to other organizations' products.

3. Product Management

Users can create, view, update, and delete products.

Each product can contain:

- Product name
- Stock Keeping Unit (SKU)
- Description
- Quantity available
- Cost price
- Selling price
- Low-stock threshold
- Creation and last-updated timestamps

The application validates product information before saving it. For example, product names and SKUs are required, quantities cannot be negative, and duplicate SKUs are not allowed within the same organization.

4. Inventory Dashboard

The dashboard provides a quick overview of inventory, including:

- Total number of products
- Total units currently in stock
- Number of low-stock products
- A list of products that need attention

This helps users understand their current stock situation without opening every product individually.

5. Low-Stock Monitoring

StockFlow identifies products that have reached or fallen below their configured low-stock threshold.

For example, if a product has 8 units available and its threshold is 10, it appears in the low-stock list.

Users can set a threshold for an individual product. When no product-specific threshold is provided, the application uses the organization's default threshold.

6. Product Search

Users can search the product list by product name or SKU to find items more easily.

7. Organization Settings

Users can update their organization name and configure the default low-stock threshold.

This default is used for products that do not have an individual threshold configured.

8. Input Validation and Error Handling

The application validates user input and handles common problems, including:

- Missing required fields
- Invalid or negative quantities
- Invalid prices
- Negative stock thresholds
- Duplicate SKUs within an organization
- Attempts to access products belonging to another organization

Technology Stack

Technology| Purpose
Python| Main programming language
Flask| Web application framework
Flask-Login| User authentication and session management
Flask-SQLAlchemy| Database integration and ORM
SQLAlchemy| Database models, relationships, and queries
SQLite| Database for local development
Jinja2| Rendering dynamic HTML templates
HTML5| Web page structure
CSS3| Styling and layout
JavaScript| Client-side interactions
Bootstrap| Responsive UI components, where used
python-dotenv| Loading environment variables from ".env"

Project Structure

wexa Ai sde ass/
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
├── instance/
│   └── stockflow.db
├── config.py
├── requirements.txt
├── run.py
├── .env
├── .gitignore
└── README.md

Note: The ".env" file, virtual environment, and local database are excluded from Git. The structure above describes the intended project layout; optional files or folders may be absent if they have not been created.

Getting Started

Follow these steps to run StockFlow on your local machine.

Prerequisites

Install the following:

- Python 3.10 or later
- pip
- Visual Studio Code or another code editor (optional)

1. Clone the Repository

After the project has been pushed to GitHub, clone it using:

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "wexa Ai sde ass"

Replace "<YOUR_GITHUB_REPOSITORY_URL>" with your actual repository URL.

If you already have the project on your computer, open its folder in your terminal instead.

2. Create a Virtual Environment

On Windows PowerShell:

python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1

If PowerShell blocks script execution for this terminal session, run:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

Then activate the environment again.

3. Install Dependencies

python -m pip install -r requirements.txt

4. Configure Environment Variables

Create a ".env" file in the project root.

Add a secret key:

SECRET_KEY=replace-this-with-a-long-random-secret-key

Use a strong, randomly generated secret key for your own environment. Do not commit your real ".env" file or share your secret key publicly.

For local development, the application uses SQLite by default. A separate database configuration is not required for the standard local setup.

5. Start the Application

From the project root, run:

python run.py

Open your browser and visit:

http://127.0.0.1:5000

The application creates its database tables when it initializes, if they do not already exist.

6. Create an Account

1. Open the signup page.
2. Enter your email address and password.
3. Provide your organization name.
4. Complete registration.
5. Log in and start managing products.

How to Use StockFlow

Add a Product

Open the Products page and choose the option to add a product. Enter its name, SKU, quantity, and any optional pricing or threshold information.

Update Stock

Open an existing product and update its quantity or other details. Save the changes to update the inventory.

Find Products

Use the product search field to locate a product by name or SKU.

Monitor Low Stock

Open the dashboard to see products whose quantities have reached or fallen below their effective low-stock thresholds.

Change the Default Threshold

Open Settings and update the organization's default low-stock threshold. Products without their own threshold use this value.

Delete a Product

Choose the delete action for the relevant product and confirm the deletion when prompted.

Database Design

StockFlow uses three main database models.

Organization

Stores organization information, including:

- Organization ID
- Organization name
- Default low-stock threshold
- Creation timestamp

User

Stores user account information, including:

- User ID
- Email address
- Password hash
- Associated organization ID
- Creation timestamp

Product

Stores inventory information, including:

- Product ID
- Associated organization ID
- Product name and SKU
- Description
- Quantity on hand
- Cost and selling prices
- Optional product-specific low-stock threshold
- Creation and update timestamps

Each product is associated with an organization. The SKU is unique within that organization, allowing two different organizations to use the same SKU without conflicting with each other.

Validation and Data Protection

StockFlow includes several basic safeguards:

- Passwords are stored as hashes.
- Authentication is required for protected application pages.
- Product access is restricted to the logged-in user's organization.
- Product names and SKUs are required.
- Quantities and configured thresholds cannot be negative.
- Prices must be valid, non-negative numeric values when provided.
- Duplicate SKUs are rejected within an organization.
- Environment secrets and local database files are excluded from Git.

These measures are intended for a small assessment project. A production deployment would require additional security review and operational configuration.

Current Scope and Limitations

StockFlow focuses on the core inventory-management requirements.

The current design assumes one user per organization and one inventory location. It does not include advanced role management, warehouse management, stock movement history, purchase orders, supplier management, billing, or external integrations.

The project uses SQLite for local development. The database and deployment configuration should be reviewed before using the application with real business data.

Future Improvements

Possible improvements include:

- Automated tests for authentication and inventory operations
- Pagination for larger product lists
- More advanced search and filtering
- Stock movement history
- CSV import and export
- Multiple users per organization
- Improved production logging and monitoring
- Additional security hardening

These are potential future enhancements and are not claims about functionality currently implemented.

What I Learned

Working on StockFlow has helped me apply Python and Flask concepts to a practical web application. It brings together authentication, database relationships, form validation, CRUD operations, organization-based data separation, and dashboard calculations in one project.

It has also helped me understand how individual backend features work together to support a complete application.

Author

ALAHARI GOVINDA SAI VIGNESWAR

Software Development Intern Candidate

GitHub: https://github.com/VIGNESHALAHARI

License

This project was developed for a software development assessment. Add a formal open-source license only if you intend to distribute the project under that license.