cd "E:\New folder (3)"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd webapp
streamlit run streamlit_app.py


best color 

modern dark


Background:     #0f172a   (Dark Navy)
Card / Panel:   #111827
Primary Text:   #e5e7eb   (Light Gray)
Secondary Text:#9ca3af
Primary Button:#38bdf8   (Sky Blue)
Accent:         #22c55e   (Green)
Error:          #ef4444   (Red)


clean light ui
Background:     #f9fafb
Card:           #ffffff
Primary Text:   #111827
Secondary Text:#6b7280
Primary Button:#2563eb   (Blue)
Accent:         #10b981   (Teal)


dark+purple
Background:     #020617
Card:           #0f172a
Primary Text:   #e5e7eb
Accent Purple:  #a855f7
Button Hover:   #9333ea
Highlight:      #22d3ee


soft green
Background:     #ecfdf5
Primary Text:   #064e3b
Button:         #10b981
Accent:         #22c55e

bold and creative
Background:     #0f172a
Primary Red:    #ef4444
Accent Yellow:  #facc15
Text:           #f8fafc

recommendation

BG:        #0f172a
Card:      #111827
Text:      #e5e7eb
Button:    #38bdf8
Accent:    #22c55e

import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import io
import numpy as np
import random

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Smart Image Compression & Enhancement",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# CSS – CLEAN LAYOUT WITHOUT BLANK SPACES
# ======================================================
st.markdown("""
<style>
    /* Sky Blue + Dark Blue Gradient Background */
    .stApp {
        background: linear-gradient(135deg, 
            #87CEEB 0%, 
            #5D8AA8 30%, 
            #003366 70%,
            #001F3F 100%) !important;
        background-attachment: fixed !important;
        min-height: 100vh !important;
        padding: 0 !important;
    }

    /* Main title - Clean & Professional */
    .main-title {
        width: 100vw !important;
        margin-left: -50vw !important;
        left: 50% !important;
        position: relative !important;
        text-align: center !important;
        background: rgba(0, 63, 127, 0.9) !important;
        color: white !important;
        padding: 25px 0 !important;
        margin-top: 0 !important;
        margin-bottom: 30px !important;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        border-bottom: 3px solid #87CEEB !important;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3) !important;
        font-family: 'Arial', sans-serif !important;
    }

    /* Main container */
    .main-container {
        width: 95% !important;
        max-width: 1400px !important;
        margin: 0 auto 40px auto !important;
        padding: 20px !important;
        text-align: center !important;
    }

    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        padding: 35px !important;
        margin: 30px auto !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(135, 206, 235, 0.3) !important;
        max-width: 900px !important;
    }

    /* Section heading */
    .section-heading {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-bottom: 30px !important;
        color: #FFFFFF !important;
        text-align: center !important;
        padding-bottom: 15px !important;
        border-bottom: 2px solid rgba(135, 206, 235, 0.7) !important;
        display: inline-block !important;
        letter-spacing: 1px !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }

    /* UPLOAD BOX - First Box */
    .upload-box {
        background: rgba(0, 40, 85, 0.7) !important;
        border-radius: 15px !important;
        padding: 40px 30px !important;
        margin: 25px 0 !important;
        border: 3px solid rgba(135, 206, 235, 0.5) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
        text-align: center !important;
    }
    
    .upload-title {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #87CEEB !important;
        margin-bottom: 25px !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }

    /* Upload area styling */
    .upload-area {
        border: 3px dashed rgba(135, 206, 235, 0.5) !important;
        border-radius: 15px !important;
        padding: 50px 20px !important;
        text-align: center !important;
        background: rgba(0, 0, 0, 0.2) !important;
        margin: 20px 0 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .upload-area:hover {
        border-color: #87CEEB !important;
        background: rgba(135, 206, 235, 0.1) !important;
        box-shadow: 0 0 30px rgba(135, 206, 235, 0.2) !important;
    }
    
    .upload-text {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        margin-bottom: 10px !important;
        font-weight: 500 !important;
    }
    
    .upload-subtext {
        color: #D0E7FF !important;
        font-size: 0.9rem !important;
        margin-bottom: 20px !important;
    }

    /* White browse files button */
    .browse-button {
        background: linear-gradient(135deg, #FFFFFF, #F0F8FF) !important;
        color: #003366 !important;
        padding: 12px 30px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border: none !important;
        cursor: pointer !important;
        display: inline-block !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.3) !important;
        text-decoration: none !important;
    }
    
    .browse-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.4) !important;
        background: linear-gradient(135deg, #F0F8FF, #FFFFFF) !important;
    }

    /* CONTROL BOX - Second Box */
    .control-box {
        background: rgba(0, 40, 85, 0.7) !important;
        border-radius: 15px !important;
        padding: 35px !important;
        margin: 25px 0 !important;
        border: 3px solid rgba(135, 206, 235, 0.5) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
    }
    
    .control-title {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #87CEEB !important;
        margin-bottom: 30px !important;
        text-align: center !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        padding: 10px !important;
        background: rgba(135, 206, 235, 0.1) !important;
        border-radius: 10px !important;
        border: 2px solid rgba(135, 206, 235, 0.3) !important;
    }

    /* Control grid - Two columns */
    .control-grid {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 25px !important;
        margin: 20px 0 !important;
    }
    
    @media (max-width: 768px) {
        .control-grid {
            grid-template-columns: 1fr !important;
        }
    }

    .control-column {
        background: rgba(0, 63, 127, 0.4) !important;
        padding: 25px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(135, 206, 235, 0.2) !important;
    }
    
    .control-label {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #87CEEB !important;
        margin-bottom: 20px !important;
        display: block !important;
        text-align: center !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
        padding-bottom: 10px !important;
        border-bottom: 2px solid rgba(135, 206, 235, 0.3) !important;
    }

    /* Slider styling inside control box */
    .control-slider {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin-top: 15px !important;
    }
    
    .control-slider label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        margin-bottom: 10px !important;
        display: block !important;
    }

    /* Images container - 40% of screen */
    .images-container {
        display: flex !important;
        justify-content: center !important;
        gap: 30px !important;
        flex-wrap: wrap !important;
        margin: 40px 0 !important;
    }
    
    .image-card {
        flex: 1 !important;
        min-width: 300px !important;
        max-width: 40vw !important;
        min-height: 40vh !important;
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin: 10px !important;
        border: 2px solid rgba(135, 206, 235, 0.3) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: space-between !important;
    }
    
    .image-title {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin-bottom: 15px !important;
        padding-bottom: 8px !important;
        border-bottom: 2px solid rgba(135, 206, 235, 0.5) !important;
        width: 100% !important;
        text-align: center !important;
    }
    
    .image-display {
        width: 100% !important;
        height: 40vh !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        overflow: hidden !important;
        border-radius: 10px !important;
        background: rgba(0, 0, 0, 0.2) !important;
        padding: 10px !important;
    }
    
    .image-display img {
        max-width: 100% !important;
        max-height: 100% !important;
        width: auto !important;
        height: auto !important;
        object-fit: contain !important;
        border-radius: 8px !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
    }

    /* Button styling */
    .action-button {
        background: linear-gradient(135deg, #FF6B6B, #EE5A24) !important;
        color: white !important;
        border: none !important;
        padding: 18px 45px !important;
        border-radius: 12px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        display: block !important;
        margin: 40px auto 20px auto !important;
        width: 300px !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3) !important;
        letter-spacing: 0.5px !important;
    }
    
    .action-button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(255, 107, 107, 0.5) !important;
        background: linear-gradient(135deg, #EE5A24, #FF6B6B) !important;
    }

    /* Advanced options expander */
    .advanced-expander {
        margin-top: 25px !important;
        background: rgba(0, 63, 127, 0.4) !important;
        border-radius: 10px !important;
        padding: 20px !important;
        border: 1px solid rgba(135, 206, 235, 0.3) !important;
    }
    
    .advanced-title {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #87CEEB !important;
        margin-bottom: 15px !important;
        text-align: center !important;
        text-transform: uppercase !important;
    }

    /* File info display */
    .file-info {
        background: rgba(0, 63, 127, 0.4) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin: 20px auto !important;
        max-width: 400px !important;
        border: 1px solid rgba(135, 206, 235, 0.3) !important;
        color: #D0E7FF !important;
        font-size: 0.95rem !important;
    }

    /* Hide Streamlit elements */
    header, [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px !important;
        background: rgba(0, 0, 0, 0.2) !important;
    }

    ::-webkit-scrollbar-track {
        background: rgba(0, 40, 85, 0.3) !important;
        border-radius: 5px !important;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #87CEEB, #1E90FF) !important;
        border-radius: 5px !important;
        border: 2px solid rgba(0, 40, 85, 0.3) !important;
    }

    /* Remove blank spaces */
    .stSpinner, .stAlert {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .st-emotion-cache-1kyxreq {
        gap: 0 !important;
        margin: 0 !important;
    }
    
    /* Fix for Streamlit file uploader */
    div[data-testid="stFileUploader"] {
        border: none !important;
        background: transparent !important;
    }
    
    /* Remove dot dot dots */
    .st-emotion-cache-1dp5vir {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION STATE INITIALIZATION
# ======================================================
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'images' not in st.session_state:
    st.session_state.images = {}
if 'compression_data' not in st.session_state:
    st.session_state.compression_data = {}

# ======================================================
# HELPER FUNCTIONS
# ======================================================
def add_noise(image, noise_level):
    """Add noise to image"""
    if noise_level == 0:
        return image
    
    img_array = np.array(image)
    noise = np.random.randn(*img_array.shape) * noise_level
    noisy_array = img_array + noise
    noisy_array = np.clip(noisy_array, 0, 255).astype(np.uint8)
    
    return Image.fromarray(noisy_array)

def process_image(image, blur_radius, noise_level, jpeg_quality, compression_level):
    """Process image with all enhancements"""
    enhanced = image.copy()
    
    # Apply blur
    if blur_radius > 0:
        enhanced = enhanced.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    # Add noise
    if noise_level > 0:
        enhanced = add_noise(enhanced, noise_level)
    
    # Apply compression
    img_bytes = io.BytesIO()
    quality_factor = max(5, jpeg_quality - (compression_level * 3))
    
    enhanced.save(img_bytes, 
                  format="JPEG", 
                  quality=quality_factor, 
                  optimize=True,
                  progressive=True)
    
    img_bytes.seek(0)
    compressed_img = Image.open(img_bytes)
    
    return enhanced, compressed_img, quality_factor

# ======================================================
# MAIN TITLE
# ======================================================
st.markdown(
    '<div class="main-title">🎯 SMART IMAGE COMPRESSION & ENHANCEMENT</div>',
    unsafe_allow_html=True
)

# ======================================================
# MAIN CONTAINER
# ======================================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ======================================================
# STEP 1: UPLOAD SECTION - FIRST BOX
# ======================================================
if st.session_state.current_step == 1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # UPLOAD BOX - First Box
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    
    # Upload title
    st.markdown('<div class="upload-title">📤 UPLOAD YOUR IMAGE</div>', unsafe_allow_html=True)
    
    # Upload area with text
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-text">Drag and drop file here</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-subtext">Limit 200MB per file: PNG, JPG, JPEG, BMP, TIFF, WEBP</div>', unsafe_allow_html=True)
    
    # White browse files button
    st.markdown(
        '<div class="browse-button" onclick="document.getElementById(\'file-upload\').click()">📁 Browse files</div>',
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close upload-area
    
    # Hidden file uploader
    uploaded_file = st.file_uploader(
        "",
        type=["png", "jpg", "jpeg", "bmp", "tiff", "webp"],
        key="file_uploader",
        label_visibility="collapsed",
        accept_multiple_files=False
    )
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close upload-box
    
    # Handle file upload
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.current_step = 2
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close glass-card

# ======================================================
# STEP 2: CONTROLS SECTION - SECOND BOX
# ======================================================
elif st.session_state.current_step == 2 and st.session_state.uploaded_file:
    uploaded_file = st.session_state.uploaded_file
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # File info
    file_size = uploaded_file.getbuffer().nbytes
    file_size_mb = file_size / (1024 * 1024)
    
    st.markdown(f'''
    <div class="file-info">
        <div style="display: flex; justify-content: center; align-items: center; gap: 15px; margin-bottom: 10px;">
            <span style="font-size: 1.2rem;">📄</span>
            <span style="font-weight: 600; color: #87CEEB;">{uploaded_file.name}</span>
        </div>
        <div style="display: flex; justify-content: space-around; margin-top: 10px;">
            <div>💾 <strong>{file_size_mb:.2f} MB</strong></div>
            <div>📁 <strong>{uploaded_file.type.split('/')[1].upper()}</strong></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 CHANGE IMAGE", key="change_image", use_container_width=True):
            st.session_state.current_step = 1
            st.session_state.uploaded_file = None
            st.rerun()
    
    # CONTROL BOX - Second Box
    st.markdown('<div class="control-box">', unsafe_allow_html=True)
    
    # Control box title
    st.markdown('<div class="control-title">ADJUST PROCESSING PARAMETERS</div>', unsafe_allow_html=True)
    
    # Control grid - Two columns
    st.markdown('<div class="control-grid">', unsafe_allow_html=True)
    
    # COLUMN 1: BLUR RADIUS and NOISE LEVEL
    st.markdown('<div class="control-column">', unsafe_allow_html=True)
    
    # BLUR RADIUS
    st.markdown('<div class="control-label">🔵 BLUR RADIUS</div>', unsafe_allow_html=True)
    st.markdown('<div class="control-slider">', unsafe_allow_html=True)
    blur_radius = st.slider(
        "Adjust blur intensity",
        0, 10, 0,
        help="Apply Gaussian blur effect (0 = no blur)",
        key="blur_slider",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # NOISE LEVEL
    st.markdown('<div class="control-label" style="margin-top: 25px;">🌀 NOISE LEVEL</div>', unsafe_allow_html=True)
    st.markdown('<div class="control-slider">', unsafe_allow_html=True)
    noise_level = st.slider(
        "Adjust noise intensity",
        0, 50, 0,
        help="Add noise effect (0 = no noise)",
        key="noise_slider",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close column 1
    
    # COLUMN 2: JPEG QUALITY and COMPRESSION LEVEL
    st.markdown('<div class="control-column">', unsafe_allow_html=True)
    
    # JPEG QUALITY
    st.markdown('<div class="control-label">🎨 JPEG QUALITY</div>', unsafe_allow_html=True)
    st.markdown('<div class="control-slider">', unsafe_allow_html=True)
    jpeg_quality = st.slider(
        "Adjust JPEG quality",
        1, 100, 85,
        help="1 = maximum compression, 100 = best quality",
        key="quality_slider",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # COMPRESSION LEVEL
    st.markdown('<div class="control-label" style="margin-top: 25px;">📉 COMPRESSION LEVEL</div>', unsafe_allow_html=True)
    st.markdown('<div class="control-slider">', unsafe_allow_html=True)
    compression_level = st.slider(
        "Adjust compression intensity",
        1, 10, 5,
        help="Overall compression intensity",
        key="compression_slider",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close column 2
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close control-grid
    
    # ADVANCED OPTIONS expander
    st.markdown('<div class="advanced-expander">', unsafe_allow_html=True)
    
    st.markdown('<div class="advanced-title">🔧 ADVANCED OPTIONS</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        optimize = st.checkbox("Optimize Compression", value=True, key="optimize_check")
        progressive = st.checkbox("Progressive JPEG", value=True, key="progressive_check")
    with col2:
        color_space = st.selectbox("Color Space", 
                                  ["RGB", "YCbCr"], key="color_select")
        dct_method = st.selectbox("DCT Method", 
                                 ["Integer (Fast)", "Float (Accurate)"], key="dct_select")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close advanced-expander
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close control-box
    
    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 START PROCESSING", key="process_btn", use_container_width=True):
            with st.spinner("🔄 Processing your image..."):
                try:
                    image = Image.open(uploaded_file)
                    
                    # Store original image
                    st.session_state.images['original'] = image
                    
                    # Process image
                    enhanced_img, compressed_img, actual_quality = process_image(
                        image, blur_radius, noise_level, jpeg_quality, compression_level
                    )
                    
                    # Store processed images
                    st.session_state.images['enhanced'] = enhanced_img
                    st.session_state.images['compressed'] = compressed_img
                    
                    # Calculate compression data
                    original_size = file_size
                    
                    compressed_bytes = io.BytesIO()
                    compressed_img.save(compressed_bytes, format="JPEG", quality=actual_quality)
                    compressed_size = len(compressed_bytes.getvalue())
                    
                    compression_ratio = ((original_size - compressed_size) / original_size) * 100
                    
                    st.session_state.compression_data = {
                        'original_size': original_size,
                        'compressed_size': compressed_size,
                        'compression_ratio': compression_ratio,
                        'space_saved': original_size - compressed_size,
                        'blur_radius': blur_radius,
                        'noise_level': noise_level,
                        'jpeg_quality': jpeg_quality,
                        'compression_level': compression_level,
                        'actual_quality': actual_quality,
                        'original_dimensions': f"{image.size[0]}x{image.size[1]}",
                        'compressed_dimensions': f"{compressed_img.size[0]}x{compressed_img.size[1]}"
                    }
                    
                    st.session_state.processed = True
                    st.session_state.current_step = 3
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close glass-card

# ======================================================
# STEP 3: RESULTS & IMAGES DISPLAY
# ======================================================
elif st.session_state.current_step == 3 and st.session_state.processed:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📊 PROCESSING RESULTS</div>', unsafe_allow_html=True)
    
    data = st.session_state.compression_data
    
    # Success message
    st.markdown(
        f'''
        <div style="background: rgba(46, 204, 113, 0.15); padding: 15px 25px; border-radius: 10px; margin: 20px auto; max-width: 500px; border: 2px solid rgba(46, 204, 113, 0.3); text-align: center;">
            <div style="font-size: 1.3rem; margin-bottom: 5px; color: #2ecc71; font-weight: 600;">✅ PROCESSING COMPLETE!</div>
            <div style="color: #D0E7FF;">Image compressed by <strong style="color: #87CEEB;">{data["compression_ratio"]:.1f}%</strong></div>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    # THREE IMAGES AT 40% SCREEN
    st.markdown('<div class="images-container">', unsafe_allow_html=True)
    
    # Original Image
    st.markdown('<div class="image-card">', unsafe_allow_html=True)
    st.markdown('<div class="image-title">📸 ORIGINAL IMAGE</div>', unsafe_allow_html=True)
    st.markdown('<div class="image-display">', unsafe_allow_html=True)
    st.image(st.session_state.images['original'], use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'''
    <div style="color: #D0E7FF; font-size: 0.9rem; margin-top: 10px; text-align: center;">
        <div>📐 {data["original_dimensions"]}</div>
        <div>💾 {data["original_size"] / (1024*1024):.2f} MB</div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close image-card
    
    # Enhanced Image
    st.markdown('<div class="image-card">', unsafe_allow_html=True)
    st.markdown('<div class="image-title">✨ ENHANCED IMAGE</div>', unsafe_allow_html=True)
    st.markdown('<div class="image-display">', unsafe_allow_html=True)
    st.image(st.session_state.images['enhanced'], use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'''
    <div style="color: #D0E7FF; font-size: 0.9rem; margin-top: 10px; text-align: center;">
        <div>🔵 Blur: {data["blur_radius"]}/10</div>
        <div>🌀 Noise: {data["noise_level"]}/50</div>
        <div>🎨 Quality: {data["jpeg_quality"]}/100</div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close image-card
    
    # Compressed Image
    st.markdown('<div class="image-card">', unsafe_allow_html=True)
    st.markdown('<div class="image-title">📦 COMPRESSED IMAGE</div>', unsafe_allow_html=True)
    st.markdown('<div class="image-display">', unsafe_allow_html=True)
    st.image(st.session_state.images['compressed'], use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'''
    <div style="color: #D0E7FF; font-size: 0.9rem; margin-top: 10px; text-align: center;">
        <div>📐 {data["compressed_dimensions"]}</div>
        <div>💾 {data["compressed_size"] / 1024:.1f} KB</div>
        <div>⚡ Actual Quality: {data["actual_quality"]}/100</div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close image-card
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close images-container
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        compressed_bytes = io.BytesIO()
        st.session_state.images['compressed'].save(compressed_bytes, format="JPEG", quality=data['actual_quality'])
        
        st.download_button(
            label="📥 DOWNLOAD",
            data=compressed_bytes.getvalue(),
            file_name=f"compressed_{st.session_state.uploaded_file.name.split('.')[0]}.jpg",
            mime="image/jpeg",
            key="download_btn",
            use_container_width=True
        )
    
    with col2:
        if st.button("⚙️ ADJUST SETTINGS", key="adjust_settings", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()
    
    with col3:
        if st.button("🔄 NEW IMAGE", key="new_image", use_container_width=True):
            for key in ['current_step', 'uploaded_file', 'processed', 'images', 'compression_data']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_step = 1
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close glass-card

st.markdown('</div>', unsafe_allow_html=True)  # Close main-container

# ======================================================
# FOOTER
# ======================================================
st.markdown(
    """
    <div style="text-align: center; color: rgba(135, 206, 235, 0.7); padding: 40px; margin-top: 30px;">
        <hr style="border-color: rgba(135, 206, 235, 0.3); margin: 30px auto; width: 50%;">
        <p style="font-size: 0.9rem; letter-spacing: 0.5px; font-weight: 400;">
            Smart Image Compression Tool • Professional Processing • Secure & Local
        </p>
        <p style="font-size: 0.8rem; margin-top: 10px; color: rgba(135, 206, 235, 0.5);">
            All image processing occurs locally in your browser. No data leaves your device.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)