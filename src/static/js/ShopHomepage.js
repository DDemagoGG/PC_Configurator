async function changeStatus(button) {
    const orderItem = button.closest('.order-item');
    
    
    const order_id = orderItem.dataset.orderId;

    const response = await fetch(`http://localhost:8000/shop/home?order_id=${order_id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) {
        const errorResponse = await response.json();
        console.error('Server Error:', errorResponse);
        alert('Failed to change order status. Please try again.');
        return;
    }
    
    const statusSpan = orderItem.querySelector('.order-status');
    const currentStatus = statusSpan.textContent;
    
    let newStatus;
    
   
    switch(currentStatus) {
        case 'processing':
            newStatus = 'accepted';
            break;
        case 'accepted':
            newStatus = 'ready';
            break;
        case 'ready':
            newStatus = 'completed';
            button.disabled = true;
            break;
    }
    
    
    statusSpan.textContent = newStatus;
    statusSpan.className = `order-status status-${newStatus}`;

    if (newStatus === 'completed') {
        location.reload(true); 
    }
}

function toggleOrderDetails(element, event) {
    if (event.target.classList.contains('status-btn')) {
        event.stopPropagation();
        return;
    }
    
    const details = element.querySelector('.order-details');
    const allDetails = document.querySelectorAll('.order-details');
    
    allDetails.forEach(detail => {
        if (detail !== details) {
            detail.classList.remove('active');
        }
    });
    
    details.classList.toggle('active');
}

function updateCompletionTimes() {
    
    const orderItems = document.querySelectorAll('.order-list .order-item');

   
    orderItems.forEach(orderItem => {

        const statusSpan = orderItem.querySelector('.order-status');
        const completionTimeDiv = orderItem.querySelector('.completion-time');
        const nextStatusButton = orderItem.querySelector('.status-btn');

        if (statusSpan && completionTimeDiv && nextStatusButton) {

            const currentStatus = statusSpan.className.includes('status-completed');
            console.log(currentStatus)

            if (currentStatus) {
                completionTimeDiv.style.display = 'block';
            } else {
                completionTimeDiv.style.display = 'none';
            }
            nextStatusButton.disabled = currentStatus;
        }
    });
}

window.onload = updateCompletionTimes;