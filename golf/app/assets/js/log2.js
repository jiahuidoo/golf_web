$(document).ready(function () {
  // Function to handle the form submission
  $('form').submit(function (event) {
    event.preventDefault(); // Prevent default form submission

    // Perform Ajax request
    $.ajax({
      url: '/process2',
      method: 'POST',
      data: $(this).serialize(), // Serialize the form data
      error: function() {
        alert("Error");
      },
      success: function (response) {
        // Loop through the JSON response and build the HTML content
        var html = '';
        $.each(response.golf, function (index, value) {
          // Always bold the first line
          if (index === 0) {
            html += '<br><strong>' + value + '</strong>';
          }
          else {
            html += '<br>' + value;
          }
        });

        // Add one more line break after the last item
        html += '<br>';

        // Set the HTML content of the output space using innerHTML
        document.querySelector(".output_space > p").innerHTML += html
      }
    });
  });

  // Function to handle the reset button click
  $('button[type="reset"]').click(function () {
    // Clear the HTML content of the output space
    document.querySelector(".output_space > p").innerHTML = "<strong>Club Advice</strong>";
  });
});