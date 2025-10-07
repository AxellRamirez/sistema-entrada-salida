document.getElementById('whatsappButton').addEventListener('click', function() {
  // Aquí iría la lógica para mostrar el API de WhatsApp
});

// Lógica para cambiar el color del círculo según el estado de asistencia
function changeAttendanceStatus(status) {
  const circle = document.getElementById('attendanceCircle');
  circle.classList.remove('registered', 'partial', 'absent');
  if (status === 'registered') {
      circle.classList.add('registered');
  } else if (status === 'partial') {
      circle.classList.add('partial');
  } else if (status === 'absent') {
      circle.classList.add('absent');
  }
}
