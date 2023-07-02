
$(document).ready(function () {
  $("#selected_paramater").change(function () {

    debugger
    let parameter = $(this).val();

    // Set the hidden parameter by the selected golfer's email in first dropdown
    var hiddenElement = document.getElementById("user_email");
    hiddenElement.setAttribute("value", parameter);
    
    // Clear golf clubs in second dropdown
    $("#selected_paramater2").empty()

  })
}
)

$(document).ready(function () {
  $("#selected_paramater2").change(function () {

    debugger
    let parameter = $(this).val();

    // Set the hidden parameter by the selected golf club in second droppdown list
    var hiddenElement = document.getElementById("club");
    hiddenElement.setAttribute("value", parameter)

  })
}
)

$(document).ready(function () {
  $("#selected_paramater").change(function () {

    debugger
    let parameter = $(this).val();

    $.ajax({
      url: "/golfclubs",
      type: "POST",
      contentType: 'application/json',
      data: JSON.stringify({ 'user_email': parameter }),
      success: function (data) {
        console.log(data.golfClubs)
        // create dropdown option for each club in the selected golfer's golf set
        // second dropdown options are populated based on golfer's golf set
        let golfClubs = data.golfClubs;
        let dropdown = $("#selected_paramater2");
        dropdown.empty();
        $.each(golfClubs, function (i, golfClub) {
          dropdown.append($('<option></option>').attr('value', golfClub.label).text(golfClub.label));
        });

      }
    })
  })
})