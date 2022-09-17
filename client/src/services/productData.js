import {sendJSONRequest} from './sendRequest';
import {SERVER_BASE_URL} from "../config/config";
const baseUrl = SERVER_BASE_URL;

export async function getAll(page, category, query, token) {
    let headers = {
        'Content-Type': 'application/json',
    }
    if (!!token) {
        headers['Authorization'] = 'Bearer ' + token
    }
    
    let endpoint = null
    if (query !== "" && query !== undefined) {
        endpoint = `${baseUrl}/products/?page=${page}&search=${query}`
    } else if (category && category !== 'all') {
        endpoint = `${baseUrl}/products/${category}/?page=${page}`
    } else {
        endpoint = `${baseUrl}/products/?page=${page}`
    }

    let {response, isSuccessful, message} = await sendJSONRequest(endpoint, {headers: headers})
    if (isSuccessful) {
        return response
    } else {
        return {
            "error": message
        }
    }
}

export async function getSpecific(id, token) {
    let headers = {
        'Content-Type': 'application/json',
    }
    if (!!token) {
        headers['Authorization'] = 'Bearer ' + token
    }
    let endpoint = `${baseUrl}/products/specific/${id}`
    let {response, isSuccessful, message} = await sendJSONRequest(endpoint, {headers: headers})
    if (isSuccessful) {
        return response
    } else {
        return {
            "error": message
        }
    }
}

export async function createProduct(product, token) {
    let headers = {
        'Content-Type': 'application/json',
    }
    if (!!token) {
        headers['Authorization'] = 'Bearer ' + token
    }
    let endpoint = `${baseUrl}/products/create`
    let {response, isSuccessful, message} = await sendJSONRequest(endpoint, {method: 'POST', headers: headers, body: product})
    if (isSuccessful) {
        return response
    } else {
        return {
            "error": message
        }
    }
}

export async function editProduct(id, product, token) {
    let endpoint = `${baseUrl}/products/edit/${id}`
    let headers = {
        'Content-Type': 'application/json',
    }
    if (!!token) {
        headers['Authorization'] = 'Bearer ' + token
    }
    product.id = id
    let {response, isSuccessful, message} = await sendJSONRequest(endpoint, {method: 'PATCH', headers: headers, body: product})
    if (isSuccessful) {
        return response
    } else {
        return {
            "error": message
        }
    }
}
