/* abrir carrito */
document.getElementById("open-cart")?.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("cart-panel").classList.remove("hidden");
    document.getElementById("cart-overlay").classList.remove("hidden");
});

/* cerrar carrito */
document.getElementById("cart-overlay")?.addEventListener("click", () => {
    document.getElementById("cart-panel").classList.add("hidden");
    document.getElementById("cart-overlay").classList.add("hidden");
});

/* actualizar total en header */
function updateHeaderTotal(total) {
    const el = document.getElementById("cart-total");
    if (el) el.innerText = total + " ₽";
}

/* renovar contenido del carrito */
function refreshMiniCart(cart, total) {
    const box = document.querySelector(".cart-items");
    box.innerHTML = "";

    for (const [id, item] of Object.entries(cart)) {
        box.innerHTML += `
            <div class="cart-item">
                <img src="/static/img/platos/${item.imagen}" class="item-img">

                <div class="item-info">
                    <p class="item-name">${item.nombre}</p>
                    <p class="item-price">${item.precio} ₽</p>
                </div>

                <div class="item-qty">
                    <button class="qty-btn" onclick="changeQty('${id}', 'dec')">−</button>
                    <span>${item.cantidad}</span>
                    <button class="qty-btn" onclick="changeQty('${id}', 'inc')">+</button>
                </div>
            </div>
        `;
    }

    document.getElementById("sidebar-total").innerText = total + " ₽";
}

/* cambiar cantidad */
async function changeQty(platoId, action) {
    const res = await fetch(`/cart_update/${platoId}/${action}`);
    const data = await res.json();
    if (!data.success) return;

    updateHeaderTotal(data.total);
    refreshMiniCart(data.cart, data.total);
}

/* eliminar todo */
async function clearCart() {
    const res = await fetch("/clear_cart");
    const data = await res.json();

    updateHeaderTotal(0);
    refreshMiniCart({}, 0);
}

/* cargar carrito al iniciar */
document.addEventListener("DOMContentLoaded", async () => {
    // botones agregar
    document.querySelectorAll(".add-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;

            const res = await fetch(`/add_to_cart/${id}`);
            const data = await res.json();

            if (!data.success) return;

            updateHeaderTotal(data.total);
            refreshMiniCart(data.cart, data.total);
        });
    });

    // cargar estado inicial
    const res = await fetch("/cart_state");
    const data = await res.json();

    updateHeaderTotal(data.total);
    refreshMiniCart(data.cart, data.total);
});

