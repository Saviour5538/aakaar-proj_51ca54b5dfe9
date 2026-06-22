import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config: AxiosRequestConfig) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
});

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  token: string;
}

export interface CurrentUserResponse {
  id: string;
  username: string;
  email: string;
}

export interface FileUploadResponse {
  file_id: string;
}

export interface FileStatusResponse {
  file_id: string;
  status: string;
}

export interface FileListResponse {
  files: Array<{
    file_id: string;
    filename: string;
    status: string;
  }>;
}

export interface IngestDocumentsRequest {
  file_id: string;
}

export interface AIQueryRequest {
  query: string;
}

export interface AIQueryResponse {
  answer: string;
}

export interface QueryHistoryResponse {
  history: Array<{
    query_id: string;
    query: string;
    answer: string;
    timestamp: string;
  }>;
}

export const register = (data: RegisterRequest) =>
  api.post<AuthResponse>('/api/auth/register', data);

export const login = (data: LoginRequest) =>
  api.post<AuthResponse>('/api/auth/login', data);

export const logout = () => api.post('/api/auth/logout');

export const getCurrentUser = () =>
  api.get<CurrentUserResponse>('/api/auth/me');

export const uploadFile = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post<FileUploadResponse>('/api/files/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const listFiles = () =>
  api.get<FileListResponse>('/api/files');

export const getFileStatus = (file_id: string) =>
  api.get<FileStatusResponse>(`/api/files/${file_id}`);

export const ingestDocuments = (data: IngestDocumentsRequest) =>
  api.post('/api/ai/ingest', data);

export const aiQuery = (data: AIQueryRequest) =>
  api.post<AIQueryResponse>('/api/ai/query', data);

export const getQueryHistory = () =>
  api.get<QueryHistoryResponse>('/api/ai/history');