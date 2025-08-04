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

// Review carousel variables
let reviewItems;
let progressFill;
let currentReviewIndex = 0;
let reviewInterval;

// Template scripts
const templates = {
    ad: "Introducing our revolutionary product! Transform your workflow with cutting-edge AI technology. Boost productivity by 300% and save hours every day. Don't miss out on this game-changing solution that's already trusted by thousands of professionals worldwide.",
    promo: "🎉 Special Offer Alert! 🎉 Get 50% off our premium AI avatar generator for a limited time only. Create professional talking videos in minutes, not hours. Perfect for marketing, education, and entertainment. Use code SPECIAL50 at checkout!",
    tutorial: "Welcome to our step-by-step tutorial! Today, I'll show you how to create stunning AI avatar videos. First, write your script in the text area. Then, choose your preferred avatar and voice settings. Finally, click generate and download your video in seconds!",
    presentation: "Good morning everyone! Today's presentation will cover our quarterly results and future roadmap. We've achieved remarkable growth with a 45% increase in revenue and expanded to three new markets. Let me walk you through the key highlights and our strategic initiatives for the upcoming quarter."
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Starting initialization...');
    
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
});

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
    console.log('Starting review carousel...');
    const transitionDuration = 3000; // 3 seconds per review
    
    function showNextReview() {
        console.log('Showing next review, current index:', currentReviewIndex);
        
        // Hide current review
        reviewItems[currentReviewIndex].classList.remove('active');
        
        // Move to next review
        currentReviewIndex = (currentReviewIndex + 1) % reviewItems.length;
        
        // Show new review
        reviewItems[currentReviewIndex].classList.add('active');
        
        // Update progress bar
        const progress = ((currentReviewIndex + 1) / reviewItems.length) * 100;
        progressFill.style.width = progress + '%';
        
        console.log('Switched to review index:', currentReviewIndex, 'at', new Date().toLocaleTimeString());
    }
    
    // Initialize progress bar
    progressFill.style.width = (100 / reviewItems.length) + '%';
    
    // Clear any existing interval
    if (reviewInterval) {
        clearInterval(reviewInterval);
    }
    
    // Set up interval for automatic transitions
    reviewInterval = setInterval(showNextReview, transitionDuration);
    
    // Log the interval setup
    console.log('Interval set for', transitionDuration, 'ms. Next change at:', new Date(Date.now() + transitionDuration).toLocaleTimeString());
    
    // Pause on hover
    const reviewsShowcase = document.querySelector('.reviews-showcase');
    if (reviewsShowcase) {
        reviewsShowcase.addEventListener('mouseenter', () => {
            console.log('Pausing review carousel');
            if (reviewInterval) {
                clearInterval(reviewInterval);
                reviewInterval = null;
            }
        });
        
        reviewsShowcase.addEventListener('mouseleave', () => {
            console.log('Resuming review carousel');
            if (!reviewInterval) {
                reviewInterval = setInterval(showNextReview, transitionDuration);
            }
        });
    }
    
    console.log('Review carousel started successfully - changing every 3 seconds');
    
    // Test the first transition after 3 seconds
    setTimeout(() => {
        console.log('First automatic transition should happen now');
    }, transitionDuration);
    
    // Add test function to global scope for debugging
    window.testReviewChange = function() {
        console.log('Manual test triggered');
        showNextReview();
    };
}

// Loader functionality
function initializeLoader() {
    if (loader) {
        // Hide loader after 1.5 seconds 
        setTimeout(() => {
            loader.classList.add('hidden');
            // Remove loader from DOM after animation completes
            setTimeout(() => {
                if (loader.parentNode) {
                    loader.remove();
                }
            }, 300);
        }, 2000); // Changed from 3000 to 1500 (1.5 seconds)
    }
}

// Smooth scrolling functionality
function initializeSmoothScrolling() {
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Only handle internal links (starting with #)
            if (href && href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    // Add smooth scroll animation
                    smoothScrollTo(targetElement);
                }
            }
        });
    });
}

// Smooth scroll to element with enhanced animation
function smoothScrollTo(element) {
    const headerHeight = document.querySelector('.header').offsetHeight;
    const bannerHeight = document.querySelector('.top-banner').offsetHeight;
    const totalOffset = headerHeight + bannerHeight;
    
    const elementPosition = element.offsetTop - totalOffset - 20; // 20px extra padding
    
    // Add scroll animation class to body
    document.body.style.scrollBehavior = 'smooth';
    
    // Scroll to element
    window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
    });
    
    // Add highlight effect to the target section
    element.classList.add('highlight-section');
    setTimeout(() => {
        element.classList.remove('highlight-section');
    }, 2000);
    
    // Reset scroll behavior after animation
    setTimeout(() => {
        document.body.style.scrollBehavior = 'auto';
    }, 1000);
}

// Event Listeners
function initializeEventListeners() {
    // Close banner
    closeBannerBtn?.addEventListener('click', () => {
        topBanner.style.display = 'none';
    });

    // Avatar selection
    avatarOptions.forEach(option => {
        option.addEventListener('click', () => {
            // Remove active class from all options
            avatarOptions.forEach(opt => opt.classList.remove('active'));
            // Add active class to clicked option
            option.classList.add('active');
        });
    });

    // Avatar upload
    uploadOption?.addEventListener('click', () => {
        avatarUpload.click();
    });

    avatarUpload?.addEventListener('change', handleAvatarUpload);

    // Template buttons
    templateBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const templateType = btn.textContent.toLowerCase().includes('ad') ? 'ad' :
                               btn.textContent.toLowerCase().includes('promo') ? 'promo' :
                               btn.textContent.toLowerCase().includes('tutorial') ? 'tutorial' :
                               btn.textContent.toLowerCase().includes('presentation') ? 'presentation' : 'ad';
            
            scriptInput.value = templates[templateType];
            scriptInput.focus();
            
            // Add visual feedback
            btn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                btn.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Generate video button
    generateBtn?.addEventListener('click', handleVideoGeneration);

    // Form validation
    scriptInput?.addEventListener('input', validateForm);
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

        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            showNotification('Image size should be less than 5MB.', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            // Create new avatar option
            const newAvatarOption = document.createElement('div');
            newAvatarOption.className = 'avatar-option active';
            newAvatarOption.innerHTML = `
                <img src="${e.target.result}" alt="Uploaded Avatar">
                <span>Your Photo</span>
            `;

            // Remove active class from other options
            avatarOptions.forEach(opt => opt.classList.remove('active'));

            // Insert new option before upload option
            uploadOption.parentNode.insertBefore(newAvatarOption, uploadOption);

            // Add click event to new option
            newAvatarOption.addEventListener('click', () => {
                avatarOptions.forEach(opt => opt.classList.remove('active'));
                newAvatarOption.classList.add('active');
            });

            showNotification('Avatar uploaded successfully!', 'success');
        };
        reader.readAsDataURL(file);
    }
}

// Handle video generation
function handleVideoGeneration() {
    const script = scriptInput.value.trim();
    
    if (!script) {
        showNotification('Please enter a script to generate the video.', 'error');
        return;
    }

    // Show loading state
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    generateBtn.classList.add('loading');

    // Simulate video generation (replace with actual API call)
    setTimeout(() => {
        // Hide loading state
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-bolt"></i> Generate Video';
        generateBtn.classList.remove('loading');

        // Show preview section
        showPreviewSection();

        // Scroll to preview
        previewSection.scrollIntoView({ behavior: 'smooth' });

        showNotification('Video generated successfully!', 'success');
    }, 3000);
}

// Show preview section
function showPreviewSection() {
    previewSection.style.display = 'block';
    previewSection.classList.add('fade-in');

    // Simulate video source (replace with actual video URL)
    const videoBlob = new Blob([''], { type: 'video/mp4' });
    const videoUrl = URL.createObjectURL(videoBlob);
    previewVideo.src = videoUrl;
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
                opacity: 0.8;
                transition: opacity 0.3s ease;
            }
            .notification-close:hover {
                opacity: 1;
            }
        `;
        document.head.appendChild(style);
    }

    // Add to page
    document.body.appendChild(notification);

    // Close button functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.remove();
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideInRight 0.3s ease-out reverse';
            setTimeout(() => notification.remove(), 300);
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

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.config-card, .step-card, .template-btn');
    animateElements.forEach(el => observer.observe(el));
}

// Utility functions
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

// Character counter for script input
function updateCharacterCount() {
    const script = scriptInput.value;
    const maxLength = 1000;
    const currentLength = script.length;
    
    // Create or update character counter
    let counter = document.querySelector('.character-counter');
    if (!counter) {
        counter = document.createElement('div');
        counter.className = 'character-counter';
        counter.style.cssText = `
            text-align: right;
            font-size: 12px;
            color: #6b7280;
            margin-top: 8px;
        `;
        scriptInput.parentNode.appendChild(counter);
    }
    
    counter.textContent = `${currentLength}/${maxLength} characters`;
    
    if (currentLength > maxLength) {
        counter.style.color = '#ef4444';
        scriptInput.style.borderColor = '#ef4444';
    } else {
        counter.style.color = '#6b7280';
        scriptInput.style.borderColor = currentLength > 0 ? '#8b5cf6' : '#e5e7eb';
    }
}

// Add character counter to script input
scriptInput?.addEventListener('input', debounce(updateCharacterCount, 100));

// Initialize character counter
updateCharacterCount();

// Export functions for potential use in other modules
window.VidFace = {
    generateVideo: handleVideoGeneration,
    showNotification: showNotification,
    templates: templates
};