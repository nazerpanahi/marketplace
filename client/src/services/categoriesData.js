import {sendJSONRequest} from './sendRequest'
import {SERVER_BASE_URL} from "../config/config"
const baseUrl = SERVER_BASE_URL;

export async function getAll() {
    let endpoint = `${baseUrl}/categories/`
    let {response, isSuccessful, message} = await sendJSONRequest(endpoint)
    if (isSuccessful) {
        return response
    } else {
        return {
            "error": message
        }
    }
}
