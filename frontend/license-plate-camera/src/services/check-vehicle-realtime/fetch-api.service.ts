import { BaseFetchAPI } from "../base-fecth-api.service";

export class FetchAPI extends BaseFetchAPI {
    constructor() {
        super('http://localhost:8000', '/api/v1/check-vehicle-real-time')
        // super('http://localhost:80', '/api/v1/check-vehicle-real-time')
    }
}