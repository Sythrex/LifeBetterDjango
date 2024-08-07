const formulario = document.getElementById("Form_Contacto");

const userName = document.getElementById("userName");
const userEmail = document.getElementById("userEmail");
const userMens = document.getElementById("userMens");

const alertSuccess = document.getElementById("alertSuccess");

const regUserName = /^[A-Za-zÑñÁáÉéÍíÓóÚúÜü\s]+$/;
const regUserEmail = /^[a-z0-9]+(\.[_a-z0-9]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,15})$/;

const pintarMensajeExito = () => {
    alertSuccess.classList.remove("d-none");
    alertSuccess.textContent = "Mensaje enviado con éxito";
};

const pintarMensajeError = (errores) => {
    errores.forEach((item) => {
        item.tipo.classList.remove("d-none");
        item.tipo.textContent = item.msg;
    });
};


document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById("Form_Contacto");
    if (formulario) {
        formulario.addEventListener("submit", (e) => {
            e.preventDefault();
            alert("Validando Formulario");

            alertSuccess.classList.add("d-none");
            const errores = [];

            // validar nombre
            if (!regUserName.test(userName.value) || !userName.value.trim()) {
                userName.classList.add("is-invalid");

                errores.push({
                    tipo: alertName,
                    msg: "Formato no válido campo nombre, solo letras",
                });
            } else {
                userName.classList.remove("is-invalid");
                userName.classList.add("is-valid");
                alertName.classList.add("d-none");
            }

            // validar email
            if (!regUserEmail.test(userEmail.value) || !userEmail.value.trim()) {
                userEmail.classList.add("is-invalid");

                errores.push({
                    tipo: alertEmail,
                    msg: "Escriba un correo válido",
                });
            } else {
                userEmail.classList.remove("is-invalid");
                userEmail.classList.add("is-valid");
                alertEmail.classList.add("d-none");
            }

            if (errores.length !== 0) {
                pintarMensajeError(errores);
                return;
            }

            console.log("Formulario enviado con éxito");
            pintarMensajeExito();
        });
    }
});


var csrftoken = '{{ csrf_token }}';  // Obtén el token CSRF de Django

function csrfSafeMethod(method) {
    // estos métodos HTTP no requieren CSRF
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
    }
});