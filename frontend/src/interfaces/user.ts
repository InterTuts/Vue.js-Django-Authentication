export interface BaseUser {
    email: string;
    password: string;
}

export interface BaseUserSocial {
    social_id: number;
    email: string;
    password: string;
}

export type BaseUserEmail = {
    email: string;
};

export type ChangePassword = {
    token: string;
    password: string;
};

export type UserSocial = {
    social_id: number;
    email: string;
};

export type UserLogin = {
    id: number;
    email: string;
    token: string;
};

export type User = {
    id: number;
    email: string;
};