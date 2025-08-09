# VidFace Backend API

A FastAPI-based backend for the VidFace AI Avatar Video Generator application.

## 🚀 Features

- **User Authentication**: JWT-based authentication with registration and login
- **Video Generation**: AI-powered avatar video creation with lip-sync
- **Voice Synthesis**: Text-to-speech using ElevenLabs and OpenAI APIs
- **Avatar Management**: Avatar selection and customization
- **User Management**: Profile management and subscription handling
- **File Storage**: Local and S3 file storage support
- **Rate Limiting**: API rate limiting for fair usage

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with Python-Jose
- **Password Hashing**: bcrypt
- **File Processing**: OpenCV, MoviePy, Librosa
- **AI Integration**: OpenAI TTS, ElevenLabs
- **Task Queue**: Celery (for background processing)
- **Caching**: Redis
- **Documentation**: Auto-generated with Swagger UI

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
- Redis (optional, for caching)
- FFmpeg (for video processing)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb vidface_db
   
   # Run migrations (if using Alembic)
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

## 📚 API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost/vidface_db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `OPENAI_API_KEY` | OpenAI API key | None |
| `ELEVENLABS_API_KEY` | ElevenLabs API key | None |
| `AWS_ACCESS_KEY_ID` | AWS access key | None |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | None |
| `S3_BUCKET` | S3 bucket name | `vidface-videos` |

## 📁 Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── auth.py          # Authentication utilities
│   │   ├── config.py        # Configuration settings
│   │   └── database.py      # Database configuration
│   ├── models/
│   │   ├── user.py          # User model
│   │   ├── video.py         # Video model
│   │   ├── avatar.py        # Avatar model
│   │   └── subscription.py  # Subscription model
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── video.py         # Video generation endpoints
│   │   ├── avatar.py        # Avatar management endpoints
│   │   └── user.py          # User management endpoints
│   ├── schemas/
│   │   ├── user.py          # User Pydantic schemas
│   │   ├── video.py         # Video Pydantic schemas
│   │   ├── avatar.py        # Avatar Pydantic schemas
│   │   └── auth.py          # Auth Pydantic schemas
│   └── services/
│       ├── video_generator.py  # Video generation service
│       └── voice_service.py    # Voice synthesis service
├── static/                  # Static files (videos, images)
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
└── .env.example            # Environment variables template
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/login/form` - OAuth2 form login

### Video Generation
- `POST /api/video/create` - Create new video
- `GET /api/video/list` - List user videos
- `GET /api/video/{video_id}` - Get specific video
- `PUT /api/video/{video_id}` - Update video
- `DELETE /api/video/{video_id}` - Delete video
- `GET /api/video/{video_id}/download` - Download video

### Avatar Management
- `GET /api/avatar/list` - List available avatars
- `GET /api/avatar/categories` - Get avatar categories
- `GET /api/avatar/{avatar_id}` - Get specific avatar
- `GET /api/avatar/popular` - Get popular avatars
- `GET /api/avatar/featured` - Get featured avatars

### User Management
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile
- `GET /api/user/stats` - Get user statistics

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting
- CORS middleware
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy

## 🧪 Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app
```

## 🚀 Deployment

### Docker Deployment

1. **Build Docker image**
   ```bash
   docker build -t vidface-backend .
   ```

2. **Run container**
   ```bash
   docker run -p 8000:8000 vidface-backend
   ```

### Production Deployment

1. **Set production environment variables**
2. **Use production database (PostgreSQL)**
3. **Set up Redis for caching**
4. **Configure reverse proxy (Nginx)**
5. **Set up SSL certificates**
6. **Configure monitoring and logging**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

For support, email support@vidface.com or create an issue in the repository. 