import { BaseFetchAPI } from "../base-fecth-api.service";

export class FetchAPI extends BaseFetchAPI {
    constructor() {
        super('http://localhost:8003', '/api/v1/license-plate-app')
    }
}