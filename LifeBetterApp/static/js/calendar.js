/*document.addEventListener('DOMContentLoaded', function () {
  var calendarEl = document.getElementById('calendar');
  var defaultEspacioId = 1; // ID del espacio común predeterminado (puedes cambiarlo)
  var calendar;

  // Función para obtener y renderizar eventos del calendario
  function fetchAndRenderEvents(espacioId) {
    $.ajax({
      url: '/obtener_reservas_espacio/' + espacioId + '/',
      dataType: 'json',
      success: function (reservas) {
        var events = reservas.map(function (reserva) {
          return {
            id: reserva.id_reservacion,
            title: 'Reservado',
            start: reserva.inicio_fecha_hora_reservacion,
            end: reserva.fin_fecha_hora_reservacion,
          };
        });

        if (calendar) {
          calendar.setOption('events', events); // Actualizar los eventos
          calendar.render();
        } else {
          // Inicializar el calendario si aún no existe
          calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            events: events,
            selectable: true,
            select: function (info) {
              $('#espacioId').val(espacioId);
              $('#inicio').val(info.startStr);
              $('#fin').val(info.endStr);
              $('#cantidad_personas').val(1);
              $('#reservarModal').modal('show');
            },
            eventClick: function (info) {
              alert('Reserva: ' + info.event.title + ', ID: ' + info.event.id);
            },
          });
          calendar.render();
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {
        alert(
          'Error al obtener las reservas: ' + textStatus + ' - ' + errorThrown
        );
      },
    });
  }

  // Manejar el cambio del select de espacio
  $('#espacioSelect').change(function () {
    var espacioId = $(this).val();
    fetchAndRenderEvents(espacioId); 
  });

  // Cargar eventos al inicio (para el primer espacio por defecto)
  fetchAndRenderEvents(defaultEspacioId);

  // Manejar el envío del formulario de reserva (AJAX)
  $('#reservacionForm').submit(function (event) {
    event.preventDefault();

    var formData = $(this).serialize() + '&espacio_id=' + $('#espacioSelect').val();

    $.ajax({
      url: '{% url "crear_reservacion" %}',
      type: 'POST',
      data: formData,
      success: function (response) {
        if (response.success) {
          $('#reservarModal').modal('hide');
          fetchAndRenderEvents($('#espacioSelect').val()); 
        } else {
          // Mostrar errores de validación en el modal
          if (response.errors) {
            var errorMessages = '';
            for (var field in response.errors) {
              errorMessages += response.errors[field] + '<br>';
            }
            $('#reservacionForm .modal-body').prepend('<div class="alert alert-danger">' + errorMessages + '</div>');
          } else {
            alert('Error desconocido al crear la reserva.');
          }
        }
      },
      error: function () {
        alert(
          'Ocurrió un error al procesar tu reserva. Por favor, inténtalo de nuevo más tarde.'
        );
      },
    });
  });
});*/