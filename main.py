# EveryWear - main.py - FIXED with create_proxy
from js import document, localStorage, window, console
from pyodide.ffi import create_proxy
import json

        # -- Added 10 Shirts to the products list with descriptions and categories -- 
products = [
    {"id": "1", "name": "WAKE UP Snail Tshirt", "price": 299, "img": "assets/shirt1.jpeg", "cat": "unisex", "desc": "Oversized fit with iconic snail graphic. Premium 100% cotton. Soft, breathable and perfect for everyday wear."},
    {"id": "2", "name": "Ibiza 20/06 Memory Tshirt", "price": 199, "img": "assets/shirt2.jpeg", "cat": "men", "desc": "Vintage-inspired Ibiza graphic. Heavyweight cotton for a structured streetwear look."},
    {"id": "3", "name": "Keep God First Tshirt", "price": 359, "img": "assets/shirt3.jpeg", "cat": "streetwear", "desc": "Bold faith statement in puff print. Unisex brown tee, durable and comfortable."},
    {"id": "4", "name": "CR7 Dedication Tshirt", "price": 399, "img": "assets/shirt4.jpeg", "cat": "men", "desc": "CR7 inspired dedication design. For the fans who never stop. Limited drop."},
    {"id": "5", "name": "Sunset State Tshirt", "price": 299, "img": "assets/shirt5.png", "cat": "women", "desc": "Sunset graphic with desert vibes. Lightweight and perfect for summer."},
    {"id": "6", "name": "Warm Days", "price": 249, "img": "assets/shirt6.png", "cat": "unisex", "desc": "Minimal EveryWear logo tee. Your everyday essential."},
    {"id": "7", "name": "Slow Motion", "price": 329, "img": "assets/shirt7.png", "cat": "streetwear", "desc": "Washed brown streetwear tee. Vintage feel, modern fit."},
    {"id": "8", "name": "Bloom In Heat", "price": 279, "img": "assets/shirt8.png", "cat": "women", "desc": "Clean white graphic tee. Minimal design for maximum style."},
    {"id": "9", "name": "Golden Hour", "price": 279, "img": "assets/shirt9.png", "cat": "women", "desc": "Golden hour glow design. Soft premium cotton."},
    {"id": "10", "name": "Keep The Flow", "price": 279, "img": "assets/shirt10.png", "cat": "men", "desc": "Keep The Flow street design. Relaxed fit."},
]

selected_product = None
proxies = [] # keep proxy alive

def keep_proxy(func):
    p = create_proxy(func)
    proxies.append(p)
    return p

console.log("EveryWear PyScript Loading...")

def get_users():
    data = localStorage.getItem("everywear_users")
    return json.loads(data) if data else []
def save_users(u): localStorage.setItem("everywear_users", json.dumps(u))
def get_current(): return localStorage.getItem("everywear_current")
def set_current(n):
    if n: localStorage.setItem("everywear_current", n)
    else: localStorage.removeItem("everywear_current")
def get_cart():
    data = localStorage.getItem("everywear_cart")
    return json.loads(data) if data else []
def save_cart(c): localStorage.setItem("everywear_cart", json.dumps(c))

def show_toast(msg):
    t = document.getElementById("toast")
    t.innerText = msg
    t.style.display = "block"
    def hide(): t.style.display = "none"
    window.setTimeout(keep_proxy(hide), 2000)

def update_cart_count():
    c = get_cart()
    s = sum(i["qty"] for i in c)
    document.getElementById("cart-count").innerText = str(s)

def update_nav():
    user = get_current()
    disp = document.getElementById("user-display")
    lb = document.getElementById("open-login")
    lob = document.getElementById("logout-btn")
    if user:
        disp.innerText = f"Hi, {user}"
        lb.style.display = "none"
        lob.style.display = "block"
    else:
        disp.innerText = ""
        lb.style.display = "block"
        lob.style.display = "none"
    update_cart_count()

def show_page(page):
    document.getElementById("landing-page").style.display = "none"
    document.getElementById("shop-page").style.display = "none"
    document.getElementById("about-page").style.display = "none"
    target = document.getElementById(page)
    if target: target.style.display = "block"
    window.scrollTo(0, 0)

def safe_bind(id, event, func):
    el = document.getElementById(id)
    if el: el.addEventListener(event, keep_proxy(func))

def handle_add_to_cart_from_data(name, price, img, pid):
    if not get_current():
        show_toast("Please login to add items to your cart")
        document.getElementById("login-modal").classList.add("open")
        return False
    cart = get_cart()
    found = next((i for i in cart if i["name"] == name), None)
    if found: found["qty"] += 1
    else: cart.append({"id": pid, "name": name, "price": price, "img": img, "qty": 1})
    save_cart(cart)
    update_cart_count()
    show_toast(name + " added to cart!")
    return True

def render_cart():
    cart = get_cart()
    con = document.getElementById("cart-items")
    con.innerHTML = ""
    total = 0
    if len(cart) == 0:
        con.innerHTML = "<p style='text-align:center;color:#888;padding:20px'>Your cart is empty</p>"
    else:
        for item in cart:
            total += item["price"] * item["qty"]
            div = document.createElement("div")
            div.className = "cart-item"
            div.innerHTML = f"<img src='{item['img']}'><div><b>{item['name']}</b><br>₱{item['price']} x {item['qty']}</div>"
            con.appendChild(div)
    document.getElementById("cart-total").innerText = f"Total: ₱{total:.2f}"

def open_product(event):
    global selected_product
    card = event.currentTarget
    pid = card.getAttribute("data-id")
    for p in products:
        if p["id"] == pid:
            selected_product = p
            break
    if selected_product:
        document.getElementById("p-img").src = selected_product["img"]
        document.getElementById("p-cat").innerText = selected_product["cat"].upper()
        document.getElementById("p-name").innerText = selected_product["name"]
        document.getElementById("p-price").innerText = f"₱{selected_product['price']}"
        document.getElementById("p-desc").innerText = selected_product["desc"]
        document.getElementById("product-modal").classList.add("open")

def on_add_click(e):
    e.stopPropagation()
    btn = e.currentTarget
    handle_add_to_cart_from_data(btn.getAttribute("data-name"), float(btn.getAttribute("data-price")), btn.getAttribute("data-img"), btn.getAttribute("data-id"))

def on_filter_click(e):
    b = e.currentTarget
    for x in document.querySelectorAll(".filter-bar button"): x.className = ""
    b.className = "active"
    render_products(b.getAttribute("data-filter"))

def render_products(filter_name="all"):
    grid = document.getElementById("product-grid")
    grid.innerHTML = ""
    for p in products:
        if filter_name != "all" and p["cat"] != filter_name: continue
        card = document.createElement("div")
        card.className = "card"
        card.setAttribute("data-id", p["id"])
        card.innerHTML = f"""
            <img src="{p['img']}" alt="{p['name']}" onerror="this.src='https://via.placeholder.com/500?text=EveryWear'">
            <div class="card-body">
                <p style="font-size:11px;letter-spacing:1px;color:#888">{p['cat'].upper()}</p>
                <h3>{p['name']}</h3>
                <p class="price">₱{p['price']}</p>
                <button class="add-btn" data-id="{p['id']}" data-name="{p['name']}" data-price="{p['price']}" data-img="{p['img']}">Add to Cart</button>
            </div>
        """
        card.addEventListener("click", keep_proxy(open_product))
        grid.appendChild(card)
    for btn in document.querySelectorAll(".add-btn"):
        btn.addEventListener("click", keep_proxy(on_add_click))

def validate_email(e): return "@" in e and "." in e and len(e) > 5
def validate_password(pw):
    has_upper = any(c.isupper() for c in pw)
    has_number = any(c.isdigit() for c in pw)
    return len(pw) >= 8 and has_upper and has_number

def do_register(e):
    for el in document.querySelectorAll(".error"): el.style.display = "none"
    s = document.getElementById("reg-success"); s.style.display = "none"
    u = document.getElementById("reg-username").value.strip()
    fn = document.getElementById("reg-fullname").value.strip()
    em = document.getElementById("reg-email").value.strip()
    pw = document.getElementById("reg-password").value
    cf = document.getElementById("reg-confirm").value
    err = False; users = get_users()
    if len(u) < 3:
        el=document.getElementById("reg-user-error"); el.innerText="Username must be at least 3 characters"; el.style.display="block"; err=True
    elif any(x["username"]==u for x in users):
        el=document.getElementById("reg-user-error"); el.innerText="Username already taken"; el.style.display="block"; err=True
    if not fn: el=document.getElementById("reg-name-error"); el.innerText="Full name is required"; el.style.display="block"; err=True
    if not validate_email(em): el=document.getElementById("reg-email-error"); el.innerText="Enter a valid email"; el.style.display="block"; err=True
    if not validate_password(pw): el=document.getElementById("reg-pass-error"); el.innerText="Password must be 8+ chars, 1 uppercase & 1 number"; el.style.display="block"; err=True
    if pw != cf: el=document.getElementById("reg-confirm-error"); el.innerText="Passwords do not match"; el.style.display="block"; err=True
    if err: return
    users.append({"username": u, "fullname": fn, "email": em, "password": pw})
    save_users(users)
    s.innerText="Account created! Please login now."; s.style.display="block"
    show_toast("Registration successful!")
    window.setTimeout(keep_proxy(lambda: (document.getElementById("register-modal").classList.remove("open"), document.getElementById("login-modal").classList.add("open"))), 1200)

def do_login(e):
    for el in document.querySelectorAll(".error"): el.style.display = "none"
    u = document.getElementById("login-username").value.strip()
    p = document.getElementById("login-password").value
    if not u: el=document.getElementById("login-user-error"); el.innerText="Username required"; el.style.display="block"; return
    if not p: el=document.getElementById("login-pass-error"); el.innerText="Password required"; el.style.display="block"; return
    found = next((x for x in get_users() if x["username"]==u and x["password"]==p), None)
    if found:
        set_current(u); update_nav()
        document.getElementById("login-modal").classList.remove("open")
        show_toast("Welcome, " + u + "!")
    else:
        g=document.getElementById("login-general-error"); g.innerText="Invalid username or password"; g.style.display="block"

def go_home(e): show_page("landing-page")
def go_shop(e): show_page("shop-page")
def go_about(e): show_page("about-page")
def open_login(e): document.getElementById("login-modal").classList.add("open")
def close_login(e): document.getElementById("login-modal").classList.remove("open")
def close_register(e): document.getElementById("register-modal").classList.remove("open")
def to_register(e): document.getElementById("login-modal").classList.remove("open"); document.getElementById("register-modal").classList.add("open")
def to_login(e): document.getElementById("register-modal").classList.remove("open"); document.getElementById("login-modal").classList.add("open")
def open_cart(e): render_cart(); document.getElementById("cart-modal").classList.add("open")
def close_cart(e): document.getElementById("cart-modal").classList.remove("open")
def close_product(e): document.getElementById("product-modal").classList.remove("open")
def do_logout(e): set_current(None); localStorage.removeItem("everywear_cart"); update_nav(); show_toast("Logged out")
def do_checkout(e): save_cart([]); update_cart_count(); render_cart(); show_toast("Order placed! Thank you for shopping at EveryWear")
def p_add_cart(e):
    if selected_product: handle_add_to_cart_from_data(selected_product["name"], float(selected_product["price"]), selected_product["img"], selected_product["id"])
def p_buy_now(e):
    if selected_product:
        ok = handle_add_to_cart_from_data(selected_product["name"], float(selected_product["price"]), selected_product["img"], selected_product["id"])
        if ok:
            document.getElementById("product-modal").classList.remove("open")
            render_cart(); document.getElementById("cart-modal").classList.add("open")

safe_bind("nav-home", "click", go_home)
safe_bind("nav-shop", "click", go_shop)
safe_bind("nav-about", "click", go_about)
safe_bind("shop-now", "click", go_shop)
safe_bind("open-login", "click", open_login)
safe_bind("close-login", "click", close_login)
safe_bind("close-register", "click", close_register)
safe_bind("to-register", "click", to_register)
safe_bind("to-login", "click", to_login)
safe_bind("open-cart", "click", open_cart)
safe_bind("close-cart", "click", close_cart)
safe_bind("close-product", "click", close_product)
safe_bind("logout-btn", "click", do_logout)
safe_bind("checkout-btn", "click", do_checkout)
safe_bind("login-btn", "click", do_login)
safe_bind("register-btn", "click", do_register)
safe_bind("p-add-cart", "click", p_add_cart)
safe_bind("p-buy-now", "click", p_buy_now)

for btn in document.querySelectorAll(".filter-bar button"):
    btn.addEventListener("click", keep_proxy(on_filter_click))

render_products()
update_nav()
show_page("landing-page")
console.log("EveryWear Loaded OK!")