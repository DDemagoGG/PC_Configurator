async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');
    
    usernameError.style.display = 'none';
    passwordError.style.display = 'none';
    
    let isValid = true;
    
    if (username.length < 3) {
        usernameError.style.display = 'block';
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
        username,
        password
    };

    try {
        const response = await fetch('http://localhost:8000/user/login', {
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
        window.location.href = "http://localhost:8000/user/home";;
    } catch (error) {
        console.error('Network Error:', error);
        alert('An error occurred. Please check your internet connection and try again.');
    }
    
    
    return false;
}