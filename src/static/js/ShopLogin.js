async function handleLogin(event) {
    event.preventDefault();
    
    const shopname = document.getElementById('shopname').value;
    const password = document.getElementById('password').value;
    const shopnameError = document.getElementById('shopnameError');
    const passwordError = document.getElementById('passwordError');
    
    shopnameError.style.display = 'none';
    passwordError.style.display = 'none';
    
    let isValid = true;
    
    if (shopname.length < 3) {
        shopnameError.style.display = 'block';
        isValid = false;
    }
    
    if (password.length < 6) {
        passwordError.style.display = 'block';
        isValid = false;
    }
    
    if (!isValid) {
        loginContainer.classList.add('shake');
        setTimeout(() => {
            loginContainer.classList.remove('shake');
        }, 500);
        return false;
    }

    const data = {
        shopname,
        password
    };

    try {
        const response = await fetch('http://localhost:8000/shop/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.status == 404){
            alert('Incorrect login or password')
            return;
        } else if (!response.ok) {
            const errorResponse = await response.json();
            console.error('Server Error:', errorResponse);
            alert('Failed to register. Please try again.');
            return;
        }

        console.log('Authentification successful:');
        window.location.href = "http://localhost:8000/shop/home";;
    } catch (error) {
        console.error('Network Error:', error);
        alert('An error occurred. Please check your internet connection and try again.');
    }
    
    
    return false;
}