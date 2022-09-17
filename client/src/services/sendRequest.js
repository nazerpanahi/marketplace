export async function sendJSONRequest(url,
                                      options=null,
                                      fetchJson=true,
                                      checkResponseStatus=true) {
    if (!options) {
        options = {}
    }
    let method = options.method || 'GET'
    let headers = options.headers || {}
    let body = options.body
    let credentials = options.credentials || 'include'

    headers['Content-Type'] = 'application/json'

    let extra = {
        'method': method,
        'headers': headers,
        'credentials': credentials,
    }

    if (!!body) {
        if (typeof body == 'string') {
            extra['body'] = body
        } else {
            extra['body'] = JSON.stringify(body)
        }
    }

    let response = await fetch(url, extra);
    let status = response.status;
    let {successful, message} = await checkStatus(status);

    if (!!fetchJson) {
        response = await response.json();

        if (!successful) {
            let detail = response.detail || response.error
            if (!!detail) {
                if (typeof detail == 'string') {
                    message = detail
                } else {
                    message = JSON.stringify(detail)
                }
            }
        }
    }

    return {
        "response": response,
        "isSuccessful": successful,
        "message": message,
        "status": status,
    }
}


async function checkStatus(status) {
    let result = {
        "successful": false,
        "message": null
    }
    if (status < 400) {
        result.successful = true
    } else if (status >= 400 && status < 500) {
        result.successful = false
        result.message = "Client error"
    } else {
        result.successful = false
        result.message = "Server error"
    }
    return result
}
