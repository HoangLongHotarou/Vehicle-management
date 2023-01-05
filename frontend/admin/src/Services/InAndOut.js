import {global} from '../Environments/global-variables';
import FetchAPIService from './fetchAPI';

const InAndOutURL = global.APILink.InAndOut;

export default class InAndOut {
    constructor(){
        this.fetchAPI = new FetchAPIService();
    }

    async searchInAndOut(obj, pageNumber = 0) {
        return await this.fetchAPI.post(`${InAndOutURL}/search_in_and_out/?page=${pageNumber}&limit=20`, obj);
    }

    async statisticInAndOut(date) {
        return await this.fetchAPI.get(`${InAndOutURL}/statistic_in_and_out?date=${date}`);
    }
}