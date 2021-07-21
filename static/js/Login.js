// 获取元素和点击操作
const signInBtn = document.getElementById("signIn");
const signUpBtn = document.getElementById("signUp");
// const fistForm = document.getElementById("form1");
// const secondForm = document.getElementById("form2");
const container = document.querySelector(".container");

signInBtn.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});

signUpBtn.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

// fistForm.addEventListener("submit", (e) => e.preventDefault());
// secondForm.addEventListener("submit", (e) => e.preventDefault());

function enroll_validate() {

    var name = document.getElementById("enroll_name").value;
    var password = document.getElementById("enroll_password").value;
    var password_sure = document.getElementById("enroll_password_sure").value;
    var url = location.href

    if (name.length == 0) {
        alert("输入姓名不能为空！！");
    } else if (password.length == 0) {
        alert("密码不能为空！！");
    } else if (password != password_sure) {
        alert("两次密码输入不同，请重试 ！！")
        password.value = ""
        password_sure.value = ""
    } else {
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify({
                type: 'enroll',
                name: name,
                password: password,
            }),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response, status) {
                // response {status,error_text}
                JSON.parse(response);
                if (response.status == true) {
                    alert("注册成功，请登录 ！！");
                    location.reload();
                } else {
                    alert(response.error_text);
                }
            },
            error: function(request, textStatus, errorThrown) {
                alert("传送错误，错误信息为: " + errorThrown + " 请重试！！")
            }
        });
    }

}

function login_validate() {
    var name = document.getElementById("login_name").value;
    var password = document.getElementById("login_password").value;
    var url = location.href

    if (name.length == 0) {
        alert("输入姓名不能为空！！");
    } else if (password.length == 0) {
        alert("密码不能为空！！");
    } else {
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify({
                type: 'login',
                name: name,
                password: password,
            }),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response, status) {
                // response {status,error_text/url}
                JSON.parse(response);
                if (response.status == true) {
                    location.href = response.url;
                } else {
                    alert(response.error_text);
                }
            },
            error: function(request, textStatus, errorThrown) {
                alert("传送错误，错误信息为: " + errorThrown + " 请重试！！")
            }
        });
    }

}