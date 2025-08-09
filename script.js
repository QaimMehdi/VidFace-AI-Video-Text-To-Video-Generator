// DOM Elements
const topBanner = document.querySelector('.top-banner');
const closeBannerBtn = document.querySelector('.close-btn');
const avatarOptions = document.querySelectorAll('.avatar-option');
const avatarUpload = document.getElementById('avatar-upload');
const uploadOption = document.querySelector('.upload-option');
const scriptInput = document.querySelector('.script-input');
const generateBtn = document.querySelector('.generate-btn');
const templateBtns = document.querySelectorAll('.template-btn');
const previewSection = document.getElementById('preview-section');
const previewVideo = document.getElementById('preview-video');
const loader = document.getElementById('loader');
const navLinks = document.querySelectorAll('.nav-link');

// Debug DOM elements
console.log('DOM Elements found:');
console.log('- scriptInput:', scriptInput);
console.log('- generateBtn:', generateBtn);
console.log('- previewSection:', previewSection);

// Review carousel variables
let reviewItems;
let progressFill;
let currentReviewIndex = 0;
let reviewInterval;

// Template scripts
const templates = {
    ad: "Introducing our revolutionary product! Transform your workflow with cutting-edge AI technology. Boost productivity by 300% and save hours every day. Don't miss out on this game-changing solution that's already trusted by thousands of professionals worldwide. Get started today and experience the future of work!",
    
    promo: "🎉 Special Offer Alert! 🎉 Get 50% off our premium AI avatar generator for a limited time only. Create professional talking videos in minutes, not hours. Perfect for marketing, education, and entertainment. Use code SPECIAL50 at checkout and start creating amazing content today!",
    
    tutorial: "Welcome to our step-by-step tutorial! Today, I'll show you how to create stunning AI avatar videos. First, write your script in the text area. Then, choose your preferred avatar and voice settings. Finally, click generate and download your video in seconds! It's that simple to create professional content.",
    
    presentation: "Good morning everyone! Today's presentation will cover our quarterly results and future roadmap. We've achieved remarkable growth with a 45% increase in revenue and expanded to three new markets. Let me walk you through the key highlights and our strategic initiatives for the upcoming quarter.",
    
    welcome: "Welcome to our amazing platform! We're thrilled to have you here. Whether you're a content creator, marketer, or educator, you'll find everything you need to create professional videos that engage and inspire your audience. Let's start creating something incredible together!",
    
    announcement: "Exciting news everyone! We're launching our brand new AI video generator that will revolutionize how you create content. Starting next week, you'll have access to advanced features, more avatars, and faster processing times. Stay tuned for more updates and get ready to transform your video creation process!",
    
    testimonial: "I've been using this AI video generator for three months now, and it's completely transformed my content creation process. The quality is incredible, the avatars look realistic, and I can create professional videos in minutes instead of hours. It's been a game-changer for my business!",
    
    product: "Let me show you our amazing new product! This innovative solution combines cutting-edge technology with user-friendly design. Watch as I demonstrate its key features: lightning-fast processing, crystal-clear audio, and stunning visual quality. Experience the difference that professional AI technology makes!"
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Starting initialization...');
    
    // Prevent any form submissions globally
    document.addEventListener('submit', function(e) {
        console.log('Form submission detected and prevented:', e.target);
        e.preventDefault();
        e.stopPropagation();
        return false;
    });
    
    // Also prevent any navigation
    document.addEventListener('click', function(e) {
        // If clicking on a button that might cause navigation, prevent it
        if (e.target.tagName === 'BUTTON' && e.target.classList.contains('generate-btn')) {
            console.log('Intercepted generate button click in global handler');
            // Temporarily comment out to see if this is blocking
            // e.preventDefault();
            // e.stopPropagation();
            // return false;
        }
    }, true); // Use capture phase to intercept early
    
    // Prevent page unload during video generation
    let isGenerating = false;
    window.addEventListener('beforeunload', function(e) {
        if (isGenerating) {
            e.preventDefault();
            e.returnValue = '';
            return '';
        }
    });
    
    // Override the handleVideoGeneration to set the flag
    const originalHandleVideoGeneration = handleVideoGeneration;
    window.handleVideoGeneration = async function() {
        isGenerating = true;
        try {
            await originalHandleVideoGeneration();
        } finally {
            isGenerating = false;
        }
    };
    
    // Initialize review carousel elements after DOM is loaded
    reviewItems = document.querySelectorAll('.review-item');
    progressFill = document.getElementById('progress-fill');
    
    console.log('DOM Elements found:');
    console.log('- Review items:', reviewItems.length);
    console.log('- Progress fill:', progressFill);
    
    initializeEventListeners();
    setupAnimations();
    initializeLoader();
    initializeSmoothScrolling();
    initializeReviewCarousel();
    initializeLogoNavigation();
    initializeUserProfile();
    
    // test backend connection
    testBackendConnection();
});

// test backend connection
async function testBackendConnection() {
    try {
        console.log('testing backend connection...');
        console.log('API service available:', typeof api !== 'undefined');
        if (typeof api === 'undefined') {
            console.error('API service not loaded!');
            return;
        }
        const response = await api.healthCheck();
        console.log('✅ backend connection successful:', response);
        showNotification('backend connected successfully!', 'success');
    } catch (error) {
        console.error('❌ backend connection failed:', error);
        showNotification('backend connection failed. please start the server.', 'error');
    }
}

// Logo navigation functionality
function initializeLogoNavigation() {
    const logoLink = document.querySelector('.logo a');
    if (logoLink) {
        logoLink.addEventListener('click', function(e) {
            e.preventDefault();
            scrollToTop();
        });
    }
}

// Scroll to top function
function scrollToTop() {
    const currentPage = window.location.pathname;
    
    if (currentPage === '/' || currentPage === '/index.html' || currentPage.endsWith('index.html')) {
        // We're on the landing page, scroll to hero section
        const heroSection = document.getElementById('hero-section');
        if (heroSection) {
            smoothScrollTo(heroSection);
        } else {
            // Fallback to top of page
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    } else {
        // We're on a different page, navigate to homepage
        window.location.href = 'index.html';
    }
}

// Review carousel functionality
function initializeReviewCarousel() {
    console.log('Initializing review carousel...');
    console.log('Review items found:', reviewItems.length);
    console.log('Progress fill found:', progressFill);
    
    if (reviewItems.length > 0 && progressFill) {
        // Make sure first review is active
        reviewItems.forEach((item, index) => {
            if (index === 0) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
        
        // Start automatic transitions
        startReviewCarousel();
    } else {
        console.log('Review elements not found, retrying in 1 second...');
        setTimeout(initializeReviewCarousel, 1000);
    }
}

function startReviewCarousel() {
    if (reviewItems.length <= 1) return;
    
    reviewInterval = setInterval(showNextReview, 3000);
    
    // Pause on hover
    const reviewsGrid = document.getElementById('reviews-grid');
    if (reviewsGrid) {
        reviewsGrid.addEventListener('mouseenter', () => clearInterval(reviewInterval));
        reviewsGrid.addEventListener('mouseleave', () => {
            reviewInterval = setInterval(showNextReview, 3000);
        });
    }
}

function showNextReview() {
    // Remove active class from current review
    reviewItems[currentReviewIndex].classList.remove('active');
    
    // Move to next review
    currentReviewIndex = (currentReviewIndex + 1) % reviewItems.length;
    
    // Add active class to new review
    reviewItems[currentReviewIndex].classList.add('active');
    
    // Update progress bar
    if (progressFill) {
        const progress = ((currentReviewIndex + 1) / reviewItems.length) * 100;
        progressFill.style.width = progress + '%';
    }
}

// Initialize loader
function initializeLoader() {
    if (loader) {
        // Hide loader after 2 seconds
        setTimeout(() => {
            loader.style.opacity = '0';
            setTimeout(() => {
                loader.style.display = 'none';
            }, 300);
        }, 2000);
    }
}

// Initialize smooth scrolling
function initializeSmoothScrolling() {
    // Add smooth scrolling to all internal links
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                smoothScrollTo(targetElement);
            }
        });
    });
}

// Smooth scroll to element
function smoothScrollTo(element) {
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - 80; // Account for fixed header
    
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

// Initialize event listeners
function initializeEventListeners() {
    // Close banner
    if (closeBannerBtn) {
        closeBannerBtn.addEventListener('click', () => {
            topBanner.style.display = 'none';
        });
    }

    // Avatar selection
    avatarOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove active class from all options
            avatarOptions.forEach(opt => opt.classList.remove('active'));
            // Add active class to clicked option
            this.classList.add('active');
        });
    });

    // Avatar upload
    if (uploadOption) {
        uploadOption.addEventListener('click', () => {
            avatarUpload.click();
        });
    }

    if (avatarUpload) {
        avatarUpload.addEventListener('change', handleAvatarUpload);
    }

    // Generate button
    if (generateBtn) {
        console.log('Setting up generate button event listener');
        generateBtn.addEventListener('click', (e) => {
            console.log('Generate button clicked - preventing default behavior');
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            
            // Additional prevention
            if (e.defaultPrevented) {
                console.log('Default already prevented');
            }
            
            console.log('About to call handleVideoGeneration');
            // Call the handler
            handleVideoGeneration();
            
            // Return false as additional prevention
            return false;
        });
        
        // Also prevent any form submission from this button
        generateBtn.setAttribute('type', 'button');
        generateBtn.setAttribute('form', '');
        console.log('Generate button setup complete');
    } else {
        console.error('Generate button not found!');
    }

    // Template buttons
    templateBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const templateType = this.getAttribute('data-template');
            if (templates[templateType]) {
                scriptInput.value = templates[templateType];
                validateForm();
                showNotification('Template loaded successfully!', 'success');
            }
        });
    });

    // Script input validation
    if (scriptInput) {
        scriptInput.addEventListener('input', validateForm);
        scriptInput.addEventListener('input', debounce(updateCharacterCount, 300));
    }

    // Navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Handle avatar upload
function handleAvatarUpload(event) {
    const file = event.target.files[0];
    
    if (file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            showNotification('Please select a valid image file.', 'error');
            return;
        }
        
        // Validate file size (5MB limit)
        if (file.size > 5 * 1024 * 1024) {
            showNotification('File size must be less than 5MB.', 'error');
            return;
        }
        
        // Create preview
        const reader = new FileReader();
        reader.onload = function(e) {
            const uploadOption = document.querySelector('.upload-option');
            if (uploadOption) {
                uploadOption.innerHTML = `
                    <img src="${e.target.result}" alt="Uploaded Avatar" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover;">
                    <span>Custom Avatar</span>
                `;
                uploadOption.classList.add('active');
            }
        };
        reader.readAsDataURL(file);
        
        showNotification('Avatar uploaded successfully!', 'success');
    }
}

// Handle video generation with backend integration
async function handleVideoGeneration() {
    console.log('handleVideoGeneration called');
    
    const script = scriptInput.value.trim();
    console.log('Script value:', script);
    
    if (!script) {
        console.log('No script provided');
        showNotification('Please enter a script to generate the video.', 'error');
        return;
    }

    // Check if user is logged in
    const token = localStorage.getItem('token');
    console.log('Token exists:', !!token);
    if (!token) {
        console.log('No token found, redirecting to signin');
        showNotification('Please sign in to generate videos.', 'error');
        // redirect to signin page
        setTimeout(() => {
            window.location.href = 'signin.html';
        }, 2000);
        return;
    }

    console.log('Starting video generation process...');

    // Show loading state
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    generateBtn.classList.add('loading');

    try {
        // Get selected avatar (default to 1 if none selected)
        const selectedAvatar = document.querySelector('.avatar-option.active');
        const avatarId = selectedAvatar ? parseInt(selectedAvatar.getAttribute('data-avatar')) : 1;
        
        // Get language setting (default to English)
        const language = 'en';
        
        // Prepare video data according to backend schema
        const videoData = {
            title: `Video - ${new Date().toLocaleDateString()}`,
            description: script.substring(0, 100) + '...',
            script: script,
            avatar_id: avatarId,
            language: language
        };

        console.log('sending video data to backend:', videoData);
        
        // Call backend api with timeout
        const response = await Promise.race([
            api.createVideo(videoData),
            new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Request timeout')), 30000)
            )
        ]);
        
        console.log('video creation response:', response);
        
        // Hide loading state
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-bolt"></i> Generate Video';
        generateBtn.classList.remove('loading');

        // Show preview section
        showPreviewSection(response);

        // Scroll to preview
        previewSection.scrollIntoView({ behavior: 'smooth' });

        showNotification('Video generation started! Check back in a few minutes.', 'success');
        
    } catch (error) {
        console.error('video generation failed:', error);
        
        // Hide loading state
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-bolt"></i> Generate Video';
        generateBtn.classList.remove('loading');
        
        // Unauthorized: force sign-in
        if (error && error.status === 401) {
            showNotification('could not validate credentials. please sign in again.', 'error');
            setTimeout(() => {
                window.location.href = 'signin.html';
            }, 1200);
            return;
        }
        
        // Handle timeout
        if (error.message === 'Request timeout') {
            showNotification('Video generation is taking longer than expected. Please check back later.', 'info');
            return;
        }
        
        // Show detailed error message
        let errorMessage = 'Failed to generate video. Please try again.';
        if (error.message) {
            try {
                const errorData = JSON.parse(error.message);
                if (errorData.detail && Array.isArray(errorData.detail)) {
                    errorMessage = errorData.detail.map(d => d.msg).join(', ');
                } else if (errorData.detail) {
                    errorMessage = errorData.detail;
                }
            } catch (e) {
                errorMessage = error.message;
            }
        }
        
        showNotification(errorMessage, 'error');
    }
}

// Show preview section with backend data
function showPreviewSection(videoData) {
    previewSection.style.display = 'block';
    previewSection.classList.add('fade-in');

    // clear any previous source
    const sourceEl = previewVideo.querySelector('source');
    if (sourceEl) {
        sourceEl.src = '';
    }
    previewVideo.removeAttribute('src');
    previewVideo.load();

    // If we have a video id, poll until it's ready then load
    if (videoData && videoData.id) {
        pollForVideoCompletion(videoData.id);
    } else {
        showNotification('could not start preview: missing video id', 'error');
    }

    // Update download button to use video id
    const downloadBtn = previewSection.querySelector('.btn-primary');
    if (downloadBtn && videoData && videoData.id) {
        downloadBtn.onclick = () => downloadVideo(videoData.id);
    }
}

function setVideoSource(url) {
    const sourceEl = previewVideo.querySelector('source');
    if (sourceEl) {
        sourceEl.src = url;
        previewVideo.load();
    } else {
        previewVideo.src = url;
    }
}

// Poll for video completion
async function pollForVideoCompletion(videoId) {
    let attempts = 0;
    const maxAttempts = 120; // up to 2 minutes
    
    const poll = async () => {
        try {
            console.log(`Polling attempt ${attempts + 1} for video ${videoId}`);
            
            // First check if backend is reachable
            try {
                await api.healthCheck();
            } catch (healthError) {
                console.log('Backend not reachable, retrying in 2s...');
                attempts++;
                if (attempts < maxAttempts) {
                    setTimeout(poll, 2000);
                } else {
                    showNotification('Backend is not responding. Please refresh the page.', 'error');
                }
                return;
            }
            
            const response = await api.getVideo(videoId);
            console.log('Video status response:', response);
            
            if (response.status === 'completed') {
                console.log('Video completed!');
                const videoUrl = `http://127.0.0.1:8000/generated/${videoId}.mp4`;
                console.log('Trying to load video from:', videoUrl);
                
                // verify file is reachable before setting src
                try {
                    const headResp = await fetch(videoUrl, { method: 'HEAD' });
                    console.log('HEAD response status:', headResp.status);
                    if (headResp.ok) {
                        console.log('Video file is accessible, setting source');
                        setVideoSource(videoUrl);
                        showNotification('Video ready!', 'success');
                    } else {
                        console.log('Video file not accessible, retrying...');
                        // try again shortly if race condition
                        setTimeout(poll, 750);
                    }
                } catch (error) {
                    console.log('Error checking video file:', error);
                    setTimeout(poll, 750);
                }
                return;
            } else if (response.status === 'failed') {
                console.log('Video generation failed:', response.error_message);
                showNotification('Video generation failed. Please try again.', 'error');
                return;
            } else {
                console.log('Video still processing, status:', response.status, 'progress:', response.progress);
            }
            
            attempts++;
            if (attempts < maxAttempts) {
                setTimeout(poll, 1000); // Poll every second
            } else {
                showNotification('Video generation is taking longer than expected. Please check back later.', 'info');
            }
        } catch (error) {
            console.error('Error polling for video completion:', error);
            attempts++;
            if (attempts < maxAttempts) {
                setTimeout(poll, 1000);
            } else {
                showNotification('Could not check video status. Please refresh and try again.', 'error');
            }
        }
    };
    
    poll();
}

// Download video function
async function downloadVideo(videoId) {
    try {
        showNotification('Preparing download...', 'info');
        const response = await api.downloadVideo(videoId);
        
        // Create download link
        const link = document.createElement('a');
        link.href = response.download_url || `http://127.0.0.1:8000/api/video/${videoId}/download`;
        link.download = `vidface-video-${videoId}.mp4`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showNotification('Download started!', 'success');
    } catch (error) {
        console.error('download failed:', error);
        showNotification('Download failed. Please try again.', 'error');
    }
}

// Validate form
function validateForm() {
    const script = scriptInput.value.trim();
    const isValid = script.length > 0;
    
    generateBtn.disabled = !isValid;
    generateBtn.style.opacity = isValid ? '1' : '0.6';
}

// Show notification
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
            <button class="notification-close"><i class="fas fa-times"></i></button>
        </div>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 16px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
    `;

    // Add notification styles to head if not exists
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            .notification-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .notification-close {
                background: none;
                border: none;
                color: white;
                cursor: pointer;
                margin-left: auto;
            }
        `;
        document.head.appendChild(style);
    }

    // Add close functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.remove();
    });

    // Add to page
    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Setup animations
function setupAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe all sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        observer.observe(section);
    });
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Update character count
function updateCharacterCount() {
    const count = scriptInput.value.length;
    const maxCount = 1000;
    
    // Update character counter if it exists
    const charCounter = document.querySelector('.char-counter');
    if (charCounter) {
        charCounter.textContent = `${count}/${maxCount}`;
        
        // Change color based on count
        if (count > maxCount * 0.9) {
            charCounter.style.color = '#ef4444';
        } else if (count > maxCount * 0.7) {
            charCounter.style.color = '#f59e0b';
        } else {
            charCounter.style.color = '#6b7280';
        }
    }
}

// Initialize user profile functionality
function initializeUserProfile() {
    const token = localStorage.getItem('token');
    const authButtons = document.getElementById('auth-buttons');
    const userProfile = document.getElementById('user-profile');
    
    if (token) {
        // User is logged in
        authButtons.style.display = 'none';
        userProfile.style.display = 'block';
        
        // Load user data
        loadUserData();
        
        // Initialize dropdown functionality
        initializeProfileDropdown();
    } else {
        // User is not logged in
        authButtons.style.display = 'flex';
        userProfile.style.display = 'none';
    }
}

// Load user data from backend
async function loadUserData() {
    try {
        const response = await api.getProfile();
        updateUserProfile(response);
    } catch (error) {
        console.error('Failed to load user data:', error);
        const authButtons = document.getElementById('auth-buttons');
        const userProfile = document.getElementById('user-profile');
        if (authButtons && userProfile) {
            authButtons.style.display = 'flex';
            userProfile.style.display = 'none';
        }
        if (error && error.status === 401) {
            showNotification('session expired. please sign in again.', 'error');
        }
        // Use default values for initial rendering if needed
        updateUserProfile({
            full_name: 'User',
            email: 'user@example.com'
        });
    }
}

// Update user profile display
function updateUserProfile(userData) {
    const userName = document.getElementById('user-name');
    const userAvatar = document.getElementById('user-avatar');
    const dropdownName = document.getElementById('dropdown-name');
    const dropdownEmail = document.getElementById('dropdown-email');
    const dropdownAvatar = document.getElementById('dropdown-avatar');
    
    // Update user name
    const displayName = userData.full_name || userData.username || 'User';
    userName.textContent = displayName;
    dropdownName.textContent = displayName;
    
    // Update user email
    dropdownEmail.textContent = userData.email || 'user@example.com';
    
    // Create dynamic avatar with user's initial
    const avatarUrl = userData.avatar_url;
    if (avatarUrl && avatarUrl !== 'https://via.placeholder.com/32x32/8b5cf6/ffffff?text=U') {
        // Use actual profile photo
        userAvatar.src = avatarUrl;
        dropdownAvatar.src = avatarUrl;
    } else {
        // Create avatar with user's initial
        const initial = getInitial(displayName);
        const avatarColor = getAvatarColor(displayName);
        
        // Create SVG avatar for user avatar (32x32)
        const userAvatarSvg = createInitialAvatar(initial, avatarColor, 32);
        userAvatar.src = userAvatarSvg;
        
        // Create SVG avatar for dropdown avatar (40x40)
        const dropdownAvatarSvg = createInitialAvatar(initial, avatarColor, 40);
        dropdownAvatar.src = dropdownAvatarSvg;
    }
}

// Get first initial from name
function getInitial(name) {
    if (!name || name.trim() === '') return 'U';
    return name.trim().charAt(0).toUpperCase();
}

// Generate consistent color based on name
function getAvatarColor(name) {
    const colors = [
        '#8b5cf6', // Purple
        '#3b82f6', // Blue
        '#10b981', // Green
        '#f59e0b', // Orange
        '#ef4444', // Red
        '#8b5cf6', // Purple
        '#06b6d4', // Cyan
        '#84cc16', // Lime
        '#f97316', // Orange
        '#ec4899'  // Pink
    ];
    
    // Generate hash from name for consistent color
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    
    return colors[Math.abs(hash) % colors.length];
}

// Create SVG avatar with initial
function createInitialAvatar(initial, color, size) {
    const fontSize = Math.floor(size * 0.5);
    const svg = `
        <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
            <circle cx="${size/2}" cy="${size/2}" r="${size/2}" fill="${color}"/>
            <text x="${size/2}" y="${size/2}" 
                  font-family="Inter, Arial, sans-serif" 
                  font-size="${fontSize}" 
                  font-weight="700" 
                  fill="white" 
                  text-anchor="middle" 
                  dominant-baseline="middle">
                ${initial}
            </text>
        </svg>
    `;
    
    return 'data:image/svg+xml;base64,' + btoa(svg);
}

// Initialize profile dropdown functionality
function initializeProfileDropdown() {
    const profileBtn = document.getElementById('profile-btn');
    const dropdownMenu = document.getElementById('dropdown-menu');
    const logoutBtn = document.getElementById('logout-btn');
    
    // Toggle dropdown on profile button click
    profileBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdownMenu.classList.toggle('show');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!profileBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
    
    // Handle logout
    logoutBtn.addEventListener('click', async function() {
        try {
            await api.logout();
            localStorage.removeItem('token');
            showNotification('Logged out successfully!', 'success');
            
            // Refresh the page to show login buttons
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } catch (error) {
            console.error('Logout failed:', error);
            // Force logout anyway
            localStorage.removeItem('token');
            window.location.reload();
        }
    });
}