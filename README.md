EveryWear Clothing is a simple clothing-shop website for browsing everyday T-shirts and streetwear. The site includes a home page with a promotional video, a product shop with category filters, product details and size choices, account registration and login, a shopping cart, and an About page.
Project note: This version is a front-end learning/demo project. Account information and the cart are stored in the visitor's browser using localStorage; there is no server-side database, payment gateway, or real order processing in the current implementation.

Features
- Home page with EveryWear branding and a promotional video.
- Shop page with product cards and category filters: All, Unisex, Men, Women, and Streetwear.
- Product details with descriptions, prices, size options, and product information.
- Account registration with basic checks for username, full name, email, password requirements, and password confirmation.
- Login and logout using accounts stored in the browser.
- Shopping cart with item quantities, item prices, and a total.
- Checkout demonstration that clears the cart and displays a confirmation message.
- Responsive styling for desktop, tablet, and mobile screens.
Technologies Used
- HTML
- CSS
- Python running in the browser through PyScript
- JavaScript for the navigation fallback
- Browser localStorage for demo account and cart data
- Google Fonts: Bebas Neue and Inter
Project Structure
EveryWear/
├── index.html       # Website pages, modals, forms, and page layout
├── style.css        # Styling and responsive layouts
├── main.py          # Product rendering, registration, login, cart, and UI logic
└── assets/
    ├── logo.jpeg    # EveryWear logo
    ├── ads.mp4      # Home page promotional video
    └── ...          # Product images used by the shop
Make sure the assets folder and all referenced image/video files are included in the project. File names and capitalization must match the paths in main.py and index.html.
How to Run the Website
Because the site loads PyScript and local assets, run it through a local web server instead of opening index.html directly.
Option 1: Visual Studio Code Live Server
1. Open the project folder in Visual Studio Code.
2. Install the Live Server extension if it is not already installed.
3. Right-click index.html and select Open with Live Server.
4. The website will open in your browser.
Option 2: Python's built-in web server
1. Install Python 3 if it is not already available.
2. Open a terminal in the project folder (the folder containing index.html).
3. Run:
   python -m http.server 8000
   On some systems, use python3 -m http.server 8000 instead.
4. Visit http://localhost:8000 in your browser.
5. Keep the terminal running while you use the website. Press Ctrl+C to stop the server.
The page loads PyScript and Google Fonts from external services, so an internet connection is needed for those resources.
How to Use
1. Open the website and select Shop to browse products.
2. Select a product to view its details and available size choices.
3. Create an account using Login → Create Account.
4. Log in, then add products to the cart.
5. Open Cart to review the items and total.
6. Select Checkout to test the demo checkout flow. This does not charge a payment method or create a server-side order.
7. Select Logout to end the current browser-stored login session.
Where Demo Data Is Stored
The current implementation uses the browser's localStorage:
Key	Purpose
everywear_users	Registered demo accounts
everywear_current	Username for the current login session
everywear_cart	Items currently in the shopping cart


To inspect these values in Chrome, open Developer Tools with F12, select Application, then open Local Storage and choose the website's origin. You can also inspect the registered-account list in the Console with:
JSON.parse(localStorage.getItem("everywear_users"))
Local Storage is specific to a browser and website origin. It is not a central database and usually will not follow a user to another browser or device. Clearing the browser's site data can remove these values.
Current Limitations and Security Notes
- This is a demonstration project and is not ready for production e-commerce use.
- Passwords are currently stored as plain text in browser localStorage. Do not use real or reused passwords with this version.
- Browser storage can be viewed or changed by the person using that browser; client-side checks are not secure authentication.
- Accounts and cart data are not shared across devices or customers through a server database.
- Checkout only clears the cart and displays a message. It does not process payments, save orders, or arrange shipping.
- The site uses PyScript from an external CDN, so its Python code runs in the browser rather than on a private backend server.
For a more secure, multi-user version, use a backend such as Python Flask with a database such as SQLite (or another appropriate database). Store passwords using a strong password-hashing method, manage login sessions on the server, and validate registration and checkout on the backend. Use a payment provider rather than collecting payment details directly.
CONTRIBUTORS:
#TUMABANG, RICARDO
#PASUMALA,KURBY
#CATAMISAN,VALERIE
#AMPER,ALJIE
#REOYAN,AISHWARYA
