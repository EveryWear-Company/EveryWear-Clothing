# EveryWear Clothing - main.py
# Handles: Register / Login / Add to Cart / Cart / Filters
# Uses browser localStorage for accounts

from js import document, localStorage, window
import json

# --- 1. PRODUCT DATA (Added 8 shirts) ---
products = [
    {"id": "1", "name": "WAKE UP Snail Tee", "price": 29.99, "img": "shirt1.jpeg", "cat": "graphic"},
    {"id": "2", "name": "Ibiza 20/06 Memory Tee", "price": 32.99, "img": "shirt2.jpeg", "cat": "graphic"},
    {"id": "3", "name": "Keep God First Tee", "price": 34.99, "img": "shirt3.jpeg", "cat": "street"},
    {"id": "4", "name": "CR7 Dedication Tee", "price": 35.99, "img": "shirt4.jpeg", "cat": "street"},
    {"id": "5", "name": "WAKE UP Snail Tee - Oversized", "price": 31.99, "img": "shirt5.png", "cat": "unisex"},
    {"id": "6", "name": "Ibiza Tee - Cream Edition", "price": 32.99, "img": "shirt6.png", "cat": "unisex"},
    {"id": "7", "name": "Keep God First - Brown", "price": 34.99, "img": "shirt7.png", "cat": "unisex"},
    {"id": "8", "name": "CR7 Legend Tee", "price": 36.99, "img": "shirt8.png", "cat": "graphic"},
]

# --- 2. STORAGE HELPERS ---
def get_users():
    data = localStorage.getItem("everywear_users")
    return json.loads(data) if data else []

def save_users(users):
    localStorage.setItem("everywear_users", json.dumps(users))

def get_current():
    return localStorage.getItem("everywear_current")

def set_current(username):
    if username:
        localStorage.setItem("everywear_current", username)
    else:
        localStorage.removeItem("everywear_current")

def get_cart():
    data = localStorage.getItem("everywear_cart")
    return json.loads(data) if data else []

def save_cart(cart):
    localStorage.setItem("everywear_cart", json.dumps(cart))

# --- 3. UI HELPERS ---
def show_toast(msg):
    t = document.getElementById("toast")
    t.innerText = msg
    t.style.display = "block"
    window.setTimeout(lambda: setattr(t.style, "display", "none"), 2000)

def update_nav():
    user = get_current()
    display = document.getElementById("user-display")
    login_btn = document.getElementById("open-login")
    logout_btn = document.getElementById("logout-btn")
    if user:
        display.innerText = f"Hi, {user} 👋"
        login_btn.style.display = "none"
        logout_btn.style.display = "block"
    else:
        display.innerText = ""
        login_btn.style.display = "block"
        logout_btn.style.display = "none"
    update_cart_count()

def update_cart_count():
    cart = get_cart()
    count = sum(item["qty"] for item in cart)
    document.getElementById("cart-count").innerText = str(count)

# --- 4. RENDER PRODUCTS ---
def render_products(filter="all"):
    grid = document.getElementById("product-grid")
    grid.innerHTML = ""
    for p in products:
        if filter != "all" and p["cat"] != filter:
            continue
        card = document.createElement("div")
        card.className = "card"
        card.innerHTML = f"""
            <img src="{p['img']}" alt="{p['name']}">
            <div class="card-body">
                <p style="font-size:11px;letter-spacing:1px;color:#888">{p['cat'].upper()}</p>
                <h3>{p['name']}</h3>
                <p class="price">${p['price']}</p>
                <button class="add-btn" data-id="{p['id']}" data-name="{p['name']}" data-price="{p['price']}" data-img="{p['img']}">Add to Cart</button>
            </div>
        """
        grid.appendChild(card)

    for btn in document.querySelectorAll(".add-btn"):
        btn.addEventListener("click", lambda e, b=btn: handle_add_to_cart(b))

def handle_add_to_cart(btn):
    # REQUIREMENT: If not logged in -> redirect to login
    if not get_current():
        show_toast("Please login to add items to your cart")
        document.getElementById("login-modal").classList.add("open")
        return

    name = btn.getAttribute("data-name")
    price = float(btn.getAttribute("data-price"))
    img = btn.getAttribute("data-img")
    pid = btn.getAttribute("data-id")

    cart = get_cart()
    found = next((i for i in cart if i["name"] == name), None)
    if found:
        found["qty"] += 1
    else:
        cart.append({"id": pid, "name": name, "price": price, "img": img, "qty": 1})

    save_cart(cart)
    update_cart_count()
    show_toast(f"{name} added to cart!")

def render_cart():
    cart = get_cart()
    container = document.getElementById("cart-items")
    container.innerHTML = ""
    total = 0
    if not cart:
        container.innerHTML = "<p style='text-align:center;color:#888;padding:20px'>Your cart is empty</p>"
    for item in cart:
        total += item["price"] * item["qty"]
        div = document.createElement("div")
        div.className = "cart-item"
        div.innerHTML = f"<img src='{item['img']}'><div><b>{item['name']}</b><br>${item['price']:.2f} x {item['qty']}</div>"
        container.appendChild(div)
    document.getElementById("cart-total").innerText = f"Total: ${total:.2f}"

# --- 5. VALIDATION ---
def validate_email(email):
    return "@" in email and "." in email and len(email) > 5

def validate_password(pw):
    # At least 8 chars, 1 uppercase, 1 number
    has_upper = any(c.isupper() for c in pw)
    has_number = any(c.isdigit() for c in pw)
    return len(pw) >= 8 and has_upper and has_number

# --- 6. REGISTER ---
def do_register(e):
    for el in document.querySelectorAll(".error"):
        el.style.display = "none"
    success = document.getElementById("reg-success")
    success.style.display = "none"

    username = document.getElementById("reg-username").value.strip()
    fullname = document.getElementById("reg-fullname").value.strip()
    email = document.getElementById("reg-email").value.strip()
    password = document.getElementById("reg-password").value
    confirm = document.getElementById("reg-confirm").value

    has_error = False
    users = get_users()

    if len(username) < 3:
        el = document.getElementById("reg-user-error")
        el.innerText = "Username must be at least 3 characters"
        el.style.display = "block"
        has_error = True
    elif any(u["username"] == username for u in users):
        el = document.getElementById("reg-user-error")
        el.innerText = "Username already taken"
        el.style.display = "block"
        has_error = True

    if not fullname:
        el = document.getElementById("reg-name-error")
        el.innerText = "Full name is required"
        el.style.display = "block"
        has_error = True

    if not validate_email(email):
        el = document.getElementById("reg-email-error")
        el.innerText = "Enter a valid email address"
        el.style.display = "block"
        has_error = True

    if not validate_password(password):
        el = document.getElementById("reg-pass-error")
        el.innerText = "Password must be 8+ chars, 1 uppercase & 1 number"
        el.style.display = "block"
        has_error = True

    if password != confirm:
        el = document.getElementById("reg-confirm-error")
        el.innerText = "Passwords do not match"
        el.style.display = "block"
        has_error = True

    if has_error:
        return

    users.append({"username": username, "fullname": fullname, "email": email, "password": password})
    save_users(users)
    success.innerText = "Account created! Please login now."
    success.style.display = "block"
    show_toast("Registration successful!")
    window.setTimeout(lambda: (document.getElementById("register-modal").classList.remove("open"), document.getElementById("login-modal").classList.add("open")), 1200)

# --- 7. LOGIN ---
def do_login(e):
    for el in document.querySelectorAll(".error"):
        el.style.display = "none"

    username = document.getElementById("login-username").value.strip()
    password = document.getElementById("login-password").value
    general = document.getElementById("login-general-error")

    if not username:
        el = document.getElementById("login-user-error")
        el.innerText = "Username required"
        el.style.display = "block"
        return
    if not password:
        el = document.getElementById("login-pass-error")
        el.innerText = "Password required"
        el.style.display = "block"
        return

    users = get_users()
    user = next((u for u in users if u["username"] == username and u["password"] == password), None)

    if user:
        set_current(username)
        update_nav()
        document.getElementById("login-modal").classList.remove("open")
        show_toast(f"Welcome, {username}!")
    else:
        general.innerText = "Invalid username or password"
        general.style.display = "block"
        general.style.textAlign = "center"
        general.style.fontWeight = "700"

# --- 8. EVENTS ---
document.getElementById("register-btn").addEventListener("click", do_register)
document.getElementById("login-btn").addEventListener("click", do_login)

document.getElementById("open-login").addEventListener("click", lambda e: document.getElementById("login-modal").classList.add("open"))
document.getElementById("close-login").addEventListener("click", lambda e: document.getElementById("login-modal").classList.remove("open"))
document.getElementById("close-register").addEventListener("click", lambda e: document.getElementById("register-modal").classList.remove("open"))

# Switch between Login <-> Register (Create Account button)
document.getElementById("to-register").addEventListener("click", lambda e: (document.getElementById("login-modal").classList.remove("open"), document.getElementById("register-modal").classList.add("open")))
document.getElementById("to-login").addEventListener("click", lambda e: (document.getElementById("register-modal").classList.remove("open"), document.getElementById("login-modal").classList.add("open")))

document.getElementById("open-cart").addEventListener("click", lambda e: (render_cart(), document.getElementById("cart-modal").classList.add("open")))
document.getElementById("close-cart").addEventListener("click", lambda e: document.getElementById("cart-modal").classList.remove("open"))
document.getElementById("logout-btn").addEventListener("click", lambda e: (set_current(None), localStorage.removeItem("everywear_cart"), update_nav(), show_toast("Logged out")))
document.getElementById("checkout-btn").addEventListener("click", lambda e: (save_cart([]), update_cart_count(), render_cart(), show_toast("Order placed! Thank you for shopping at EveryWear")))
document.getElementById("shop-now").addEventListener("click", lambda e: document.getElementById("product-grid").scrollIntoView({"behavior": "smooth"}))

for btn in document.querySelectorAll(".filter-bar button"):
    btn.addEventListener("click", lambda e, b=btn: ( [setattr(x, "className", "") for x in document.querySelectorAll(".filter-bar button")], setattr(b, "className", "active"), render_products(b.getAttribute("data-filter")) ))

# --- 9. INIT ---
render_products()
update_nav()