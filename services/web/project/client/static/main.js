// custom javascript

$(() => {
  console.log('Sanity Check!');
});

$('.delete-project').on('click', (event) => {
  const result = confirm('Are you sure?');
  if (!result) event.preventDefault();
});
