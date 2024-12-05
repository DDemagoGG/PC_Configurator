function toggleOrderDetails(element) {
    const details = element.querySelector('.order-details');
    const allDetails = document.querySelectorAll('.order-details');
    
    allDetails.forEach(detail => {
        if (detail !== details) {
            detail.classList.remove('active');
        }
    });
    
    details.classList.toggle('active');
}