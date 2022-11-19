export interface Pagination{
    total: number;
    page_sizes: number;
    page: number;
    limit: number;
    list: Array<any>;
}