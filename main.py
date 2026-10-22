# EveryWear - main.py - CART SAVED AFTER LOGOUT + EYE TOGGLE
import asyncio
from js import document, localStorage
from pyodide.ffi import create_proxy
import json

products = [
    {"id": "1", "name": "CR7 Dedication Tshirt", "price": 299, "img": "assets/shirt1.jpeg", "cat": "unisex", "desc": "Oversized fit with iconic snail graphic. Premium 100% cotton. Soft, breathable and perfect for everyday wear."},
    {"id": "2", "name": "IBIZA 20/06 MEMORY TSHIRT", "price": 199, "img": "assets/shirt2.jpeg", "cat": "men", "desc": "Vintage-inspired Ibiza graphic. Heavyweight cotton for a structured streetwear look."},
    {"id": "3", "name": "Keep God First Tshirt", "price": 359, "img": "assets/shirt3.jpeg", "cat": "streetwear", "desc": "Bold faith statement in puff print. Unisex brown tee, durable and comfortable."},
    {"id": "4", "name": "WAKE UP SNAIL TSHIRT", "price": 399, "img": "assets/shirt4.jpeg", "cat": "men", "desc": "CR7 inspired dedication design. For the fans who never stop. Limited drop."},
    {"id": "5", "name": "Sunset State Tshirt", "price": 299, "img": "assets/shirt5.png", "cat": "women", "desc": "Sunset graphic with desert vibes. Lightweight and perfect for summer."},
    {"id": "6", "name": "Warm Days", "price": 249, "img": "assets/shirt6.png", "cat": "unisex", "desc": "Minimal EveryWear logo tee. Your everyday essential."},
    {"id": "7", "name": "Slow Motion", "price": 329, "img": "assets/shirt7.png", "cat": "streetwear", "desc": "Washed brown streetwear tee. Vintage feel, modern fit."},
    {"id": "8", "name": "Bloom In Heat", "price": 279, "img": "assets/shirt8.png", "cat": "women", "desc": "Clean white graphic tee. Minimal design for maximum style."},
    {"id": "9", "name": "Golden Hour", "price": 279, "img": "assets/shirt9.png", "cat": "women", "desc": "Golden hour glow design. Soft premium cotton."},
    {"id": "10", "name": "Keep The Flow", "price": 279, "img": "assets/shirt10.png", "cat": "men", "desc": "Keep The Flow street design. Relaxed fit."},
]

selected_product = None
selected_size = None
PROXIES = []
def keep(fn):
    p = create_proxy(fn)
    PROXIES.append(p)
    return p

def get_users():
    data = localStorage.getItem("everywear_users")
    return json.loads(data) if data else []
def save_users(u): localStorage.setItem("everywear_users", json.dumps(u))
def get_current(): return localStorage.getItem("everywear_current")
def set_current(n):
    if n: localStorage.setItem("everywear_current", n)
    else: localStorage.removeItem("everywear_current")
def get_cart():
    # A cart belongs only to the currently logged-in user.
    user = get_current()
    if not user:
        return []

    data = localStorage.getItem(f"everywear_cart_{user}")
    return json.loads(data) if data else []

def save_cart(c):
    # Keep the active user's cart in their own storage key.
    user = get_current()
    cart_data = json.dumps(c)
    localStorage.setItem("everywear_cart", cart_data)
    if user:
        localStorage.setItem(f"everywear_cart_{user}", cart_data)

def show_toast(msg):
    t = document.getElementById("toast")
    t.innerText = msg
    t.style.display = "block"
    async def hide_later():
        await asyncio.sleep(2)
        t.style.display = "none"
    asyncio.create_task(hide_later())

def update_cart_count():
    s = sum(i["qty"] for i in get_cart())
    document.getElementById("cart-count").innerText = str(s)

def update_nav():
    user = get_current()
    lb = document.getElementById("open-login")
    lob = document.getElementById("logout-btn")
    disp = document.getElementById("user-display")
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
    document.getElementById(page).style.display = "block"
    document.documentElement.scrollTop = 0
    document.body.scrollTop = 0

def handle_add_to_cart_from_data(name, price, img, pid, size="M"):
    if not get_current():
        show_toast("Please login to add items to your cart")
        document.getElementById("login-modal").classList.add("open")
        return False
    if not size:
        err = document.getElementById("size-error")
        err.innerText = "Please select a size"
        err.style.display = "block"
        show_toast("Please select a size")
        return False
    cart = get_cart()
    found = next((i for i in cart if i["name"] == name and i.get("size") == size), None)
    if found: found["qty"] += 1
    else: cart.append({"id": pid, "name": name, "price": price, "img": img, "qty": 1, "size": size})
    save_cart(cart)
    update_cart_count()
    show_toast(f"{name} ({size}) added to cart!")
    return True

def render_cart():
    cart = get_cart()
    con = document.getElementById("cart-items")
    con.innerHTML = ""
    total = 0
    if len(cart) == 0:
        con.innerHTML = "<p style=\'text-align:center;color:#888;padding:20px\'>Your cart is empty</p>"
    else:
        for item in cart:
            total += item["price"] * item["qty"]
            size = item.get("size", "M")
            div = document.createElement("div")
            div.className = "cart-item"
            div.innerHTML = f"<img src='{item['img']}'><div><b>{item['name']}</b><br>Size: {size} — ₱{item['price']} x {item['qty']}</div>"
            con.appendChild(div)
    document.getElementById("cart-total").innerText = f"Total: ₱{total:.2f}"

def open_product(event):
    global selected_product, selected_size
    selected_size = None
    for b in document.querySelectorAll(".size-btn"): b.className = "size-btn"
    se = document.getElementById("size-error")
    if se: se.style.display = "none"
    pid = event.currentTarget.getAttribute("data-id")
    for p in products:
        if p["id"] == pid:
            selected_product = p
            break
    if selected_product:
        document.getElementById("p-img").src = selected_product["img"]
        document.getElementById("p-cat").innerText = selected_product["cat"].upper()
        document.getElementById("p-name").innerText = selected_product["name"].upper()
        document.getElementById("p-price").innerText = f"₱{selected_product['price']}"
        document.getElementById("p-desc").innerText = selected_product["desc"]
        document.getElementById("product-modal").classList.add("open")

def on_add_click(e):
    e.stopPropagation()
    global selected_product, selected_size
    selected_size = None
    # clear old size selection
    for b in document.querySelectorAll(".size-btn"): 
        b.className = "size-btn"
    se = document.getElementById("size-error")
    if se: se.style.display = "none"
    
    # get product id from the Add to Cart button
    btn = e.currentTarget
    pid = btn.getAttribute("data-id")
    for p in products:
        if p["id"] == pid:
            selected_product = p
            break
    if selected_product:
        document.getElementById("p-img").src = selected_product["img"]
        document.getElementById("p-cat").innerText = selected_product["cat"].upper()
        document.getElementById("p-name").innerText = selected_product["name"].upper()
        document.getElementById("p-price").innerText = f"₱{selected_product['price']}"
        document.getElementById("p-desc").innerText = selected_product["desc"]
        document.getElementById("product-modal").classList.add("open")

def on_size_click(e):
    global selected_size
    b = e.currentTarget
    for x in document.querySelectorAll(".size-btn"): x.className = "size-btn"
    b.className = "size-btn active"
    selected_size = b.getAttribute("data-size")
    document.getElementById("size-error").style.display = "none"

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
            <img src="{p['img']}" alt="{p['name']}">
            <div class="card-body">
                <p style="font-size:11px;letter-spacing:1px;color:#888">{p['cat'].upper()}</p>
                <h3>{p['name']}</h3>
                <p class="price">₱{p['price']}</p>
                <button class="add-btn" data-id="{p['id']}" data-name="{p['name']}" data-price="{p['price']}" data-img="{p['img']}">Add to Cart</button>
            </div>
        """
        card.addEventListener("click", keep(open_product))
        card.querySelector("img").addEventListener("error", keep(on_image_error))
        grid.appendChild(card)
    for btn in document.querySelectorAll(".add-btn"):
        btn.addEventListener("click", keep(on_add_click))

def on_image_error(event):
    image = event.currentTarget
    if image.getAttribute("data-fallback"):
        return
    image.setAttribute("data-fallback", "true")
    image.src = "https://via.placeholder.com/500?text=EveryWear"

def validate_email(e): return "@" in e and "." in e and len(e) > 5
def validate_password(pw): return len(pw) >= 8 and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw)

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
    def go(): 
        document.getElementById("register-modal").classList.remove("open")
        document.getElementById("login-modal").classList.add("open")
    async def go_later():
        await asyncio.sleep(1.2)
        go()
    asyncio.create_task(go_later())

def do_login(e):
    for el in document.querySelectorAll(".error"): el.style.display = "none"
    u = document.getElementById("login-username").value.strip()
    p = document.getElementById("login-password").value
    if not u: el=document.getElementById("login-user-error"); el.innerText="Username required"; el.style.display="block"; return
    if not p: el=document.getElementById("login-pass-error"); el.innerText="Password required"; el.style.display="block"; return
    found = next((x for x in get_users() if x["username"]==u and x["password"]==p), None)
    if found:
        set_current(u)
        # Load only this user's cart; never reuse another session's cart.
        saved = localStorage.getItem(f"everywear_cart_{u}")
        localStorage.setItem("everywear_cart", saved if saved else "[]")
        update_nav()
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
def close_checkout(e): document.getElementById("checkout-modal").classList.remove("open")
def do_logout(e):
    # Clear the active user's unpurchased cart when they log out.
    user = get_current()
    if user:
        localStorage.removeItem(f"everywear_cart_{user}")

    # Clear the session cart as well, so it cannot appear while logged out
    # or leak into another account's session.
    localStorage.setItem("everywear_cart", "[]")
    set_current(None)

    # Close shopping dialogs and refresh the cart badge to show zero items.
    for modal_id in ("cart-modal", "checkout-modal", "product-modal"):
        document.getElementById(modal_id).classList.remove("open")

    update_nav()
    render_cart()
    show_toast("Logged out - your cart has been cleared.")
def on_checkout(e):
    cart = get_cart()
    if len(cart)==0:
        show_toast("Cart is empty")
        return
    document.getElementById("cart-modal").classList.remove("open")
    document.getElementById("checkout-modal").classList.add("open")
def confirm_order(e):
    addr = document.getElementById("checkout-address").value.strip()
    contact = document.getElementById("checkout-contact").value.strip()
    for el in [document.getElementById("checkout-address-error"), document.getElementById("checkout-contact-error")]:
        el.style.display = "none"
    has_err = False
    if not addr:
        el=document.getElementById("checkout-address-error"); el.innerText="Delivery address is required"; el.style.display="block"; has_err=True
    if not contact:
        el=document.getElementById("checkout-contact-error"); el.innerText="Contact number is required"; el.style.display="block"; has_err=True
    elif len(contact) < 11 or not contact.replace(" ","").replace("-","").isdigit():
        el=document.getElementById("checkout-contact-error"); el.innerText="Enter a valid contact number"; el.style.display="block"; has_err=True
    if has_err: return
    save_cart([])
    user = get_current()
    if user:
        localStorage.setItem(f"everywear_cart_{user}", json.dumps([]))
    update_cart_count()
    render_cart()
    document.getElementById("checkout-modal").classList.remove("open")
    show_toast(f"Order confirmed! Deliver to {addr}")
    document.getElementById("checkout-address").value = ""
    document.getElementById("checkout-contact").value = ""

def p_add_cart(e):
    if selected_product: 
        if handle_add_to_cart_from_data(selected_product["name"], float(selected_product["price"]), selected_product["img"], selected_product["id"], selected_size):
            document.getElementById("product-modal").classList.remove("open")

def p_buy_now(e):
    if selected_product:
        ok = handle_add_to_cart_from_data(selected_product["name"], float(selected_product["price"]), selected_product["img"], selected_product["id"], selected_size)
        if ok:
            document.getElementById("product-modal").classList.remove("open")
            render_cart(); document.getElementById("cart-modal").classList.add("open")

# EYE TOGGLE
def toggle_login_pass(e):
    inp = document.getElementById("login-password")
    btn = document.getElementById("toggle-login-pass")
    if inp.type == "password":
        inp.type = "text"
        btn.innerText = "🙈"
    else:
        inp.type = "password"
        btn.innerText = "👁️"

def toggle_reg_pass(e):
    inp = document.getElementById("reg-password")
    btn = document.getElementById("toggle-reg-pass")
    if inp.type == "password":
        inp.type = "text"
        btn.innerText = "🙈"
    else:
        inp.type = "password"
        btn.innerText = "👁️"

def toggle_reg_confirm(e):
    inp = document.getElementById("reg-confirm")
    btn = document.getElementById("toggle-reg-confirm")
    if inp.type == "password":
        inp.type = "text"
        btn.innerText = "🙈"
    else:
        inp.type = "password"
        btn.innerText = "👁️"

# BIND ALL
for id, fn in [("nav-home", go_home), ("nav-shop", go_shop), ("nav-about", go_about), ("shop-now", go_shop), ("open-login", open_login), ("close-login", close_login), ("close-register", close_register), ("to-register", to_register), ("to-login", to_login), ("open-cart", open_cart), ("close-cart", close_cart), ("close-product", close_product), ("close-checkout", close_checkout), ("logout-btn", do_logout), ("checkout-btn", on_checkout), ("confirm-order-btn", confirm_order), ("login-btn", do_login), ("register-btn", do_register), ("p-add-cart", p_add_cart), ("p-buy-now", p_buy_now), ("toggle-login-pass", toggle_login_pass), ("toggle-reg-pass", toggle_reg_pass), ("toggle-reg-confirm", toggle_reg_confirm)]:
    el = document.getElementById(id)
    if el: el.addEventListener("click", keep(fn))

for btn in document.querySelectorAll(".filter-bar button"):
    btn.addEventListener("click", keep(on_filter_click))

for btn in document.querySelectorAll(".size-btn"):
    btn.addEventListener("click", keep(on_size_click))

render_products()
update_nav()
show_page("landing-page")
# restore cart for already logged in user
user = get_current()
if user:
    saved = localStorage.getItem(f"everywear_cart_{user}")
    if saved:
        localStorage.setItem("everywear_cart", saved)
        update_cart_count()