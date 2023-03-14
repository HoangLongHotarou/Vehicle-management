export default class FuncUtils {

    getDateNow() {
        let d = new Date();
        return [
            d.getFullYear(),
            ('0' + (d.getMonth() + 1)).slice(-2),
            ('0' + d.getDate()).slice(-2)
        ].join('-'); 
    }

    formatDate(date, express, type) { 
        let kq;
        let strArr = date.split(express);
        switch (type) {
            case 'dd-mm-yyyy':                 
                kq = [
                    strArr[2],
                    strArr[1],
                    strArr[0]
                ].join('-'); 
                break;
            default:
                kq = date;
        }
        return kq;
    }
}