const term = new Terminal({cursorBlink: false, rows: 20});

$(() => {
  console.log('Sanity Check!');
  term.open(document.getElementById('terminal'));
});

$('.delete-project').on('click', (event) => {
  const result = confirm('Are you sure?');
  if (!result) event.preventDefault();
});

$('body').on('click', '.grade-project', function() {
  term.clear();
  term.writeln('Running...');
  const projectID = $(this).data('id');
  $.ajax({
    url: `/projects/grade/${projectID}`,
    type: 'GET',
  })
  .done((res) => {
    getStatus(res.data.task_id, projectID);
  })
  .fail((err) => { console.log(err); });

});

function getStatus(taskID, projectID) {
  $.ajax({
    url: `/tasks/${projectID}/${taskID}`,
    method: 'GET'
  })
  .done((res) => {
    const taskStatus = res.data.task_status;
    if (taskStatus === 'finished') {
      if (res.data.task_result.status) {
        $(`.status-${projectID}`).html(
          '<i class="fas fa-times fa-lg build-pass"></i>'
        );
      } else {
        $(`.status-${projectID}`).html(
          '<i class="fas fa-check fa-lg build-fail"></i>'
        );
      }
      const termData = (res.data.task_result.data).replace(/\r?\n/g, "\r\n");
      term.clear();
      term.writeln(termData);
      term.scrollToBottom();
      return false;
    }
    if (taskStatus === 'failed') {
      $(`.status-${projectID}`).html(
        '<i class="fas fa-check fa-lg build-fail"></i>'
      );
      return false;
    }
    setTimeout(function() {
      getStatus(res.data.task_id, projectID);
    }, 1000);
  })
  .fail((err) => {
    console.log(err);
  });
}
