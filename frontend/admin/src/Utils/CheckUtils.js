import AuthService from "../Services/auth";

export default class CheckUtils {
    constructor() {
        this.auth = new AuthService();
    }

    unauthenticated() {
        alert('Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại!');
        this.auth.logout();
    }

    serverError() {
        alert('Lỗi Server hoặc Không có kết nối mạng!\nVui lòng thử lại sau.');
    }

    async catchError(error) {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    this.unauthenticated();
                    break;   
                default:
                    break;        
            }
        }
        else {
            this.serverError();
        }
    }
}