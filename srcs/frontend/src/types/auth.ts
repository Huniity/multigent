

export interface LoginForm {
  username: string;
  password: string;
}

export interface RegisterForm {
  email: string;
  username: string;
  password: string;
  confirmPassword: string;
}

export type FieldErrors<T> = Partial<Record<keyof T, string>>;
