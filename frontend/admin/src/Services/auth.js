import {global} from '../Environments/global-variables';
import FetchAPIService from './fetchAPI';
import LocalStorageService from './localStorage';

const AuthURL = global.APILink.Auth;
const userLocalKey = 'user';

export default class AuthService {
    constructor(){
        this.fetchAPI = new FetchAPIService();
        this.localStore = new LocalStorageService();
    }

    async login(obj) {
        let check = true;
        if (!this.checkLogin()) {
            await this.fetchAPI.post(`${AuthURL}/login/`, obj).then(async res => {
                this.localStore.setTokenAuth(res.data.access_token);    
                await this.saveInfo();
            }).catch(err => {
                check = false;
            });                 
        }
        else {
            console.log('Login Already!');
        }
        return check;  
    }

    logout() {
        this.localStore.deleteTokenAuth();
        this.localStore.deleteLocalStorage(userLocalKey);
        window.location.reload();
    }

    async saveInfo() {
        await this.fetchAPI.get(`${AuthURL}/users/me/`, true).then(res => {
            this.localStore.setLocalStorage(userLocalKey, JSON.stringify(res.data));
        });
    }

    getInfo() {
        return JSON.parse(this.localStore.getLocalStorage(userLocalKey));
    }

    updateAvatarLocalStorage(avatarLink) {
        let info = this.getInfo();
        info.avatar = avatarLink;
        this.localStore.setLocalStorage(userLocalKey, JSON.stringify(info));
    }

    updateInfoLocalStorage(infoUpdate) {
        let info = this.getInfo();
        info.phone_number = infoUpdate.phone_number;
        info.last_name = infoUpdate.last_name;
        info.first_name = infoUpdate.first_name;
        this.localStore.setLocalStorage(userLocalKey, JSON.stringify(info));
    }

    async updateAvatar(obj) {
        return await this.fetchAPI.putFormData(`${AuthURL}/users/me/avatar`, obj, true);
    }

    async updateInfo(obj) {
        return await this.fetchAPI.put(`${AuthURL}/users/me`, obj, true);
    }

    checkLogin() {
        return (this.localStore.getTokenAuth()) ? true : false;
    }

    async getAllUser(pageNumber = 0) {
        return await this.fetchAPI.get(`${AuthURL}/users/?page=${pageNumber}&limit=20`, true);
    }

    async getUser(idUser) {
        return await this.fetchAPI.get(`${AuthURL}/users/${idUser}`, true);
    }
}