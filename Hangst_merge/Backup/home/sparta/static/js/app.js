/*
* 사용자에게 입력받은 input-username, input-password 라는 id 값을 가진 폼 데이터를 전달받은 후,
* 해당 데이터의 입력값이 빈 공란인지 확인
* */
function sign_in() {
    let username = $("#input-username").val()
    let password = $("#input-password").val()

    /* username 변수와 password 변수에 값이 없을 경우 아이디 및 비밀번호 확인 텍스트 출력  */
    if (username == "") {
        $("#help-id-login").text("아이디를 입력해주세요.")
        $("#input-username").focus()
        return;
    } else {
        $("#help-id-login").text("")
    }

    if (password == "") {
        $("#help-password-login").text("비밀번호를 입력해주세요.")
        $("#input-password").focus()
        return;
    } else {
        $("#help-password-login").text("")
    }
    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            username_give: username,
            password_give: password
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                window.location.replace("/")
            } else {
                alert(response['msg'])
            }
        }
    });
}
