const cartItems = [
    { name: 'Item 1', price: 10, quantity: 1 },
    { name: 'Item 2', price: 20, quantity: 2 },
];

const cartTable = document.getElementById('cart-table');
const cartItemsContainer = document.getElementById('cart-items');
const totalBillElement = document.getElementById('total-bill');

function updateCart() {
    cartItemsContainer.innerHTML = '';
    let totalBill = 0;

    cartItems.forEach(item => {
        const totalItemPrice = item.price * item.quantity;
        totalBill += totalItemPrice;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.name}</td>
            <td>$${item.price}</td>
            <td>
                <input type="number" value="${item.quantity}" min="1" onchange="updateQuantity(${cartItems.indexOf(item)}, this.value)">
            </td>
            <td>$${totalItemPrice}</td>
            <td>
                <button onclick="removeItem(${cartItems.indexOf(item)})">Remove</button>
            </td>
        `;
        cartItemsContainer.appendChild(tr);
    });

    totalBillElement.textContent = `Total Bill: $${totalBill}`;
}

function updateQuantity(index, newQuantity) {
    cartItems[index].quantity = parseInt(newQuantity);
    updateCart();
}

function removeItem(index) {
    cartItems.splice(index, 1);
    updateCart();
}

updateCart();
