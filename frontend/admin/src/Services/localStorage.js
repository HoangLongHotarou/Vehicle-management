export default class LocalStorageService {

    constructor() {
        this.tokenKey = 'token';
    }

    setTokenAuth(value) {
        localStorage.setItem(this.tokenKey, value);
    }

    getTokenAuth() {
        return localStorage.getItem(this.tokenKey);
    }

    deleteTokenAuth() {
        localStorage.removeItem(this.tokenKey);
    }

    setLocalStorage(key, value) {
        localStorage.setItem(key, value);
    }

    getLocalStorage(key) {
        return localStorage.getItem(key);
    }

    deleteLocalStorage(key) {
        localStorage.removeItem(key);
    }
}