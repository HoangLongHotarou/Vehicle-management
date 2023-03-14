import { SET_DETAIL_INFO, SET_PENDING } from "./constants";

export const setDetailInfo = payload => ({
    type: SET_DETAIL_INFO,
    payload
})

export const setPending = payload => ({
    type: SET_PENDING,
    payload
})