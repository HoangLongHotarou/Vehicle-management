import axios from "axios"

export class BaseFetchAPI{
    private resourceUrl: string;

    constructor(pathUrl: string){
        // this.resourceUrl = 'http://127.0.0.1:443'
        this.resourceUrl = 'http://localhost:443'
        // this.resourceUrl = 'http://192.168.1.6:443'
        // this.resourceUrl = 'http://54.238.251.141'
        this.resourceUrl += pathUrl;
    }

    async get(urls: string){
        return axios.get(`${this.resourceUrl+urls}`,{
            headers: {
            'Content-Type': 'application/json',
            }
        });
    }

    async put(urls: string, obj: object){
        return axios.put(`${this.resourceUrl+urls}`,obj,{
            headers: {
                'Content-Type': 'application/json',
            }
        })
    }
}