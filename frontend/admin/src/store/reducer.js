import { SET_DETAIL_INFO, SET_PENDING } from "./constants"

const initState = {
    detailInfo: null,
    pending: false,
}

function reducer(state, action) {
    switch (action.type) {
        case SET_DETAIL_INFO: 
            return {
                ...state,
                detailInfo: action.payload
            }
        case SET_PENDING:
            return {
                ...state,
                pending: action.payload
            }
        default:
            throw new Error('Error Action!')
    }
}

export { initState }
export default reducer