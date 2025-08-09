// api service for frontend-backend communication
class ApiService {
    constructor() {
        this.baseUrl = 'http://127.0.0.1:8000';
        this.token = localStorage.getItem('token');
    }

    // set auth token
    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    // remove auth token
    removeToken() {
        this.token = null;
        localStorage.removeItem('token');
    }

    // get auth headers
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        return headers;
    }

    // make api request
    async makeRequest(endpoint, options = {}) {
        try {
            const url = `${this.baseUrl}${endpoint}`;
            const config = {
                headers: this.getHeaders(),
                ...options
            };

            const response = await fetch(url, config);
            
            if (!response.ok) {
                // handle unauthorized globally
                if (response.status === 401) {
                    this.removeToken();
                }
                let errorBody = {};
                try { errorBody = await response.json(); } catch (_) {}
                const message = (errorBody && errorBody.detail) ? errorBody.detail : `http error! status: ${response.status}`;
                const err = new Error(message);
                err.status = response.status;
                throw err;
            }

            return await response.json();
        } catch (error) {
            console.error('api request failed:', error);
            throw error;
        }
    }

    // authentication endpoints
    async register(userData) {
        return await this.makeRequest('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async login(credentials) {
        const response = await this.makeRequest('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
        
        if (response.access_token) {
            this.setToken(response.access_token);
        }
        
        return response;
    }

    async logout() {
        this.removeToken();
        return { message: 'logged out successfully' };
    }

    // user management endpoints
    async getProfile() {
        return await this.makeRequest('/api/user/profile');
    }

    async updateProfile(profileData) {
        return await this.makeRequest('/api/user/profile', {
            method: 'PUT',
            body: JSON.stringify(profileData)
        });
    }

    async getUserStats() {
        return await this.makeRequest('/api/user/stats');
    }

    // avatar management endpoints
    async getAvatars() {
        return await this.makeRequest('/api/avatar/list');
    }

    async getAvatarCategories() {
        return await this.makeRequest('/api/avatar/categories');
    }

    async getAvatar(avatarId) {
        return await this.makeRequest(`/api/avatar/${avatarId}`);
    }

    async getPopularAvatars() {
        return await this.makeRequest('/api/avatar/popular');
    }

    async getFeaturedAvatars() {
        return await this.makeRequest('/api/avatar/featured');
    }

    // video management endpoints
    async createVideo(videoData) {
        return await this.makeRequest('/api/video/create', {
            method: 'POST',
            body: JSON.stringify(videoData)
        });
    }

    async getVideos() {
        return await this.makeRequest('/api/video/list');
    }

    async getVideo(videoId) {
        return await this.makeRequest(`/api/video/${videoId}`);
    }

    async updateVideo(videoId, videoData) {
        return await this.makeRequest(`/api/video/${videoId}`, {
            method: 'PUT',
            body: JSON.stringify(videoData)
        });
    }

    async deleteVideo(videoId) {
        return await this.makeRequest(`/api/video/${videoId}`, {
            method: 'DELETE'
        });
    }

    async downloadVideo(videoId) {
        return await this.makeRequest(`/api/video/${videoId}/download`);
    }

    // health check
    async healthCheck() {
        return await this.makeRequest('/health');
    }
}

// create global api instance
const api = new ApiService();

// export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ApiService;
} else {
    window.ApiService = ApiService;
    window.api = api;
} 