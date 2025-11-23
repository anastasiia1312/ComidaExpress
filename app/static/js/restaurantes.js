/* agregar en carrito*/
document.querySelectorAll(".add-btn").forEach(btn => {
    btn.addEventListener("click", async () => {

        const platoId = btn.dataset.id;

        const res = await fetch(`/add_to_cart/${platoId}`);
        
        if (res.status === 401) {
            alert("Para agregar productos debes iniciar sesión.");
            return;
        }

        const data = await res.json();

        if (!data.success) return;

        updateHeaderTotal(data.total);
        refreshMiniCart(data.cart, data.total);
    });
});

