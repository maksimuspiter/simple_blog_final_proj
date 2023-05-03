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

function get_btn_pressed_id(action, content_type, id) {
  const btn_pressed_id = "btn" + "-" + action + "-" + content_type + "-" + id;
  let btn_press = document.getElementById(btn_pressed_id);
  return btn_press;
}

function get_btn_other_id(action, content_type, id) {
  let other_action;

  switch (action) {
    case "like":
      other_action = "dislike";
      break;
    case "dislike":
      other_action = "like";
      break;
  }
  const btn_other_id =
    "btn" + "-" + other_action + "-" + content_type + "-" + id;
  let btn_other = document.getElementById(btn_other_id);
  return btn_other;
}

function change_collor(action, content_type, id, change_collor = false) {
  let btn_press = get_btn_pressed_id(action, content_type, id);
  let btn_other = get_btn_other_id(action, content_type, id);

  btn_other.classList = "btn btn-secondary";

  switch (action) {
    case "like":
      if (change_collor) {
        btn_press.classList = "btn btn-success";
      } else {
        btn_press.classList = "btn btn-secondary";
      }
      break;

    case "dislike":
      if (change_collor) {
        btn_press.classList = "btn btn-danger";
      } else {
        btn_press.classList = "btn btn-secondary";
      }

      break;
    default:
      throw new Error("Invalide Parameter,  unknown action");
  }
}
function change_raiting(content_type, id, add) {
  let raiting = document.getElementById("raiting-" + content_type + "-" + id);
  const raiting_int = Number(raiting.innerHTML);
  raiting.innerHTML = raiting_int + add;
}

function add_like_dislike(action, content_type, id) {
  const url =
    "/" + "like_dislike/" + content_type + "/" + id + "/" + action + "/";
  $.ajax({
    url: url,
    type: "POST",
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    success: (data) => {
      let result = data.result;
      let add = data.change_raiting;

      change_collor(action, content_type, id, result);
      change_raiting(content_type, id, add);
    },

    error: (error) => {
      console.log(error);
    },
  });
}
