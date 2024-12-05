let costs = JSON.parse(sessionStorage.getItem("costs"));
let names = JSON.parse(sessionStorage.getItem("names"));
let order = JSON.parse(sessionStorage.getItem("order"));

function toggleCreateButton() {
    const select = document.querySelector('.shop-select');
    const createBtn = document.querySelector('.create-btn');
    
    if (select.value) {
        createBtn.classList.add('active');
        createBtn.disabled = false;
    } else {
        createBtn.classList.remove('active');
        createBtn.disabled = true;
    }
}

async function createOrder() {
    const selectElement = document.querySelector('.shop-select');
    const shop_id = selectElement.value;
    data = {
        order,
        shop_id
    }
    const response = await fetch('http://localhost:8000/user/order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const errorResponse = await response.json();
        console.error('Server Error:', errorResponse);
        alert('Failed to create order. Please try again.');
        return;
    }

    window.location.href = 'http://localhost:8000/user/account';
}

function updateOrderSummary() {
    const orderSummary = document.querySelector('.order-summary .component-list');
    
    let total = 0;
    Object.keys(order).forEach(item => {
        const listItem = document.createElement('li');
        listItem.classList.add('component-item');
        
        const nameSpan = document.createElement('span');
        if (item == 'processor'){
            nameSpan.textContent = `CPU: ${names[item]}`;
        } else if (item == 'computer_case'){
            nameSpan.textContent = `case: ${names[item]}`;
        } else if (item == 'videocard'){
            nameSpan.textContent = `GPU: ${names[item]}`;
        } else if (item == 'power_block'){
            nameSpan.textContent = `power supply: ${names[item]}`;
        } else if (item == 'cooler'){
            nameSpan.textContent = `cooling: ${names[item]}`;
        } else{
            nameSpan.textContent = `${item}: ${names[item]}`;
        }
        
        const priceSpan = document.createElement('span');
        priceSpan.textContent = `$${costs[item]}`;
        
        listItem.appendChild(nameSpan);
        listItem.appendChild(priceSpan);
        
        orderSummary.appendChild(listItem);
        
        total += costs[item];
    });

    const totalItem = document.createElement('li');
    totalItem.classList.add('component-item');
    
    const totalNameSpan = document.createElement('span');
    totalNameSpan.textContent = 'Total';
    
    const totalPriceSpan = document.createElement('span');
    totalPriceSpan.textContent = `$${total}`;
    
    totalItem.appendChild(totalNameSpan);
    totalItem.appendChild(totalPriceSpan);
    
    orderSummary.appendChild(totalItem);
}

updateOrderSummary();
