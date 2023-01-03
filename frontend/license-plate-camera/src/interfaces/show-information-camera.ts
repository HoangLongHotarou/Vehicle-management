export interface info{
    message: string;
    date: string;
    time: string;
}

export interface ShowRegisterInfo{
    username: string;
    plate: string;
    role:string[];
    information: info;
}

export interface ShowNotRegisterInfo{
    plate: string;
    information: string;
}

export interface ShowUserInfo{
    register: ShowRegisterInfo[]
    not_registered: ShowNotRegisterInfo[]
    turn: string;
}