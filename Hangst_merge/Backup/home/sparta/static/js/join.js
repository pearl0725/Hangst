
<!-- 회원가입 -->
function sign_up() {
    <!-- 사용자가 입력한 를 변수에 담는다. -->
    let userid = $("#input-id").val()
    let password = $("#input-pwd").val()
    let password2 = $("#input-pwd-check").val()
    let username = $("#inputName").val()

    if ($("#help-id").hasClass("is-danger")) {
        alert("아이디를 다시 확인해주세요.")
        return;
    } else if (!$("#help-id").hasClass("is-success")) {
        alert("아이디 중복확인을 해주세요.")
        return;
    }

    // 비밀번호가 공백일 경우 -> 해당 텍스트로 변경하여 사용자에게 알려준다.
    if (password == "") {
        $("#help-password").text("비밀번호를 입력해주세요.").addClass("is-danger").css("color", "crimson")
        $("#input-pwd").focus()
        return;

    // 비밀번호가 형식에 맞지 않을 경우 -> 해당 텍스트로 변경하여 사용자에게 알려준다.
    } else if (!is_password(password)) {
        $("#help-password").text("8~16자, 대소문자와 숫자(각 1개 이상 포함), 특수문자(!@#$%^&*)만 사용 가능합니다.").addClass("is-danger").css("color", "crimson")
        $("#input-pwd").focus()
        return

    // 위 조건식을 모두 패스하면 해당 텍스트로 변경 후 'is-success' 클래스를 추가 -> 조건에 부합하게된다.
    } else {
        $("#help-password").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger").addClass("is-success").css("color", "dodgerblue")
    }

    // 두 번째 비밀번호에 대한 조건식 검사 (위와 동일)
    if (password2 == "") {
        $("#help-password2").text("비밀번호를 입력해주세요.").addClass("is-danger").css("color", "crimson")
        $("#input-pwd-check").focus()
        return;
    } else if (password2 != password) {
        $("#help-password2").text("비밀번호가 일치하지 않습니다.").addClass("is-danger").css("color", "crimson")
        $("#input-pwd-check").focus()
        return;
    } else {
        $("#help-password2").text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-success").css("color", "dodgerblue")
    }

    // 이름이 공백일 경우 (이름은 정해진 형식은 없다.)
    if (username == "") {
        $("#help-name").text("이름을 입력해주세요.").addClass("is-danger").css("color", "crimson")
        $("#inputName").focus()
        return;
    }
    // 모든 조건 통과 시 해당 url로 데이터를 보내준다. (아이디, 비밀번호, 이름)
    $.ajax({
        type: "POST",
        url: "/sign_up/save",
        data: {
            userid_give: userid,
            password_give: password,
            username_give: username
        },
        success: function (response) {
            alert("항스트99의 멤버가 되었습니다!")
            window.location.reload()
        }
    });
}

// 정규식 사용하여 아이디 형식 검사
function is_id(asValue) {
    var regExp = /^(?=.*[a-z])[-a-z0-9_]{4,10}$/;
    return regExp.test(asValue);
}

// 정규식 사용하여 비밀번호 형식 검사
function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z0-9!@#$%^&*])[0-9a-zA-Z!@#$%^&*]{8,16}$/;
    return regExp.test(asValue);
}

// 아이디 검사
function check_dup() {
    let userid = $("#input-id").val()

    // 아이디가 공백일 경우 -> 해당 텍스트로 변경하여 사용자에게 알려준다.
    if (userid == "") {
        $("#help-id").text("아이디를 입력해주세요.").addClass("is-danger").css("color", "crimson")
        $("#input-id").focus()
        return;
    }

    // 아이디의 형식이 맞지 않을 경우 -> 해당 텍스트로 변경하여 사용자에게 알려준다.
    if (!is_id(userid)) {
        $("#help-id").text("아이디의 형식을 확인해주세요. (4-10자의 영문 소문자, 숫자와 특수기호(_)만 사용 가능)").addClass("is-danger").css("color", "crimson")
        $("#input-id").focus()
        return;
    }

    // 모든 조건 통과 시 해당 url로 데이터(아이디)를 보냄 -> 아이디 중복체크
    $.ajax({
        type: "POST",
        url: "/sign_up/check_dup",
        data: {
            userid_give: userid
        },
        success: function (response) {
            if (response["exists"]) {
                $("#help-id").text("이미 사용중 아이디입니다.").addClass("is-danger").css("color", "crimson")
                $("#input-id").focus()
            } else {
                $("#help-id").text("멋진 아이디네요!").removeClass("is-danger").addClass("is-success").css("color", "dodgerblue")
            }
            $("#help-id").removeClass("is-loading")

        }
    });
}
