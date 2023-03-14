import { global } from '../Environments/global-variables';
import axios from 'axios';
import LocalStorageService from './localStorage';

const baseURL = global.APILink.Root;
const localStore = new LocalStorageService();

export default class FetchAPIService {
    async get(url, checkAuth = false) {
        let auth = ''
        if (checkAuth) {
            auth = `Bearer ${localStore.getTokenAuth()}`;   
        }
        return axios.get(`${baseURL + url}`,
            {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: auth
                }
            }
        );
    }

    async post(url, object, checkAuth = false) {
        let auth = ''
        if (checkAuth) {
            auth = `Bearer ${localStore.getTokenAuth()}`
        }
        return axios.post(`${baseURL + url}`, object,
            {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: auth
                }
            }
        );
    }

    async postFormData(url, object, checkAuth = false) {
        let auth = '';
        if (checkAuth === true) {
            auth = `Bearer ${localStore.getTokenAuth()}`
        }
        return axios.post(`${baseURL + url}`, object,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: auth
                }
            }
        );
    }

    async put(url, object, checkAuth = false) {
        let auth = '';
        if (checkAuth === true) {
            auth = `Bearer ${localStore.getTokenAuth()}`
        }
        return axios.put(`${baseURL + url}`, object,
            {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: auth,                    
                }
            }
        );
    }

    async putFormData(url, object, checkAuth = false) {
        let auth = '';
        if (checkAuth === true) {
            auth = `Bearer ${localStore.getTokenAuth()}`
        }
        return axios.put(`${baseURL + url}`, object,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: auth,                    
                }
            }
        );
    }
}