const input = document.querySelector(".input__field__password");
const inputIcon = document.querySelector(".input__icon__password");

inputIcon.addEventListener("click", (e) => {
    e.preventDefault();

    inputIcon.setAttribute(
        'src', 
        input.getAttribute('type') === 'password' ?
        '/static/imgs/icons/eye.svg'
          :
        '/static/imgs/icons/eye-off.svg'
    );

    input.setAttribute(
        'type', 
        input.getAttribute('type') === 'password' ? 
        'text'
          :
        'password'
    );
});

