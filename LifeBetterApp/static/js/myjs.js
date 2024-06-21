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

document.addEventListener('DOMContentLoaded', function() {
    document.documentElement.style.setProperty(
        --background-image-url, 
        url(img/kawaiefdificiouwu.png)
    );
});

const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

// Cargar preferencia al iniciar
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    body.classList.add(savedTheme);
}

themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark');

    // Guardar preferencia
    const currentTheme = body.classList.contains('dark') ? 'dark' : 'light';
    localStorage.setItem('theme', currentTheme);
});


/***********************************************************************
/*--------------------------CALENDARIO----------------------------------------*/
document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth'
    });
    calendar.render();
});

document.addEventListener('DOMContentLoaded', function () {
  // Obtener todos los elementos con ID que comienza por "calendar-"
    var calendarElements = document.querySelectorAll('[id^="calendar-"]');

    calendarElements.forEach(function (calendarEl) {
        // Extraer el ID del espacio común del ID del elemento del calendario
        var espacioId = calendarEl.id.split('-')[1];

        // Realizar la solicitud AJAX para obtener las reservas del espacio
        $.ajax({
        url: '/obtener_reservas_espacio/' + espacioId + '/', // URL de tu vista Django
        dataType: 'json',
        success: function (reservas) {
            // Crear un array de eventos para FullCalendar
            var events = reservas.map(function (reserva) {
            return {
                title: 'Reservado',
                start: reserva.inicio_fecha_hora_reservacion,
                end: reserva.fin_fecha_hora_reservacion,
                // Puedes agregar más propiedades aquí si es necesario, como el ID de la reserva
            };
            });

            // Inicializar el calendario con los eventos obtenidos
            var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            events: events,
            selectable: true, // Habilitar la selección de fechas
            select: function (info) {
                // Llenar el formulario del modal con los datos de la selección
                $('#espacioId').val(espacioId);
                $('#inicio').val(info.startStr);
                $('#fin').val(info.endStr);
                $('#cantidad_personas').val(1); // Valor predeterminado

                // Abrir el modal
                $('#reservarModal').modal('show');
            },
            // ... (otras opciones de configuración del calendario)
            });

            calendar.render();
        },
        });
    });

    // Manejar el envío del formulario de reserva (AJAX)
    $('#reservacionForm').submit(function (event) {
        event.preventDefault(); // Evitar envío normal del formulario

        $.ajax({
            url: '{% url "crear_reservacion" %}', // URL de tu vista crear_reservacion
            type: 'POST',
            data: $(this).serialize(),
            success: function (response) {
                if (response.success) {
                    // Reserva creada con éxito
                    $('#reservarModal').modal('hide');
                    // Actualizar el calendario para mostrar la nueva reserva
                    calendar.refetchEvents(); // Vuelve a cargar los eventos del calendario
                } else {
                    // Error al crear la reserva
                    alert('Lo sentimos, hubo un problema al crear tu reserva. Por favor verifica los datos e inténtalo de nuevo.');
                }
            },
            error: function () {
                // Error en la solicitud AJAX, mostrar mensaje de error genérico
                alert('Ocurrió un error al procesar tu reserva. Por favor, inténtalo de nuevo más tarde.'); 
            }
        })
    });
});