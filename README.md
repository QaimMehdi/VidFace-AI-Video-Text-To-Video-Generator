# VidFace - AI Avatar Video Generator Frontend

A modern, responsive web application for generating AI-powered talking avatar videos from text scripts. Built with HTML5, CSS3, and vanilla JavaScript, inspired by the clean design of VEED.io.

## 🚀 Features

### Core Functionality
- **Text-to-Video Generation**: Convert text scripts into talking avatar videos
- **Avatar Selection**: Choose from predefined avatars or upload your own photo
- **Voice Customization**: Multiple voice tones and languages
- **Video Settings**: Resolution, duration, and background options
- **Template System**: Quick-start templates for common use cases

### User Experience
- **Modern UI/UX**: Clean, professional design with smooth animations
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Real-time Validation**: Form validation and character counting
- **Interactive Elements**: Hover effects, loading states, and notifications
- **Accessibility**: Keyboard navigation and screen reader support

### Technical Features
- **Vanilla JavaScript**: No framework dependencies
- **CSS Grid & Flexbox**: Modern layout techniques
- **Intersection Observer**: Performance-optimized animations
- **File Upload**: Image validation and preview
- **Local Storage**: Save user preferences

## 📁 Project Structure

```
vidface-frontend/
├── index.html          # Main HTML file
├── styles.css          # CSS styles and responsive design
├── script.js           # JavaScript functionality
└── README.md           # Project documentation
```

## 🎨 Design System

### Color Palette
- **Primary**: Purple gradient (`#667eea` to `#764ba2`)
- **Secondary**: Dark gray (`#1f2937`)
- **Background**: Light gray (`#f9fafb`)
- **Text**: Dark gray (`#1f2937`) and medium gray (`#6b7280`)
- **Success**: Green (`#10b981`)
- **Error**: Red (`#ef4444`)

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Sizes**: 12px to 48px (responsive)

### Components
- **Buttons**: Primary, secondary, and gradient variants
- **Cards**: Rounded corners with subtle shadows
- **Forms**: Clean inputs with focus states
- **Navigation**: Sticky header with dropdown indicators

## 🛠️ Installation & Setup

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Local web server (optional, for development)

### Quick Start
1. Clone or download the project files
2. Open `index.html` in your web browser
3. Start creating AI avatar videos!

### Development Setup
```bash
# Using Python (if available)
python -m http.server 8000

# Using Node.js (if available)
npx serve .

# Using PHP (if available)
php -S localhost:8000
```

Then visit `http://localhost:8000` in your browser.

## 📱 Responsive Breakpoints

- **Desktop**: 1200px and above
- **Tablet**: 768px to 1199px
- **Mobile**: 480px to 767px
- **Small Mobile**: Below 480px

## 🎯 Usage Guide

### 1. Writing Your Script
- Type or paste your text in the main input area
- Use the character counter to stay within limits (1000 characters)
- Try the quick templates for inspiration

### 2. Choosing an Avatar
- Select from 4 predefined professional avatars
- Upload your own photo (max 5MB, JPG/PNG)
- Click on any avatar to select it

### 3. Customizing Voice & Language
- **Voice Tone**: Friendly, Professional, Energetic, Calm, Authoritative
- **Voice Speed**: Slow, Normal, Fast
- **Language**: 10+ languages including English, Spanish, French, etc.
- **Accent**: American, British, Australian, Canadian

### 4. Video Settings
- **Resolution**: 720p, 1080p, 4K
- **Duration**: 15s, 30s, 1min, 2min, Custom
- **Background**: Blurred, Office, Studio, Outdoor, Custom

### 5. Generating & Downloading
- Click "Generate Video" to start the process
- Wait for the AI to create your video (simulated)
- Preview the result in the video player
- Download as MP4 or share directly

## 🔧 Customization

### Adding New Templates
Edit the `templates` object in `script.js`:

```javascript
const templates = {
    // ... existing templates
    newTemplate: "Your new template script here...",
};
```

### Modifying Colors
Update CSS custom properties in `styles.css`:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    /* ... other colors */
}
```

### Adding New Languages
Update the language select options in `index.html`:

```html
<option value="new-lang">New Language</option>
```

## 🚀 Future Enhancements

### Planned Features
- **Real AI Integration**: Connect to actual video generation APIs
- **Voice Cloning**: Upload voice samples for custom voices
- **Video Editor**: Basic editing capabilities
- **Project Management**: Save and organize video projects
- **Collaboration**: Share projects with team members

### Technical Improvements
- **Progressive Web App**: Offline functionality and app-like experience
- **WebAssembly**: Performance optimization for video processing
- **WebRTC**: Real-time video preview
- **Service Workers**: Background processing and caching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

**VidFace** - Transform text into engaging talking avatar videos with AI-powered technology. 🎬✨ 