document.querySelector('.pay-btn').addEventListener('click', () => {
    document.getElementById('ciudad_input').value = document.querySelector('.addr.ciudad').value;
    document.getElementById('calle_input').value = document.querySelector('.addr.calle').value;
    document.getElementById('altura_input').value = document.querySelector('.addr.altura').value;
    document.getElementById('piso_input').value = document.querySelector('.addr.piso').value;
    document.getElementById('departamento_input').value = document.querySelector('.addr.departamento').value;

    document.getElementById('order-form').submit();
});

document.querySelectorAll(".qty-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
        e.preventDefault();

        const itemEl = e.target.closest(".order-item");
        const platoId = itemEl.dataset.id;
        const action = e.target.dataset.action;

        const res = await fetch(`/cart_update/${platoId}/${action}`);
        const data = await res.json();

        if (!data.success) return;
        if (data.cart[platoId]) {
            itemEl.querySelector(".qty").innerText = data.cart[platoId].cantidad;

            const newPrice =
                data.cart[platoId].precio * data.cart[platoId].cantidad;

            itemEl.querySelector(".order-price").innerText = newPrice + " ₽";
        } else {
            itemEl.remove();
        }
        document.querySelector(".total-sum").innerText = data.total + " ₽";
        updateHeaderTotal(data.total);
        refreshMiniCart(data.cart, data.total);
    });
});