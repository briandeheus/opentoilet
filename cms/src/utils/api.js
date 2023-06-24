import { useStore } from "../store";

const API_URL = window.location.protocol + "//localhost:8000";

const prependSlash = (path) => {

    if (path.charAt(path.length - 1) !== "/") {
        return `${path}/`
    }
    return path

}

async function request(method, path, data = {}) {

    const { apiToken } = useStore.getState();

    const headers = {
        "Content-Type": "application/json",
    };

    if (apiToken) {
        headers["Authorization"] = `Bearer ${apiToken}`;
    }

    const fetchConfig = { method, headers }

    if (["post", "put"].includes(method.toLowerCase()) === true) {
        fetchConfig["body"] = JSON.stringify(data);
    }


    const response = await fetch(`${API_URL}${path}`, fetchConfig);
    const statusCode = response.status;
    const json = await response.json();

    return [json, statusCode];

}

async function post(path, data = {}) {

    return request("post", prependSlash(path), data);

}

async function put(path, data = {}) {

    return request("put", prependSlash(path), data);

}

async function get(path, params = null) {

    if (params) {
        const searchParams = new URLSearchParams(params);
        path = `${path}?${searchParams.toString()}`;
    }

    return request("get", path);
}

export default { post, get, put }