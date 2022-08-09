def status_code(code, msg=""):

    if code == 0:
        return {"code": code, "message": "success"}
    elif code == 1:
        return {"code": code, "message": "error"}
    elif code == 2:
        return {"code": code, "message": "invalid parameter"}
    elif code == 3:
        return {"code": code, "message": "blocked"}
    elif code == 4:
        return {"code": code, "message": "none"}
    elif code == 5:
        return {
            "code": code,
            "message": msg,
        }
    else:
        return {
            "code": 900,
            "message": "Invalid error code",
        }
