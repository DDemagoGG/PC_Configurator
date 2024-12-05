async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const birthdate = document.getElementById('birthdate').value;

    const errors = {
        username: document.getElementById('usernameError'),
        email: document.getElementById('emailError'),
        password: document.getElementById('passwordError'),
        birthdate: document.getElementById('birthdateError')
    };

    Object.values(errors).forEach(error => error.style.display = 'none');

    let isValid = true;

    if (username.length < 3) {
        errors.username.style.display = 'block';
        isValid = false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        errors.email.style.display = 'block';
        isValid = false;
    }

    if (password.length < 6) {
        errors.password.style.display = 'block';
        isValid = false;
    }

    const today = new Date();
    const birthdateObj = new Date(birthdate);
    if (!birthdate || birthdateObj > today) {
        errors.birthdate.style.display = 'block';
        isValid = false;    
    }

    if (!isValid) {
        const registerContainer = { shake: true };
        console.log('Validation failed:', registerContainer);
        setTimeout(() => {
            registerContainer.shake = false;
            console.log('Shake animation removed:', registerContainer);
        }, 500);
        return false;
    }

    const data = {
        username,
        email,
        password,
        birthdate
    };

    try {
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.status == 409){
            alert('username is not unique')
            return;
        } else if (!response.ok) {
            const errorResponse = await response.json();
            console.error('Server Error:', errorResponse);
            alert('Failed to register. Please try again.');
            return;
        }

        console.log('Registration successful:');
        window.location.href = "http://localhost:8000/user/login";
    } catch (error) {
        console.error('Network Error:', error);
        alert('An error occurred. Please check your internet connection and try again.');
    }

    return false;
}
