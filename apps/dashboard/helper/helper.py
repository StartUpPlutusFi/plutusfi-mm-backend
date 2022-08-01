def status_code(code):

    match code:
        case 0:
            return {
                'code': code,
                'message': "success"
            }
        case 1:
            return {
                'code': code,
                'message': "error"
            }
        case 2:
            return {
                'code': code,
                'message': "invalid"
            }
        case 3:
            return {
                'code': code,
                'message': "blocked"
            }
        case 4:
            return {
                'code': code,
                'message': "none"
            }