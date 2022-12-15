const username_label = document.querySelector("#username_label");
const email_label = document.querySelector("#email_label");
const user_avatar = document.querySelector("#user_avatar");

const login_button = document.querySelector("#login_button");
const register_button = document.querySelector("#register_button");
const logout_button = document.querySelector("#logout_button");


// Get token & decode
function getCookie(cookieName) {
    let cookie = {};
    document.cookie.split(';').forEach(function(el) {
        let [key,value] = el.split('=');
        cookie[key.trim()] = value;
    })
    return cookie
}

function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

const token = getCookie('jwt')

if (token["jwt"] === undefined) {
    username_label.innerHTML = "Guest";
    email_label.innerHTML = "guest@zing.vn";
    user_avatar.src = "/static/images/3d-guest-avatar.webp"

    login_button.style.display = 'flex'
    register_button.style.display = 'flex'
    logout_button.style.display = 'none'
} else {
    const token_decode = parseJwt(token['jwt'])
    username_label.innerHTML = token_decode['sub'];
    email_label.innerHTML = token_decode['email'];
    token_decode['gender'] == 'male' 
        ? user_avatar.src = "/static/images/3d-boy-avatar.webp"
        : user_avatar.src = "/static/images/3d-girl-avatar.webp"

    login_button.style.display = 'none'
    register_button.style.display = 'none'
    logout_button.style.display = 'flex'
}