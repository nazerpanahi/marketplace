import {sendJSONRequest} from './sendRequest'
import {SERVER_BASE_URL} from "../config/config"
const baseUrl = SERVER_BASE_URL;

const registerEndpoint = `${baseUrl}/auth/register`
const loginEndpoint = `${baseUrl}/auth/login`
const logoutEndpoint = `${baseUrl}/auth/logout`
const getUserEndpoint = `${baseUrl}/auth/getUser`
const getUserByIdEndpoint = `${baseUrl}/user/getUserById`

export async function registerUser(userData) {
    let {response, isSuccessful, message} = await sendJSONRequest(registerEndpoint, {method: 'POST', body: userData})
    if (isSuccessful) {
        return response
    } else {
        return {
            "error": message
        }
    }
}

export async function loginUser(userData) {
    let {response, isSuccessful, message} = await sendJSONRequest(loginEndpoint, {method: 'POST', body: userData})
    if (isSuccessful) {
        return response
    } else {
        return {
            "error": message
        }
    }
}

export async function logoutUser(token) {
    let headers = {
        'Content-Type': 'application/json',
    }
    if (!!token) {
        headers['Authorization'] = 'Bearer ' + token
    }
    let {response, isSuccessful, message} = await sendJSONRequest(logoutEndpoint, {method: 'POST', headers: headers})
    if (isSuccessful) {
        return response
    } else {
        return {
            "error": message
        }
    }
}

export async function getUser(token) {
    let headers = {
        'Content-Type': 'application/json',
    }
    if (!!token) {
        headers['Authorization'] = 'Bearer ' + token
    }

    let {response, isSuccessful, message} = await sendJSONRequest(getUserEndpoint, {headers: headers})
    if (isSuccessful) {
        return response
    } else {
        return {
            "error": message
        }
    }
}

export async function getUserById(id, token) {
    let headers = {
        'Content-Type': 'application/json',
    }
    if (!!token) {
        headers['Authorization'] = 'Bearer ' + token
    }

    let {response, isSuccessful, message} = await sendJSONRequest(getUserByIdEndpoint + '/' + id, {headers: headers})
    if (isSuccessful) {
        return response
    } else {
        return {
            "error": message
        }
    }
}
