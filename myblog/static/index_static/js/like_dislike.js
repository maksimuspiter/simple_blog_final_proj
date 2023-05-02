function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function add_like_dislike(action, btn_pressed_id, btn_other_id, url, post_id) {
  let btn_class_active;
  let btn_press = document.getElementById(btn_pressed_id);
  let btn_other = document.getElementById(btn_other_id);
  let raiting = document.getElementById("raiting-post-" + post_id);
  const raiting_int = Number(raiting.innerHTML);

  switch (action) {
    case "like":
      btn_class_active = "btn btn-success";
      break;
    case "dislike":
      btn_class_active = "btn btn-danger";
      break;
    default:
      console.log("error: unknown action");
  }

  $.ajax({
    url: url,
    type: "POST",
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    success: (data) => {
      const result = data.result;
      console.log(data);

      btn_other.classList = "btn btn-secondary";

      if (result) {
        btn_press.classList = btn_class_active;

        switch (action) {
          case "like":
            raiting.innerHTML = raiting_int + 1;
            break;
          case "dislike":
            raiting.innerHTML = raiting_int - 1;
            break;
        }
      } else {
        btn_press.classList = "btn btn-secondary";
        switch (action) {
          case "like":
            raiting.innerHTML = raiting_int - 1;
            break;
          case "dislike":
            raiting.innerHTML = raiting_int + 1;
            break;
        }
      }
    },
    error: (error) => {
      console.log(error);
    },
  });
}
