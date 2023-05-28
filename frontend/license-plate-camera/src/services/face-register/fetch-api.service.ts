import { BaseFetchAPI } from "../base-fecth-api.service";

export class FetchAPI extends BaseFetchAPI {
    constructor() {
        super('http://localhost:8005', '/api/v1/vehicle-face-recognition')
    }
}