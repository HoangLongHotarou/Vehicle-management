import { global } from '../Environments/global-variables';
import FetchAPIService from './fetchAPI';

const RegionURL = global.APILink.Region;

export default class RegionServices {
  constructor() {
    this.fetchAPI = new FetchAPIService();
  }

  async getAllRegions(pageNumber = 0) {
    return await this.fetchAPI.get(
      `${RegionURL}/?page=${pageNumber}&limit=10`,
      true,
    );
  }
}
