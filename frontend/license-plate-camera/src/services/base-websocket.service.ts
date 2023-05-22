export default class BaseWebSocketAPI {
    private static _instance: BaseWebSocketAPI;
    private socket!: WebSocket;

    constructor() {
        this.socket = new WebSocket("ws://localhost:443/api/v1/license-plate-app/in_and_out/test_ws");
        // this.socket  = new WebSocket("ws://192.168.1.6:443/api/v1/check-vehicle-real-time/ws");
        // this.socket  = new WebSocket("ws://192.168.1.6:443/api/v1/check-vehicle-real-time/ws");
        // this.socket = new WebSocket("ws://localhost:8000/api/v1/check-vehicle-real-time/ws");
    }

    public static get Instance(): BaseWebSocketAPI {
        if (this._instance === undefined) {
            this._instance = new BaseWebSocketAPI();
        }
        return this._instance;
    }

    public openSocket() {
        this.socket.addEventListener('open', function (event) {
            console.log(event)
        });
    }

    public sendData(data: object) {
        this.socket.send(JSON.stringify(data));
    }

    public receiveData() {
        this.socket.addEventListener('message', function (event) {
            console.log(event.data);
        });
    }

    public receiveDataUseState(setState: any) {
        this.socket.addEventListener('message', function (event) {
            console.log(event.data);
            setState(JSON.parse(event.data));
        });
    }
}