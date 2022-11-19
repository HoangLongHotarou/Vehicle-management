import { BaseFetchAPI } from "../base-fecth-api.service";

export class FetchAPI extends BaseFetchAPI{
    constructor(){
        super('/api/v1/check-vehicle-real-time')
    }
}