import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

def generate_pdf(original, corrupted, enhanced, psnr, ssim, jpeg_kb):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W/2, H-50, "Smart Image Compression & Enhancement Report")

    # Images
    img_w, img_h = 150, 110
    y = H - 180

    c.drawImage(ImageReader(original), 40, y, img_w, img_h)
    c.drawImage(ImageReader(corrupted), 220, y, img_w, img_h)
    c.drawImage(ImageReader(enhanced), 400, y, img_w, img_h)

    # Labels
    c.setFont("Helvetica", 10)
    c.drawCentredString(115, y-15, "Original")
    c.drawCentredString(295, y-15, "Corrupted")
    c.drawCentredString(475, y-15, "Enhanced")

    # Metrics
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y-50, "Metrics")
    c.setFont("Helvetica", 11)
    c.drawString(40, y-70, f"PSNR: {psnr:.2f} dB")
    c.drawString(40, y-90, f"SSIM: {ssim:.4f}")
    c.drawString(40, y-110, f"JPEG Size: {jpeg_kb:.2f} KB")

    c.showPage()
    c.save()
    buf.seek(0)
    return buf
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Smart Image Compression & Enhancement",
    layout="wide"
)

# ===============================
# GLOBAL CSS
# ===============================
st.markdown("""
<style>

/* FORCE FULL BACKGROUND */
html, body, [class*="css"] {
    background-color: #a855f7;
}
.stApp {
    background-color: #ecfdf5 !important;
    color: #064e3b !important;
}
/* MAIN APP */
.stApp {
    background-color: #ecfdf5 !important;
    color: #064e3b !important;
}

/* REMOVE DEFAULT STREAMLIT WHITE BOX */
section.main > div {
    background-color: transparent !important;
}

/* HEADER */
.header {
    text-align: center;
    margin-bottom: 30px;
}
.header h1 {
    font-size: 38px;
    font-weight: 800;
    color: #064e3b;
}
.header p {
    color: #047857;
}

/* CENTER CONTROL CARD */
.center-box {
    max-width: 700px;
    margin: auto;
    background: #ffffff;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 20px 40px rgba(16,185,129,0.15);
}

/* RESULT BOX */
.result-box {
    max-width: 900px;
    margin: 40px auto;
    background: #ffffff;
    border-radius: 20px;
    padding: 26px;
    box-shadow: 0 25px 50px rgba(16,185,129,0.18);
}

/* BUTTON */
.stButton > button {
    width: 100%;
    padding: 14px;
    border-radius: 14px;
    background: linear-gradient(90deg, #10b981, #22c55e);
    color: white;
    font-weight: bold;
    border: none;
}
/* FIX SLIDER LABEL VISIBILITY */
label, .stSlider label, .stMarkdown, p {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* FIX SLIDER VALUE TEXT */
.css-1cpxqw2, .css-1v0mbdj {
    color: #000000 !important;
}

/* FORCE ALL TEXT DARK */
* {
    color: #064e3b;
}

</style>
""", unsafe_allow_html=True)

# ===============================
# HEADER (FULL WIDTH)
# ===============================
st.markdown("""
<div class="card">
<h1>Smart Image Compression & Enhancement</h1>
<p style="text-align:center;color:#94a3b8">
Upload → Corrupt → Enhance → Analyze → Download
</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# UPLOAD & CONTROLS
# ======================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📤 Upload & Controls")

uploaded = st.file_uploader(
    "Upload Image",
    type=["png","jpg","jpeg"],
    key="upload"
)

noise = st.slider("Noise Level", 0, 50, 0)
blur = st.slider("Blur Radius", 0, 10, 0)
quality = st.slider("JPEG Quality", 10, 95, 80)

run = st.button("⚡ Apply + Enhance")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded is None:
    st.stop()

original = Image.open(uploaded).convert("RGB")

if not run:
    st.image(original, caption="Uploaded Image", width=360)
    st.stop()

# ======================================================
# IMAGE PROCESSING
# ======================================================
corrupted = original.copy()

if noise > 0:
    arr = np.array(corrupted).astype(np.float32)
    arr += np.random.normal(0, noise, arr.shape)
    corrupted = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))

if blur > 0:
    corrupted = corrupted.filter(ImageFilter.GaussianBlur(blur))

enhanced = corrupted.filter(ImageFilter.SHARPEN)

# ======================================================
# METRICS (DEFINE ONCE – FIX)
# ======================================================
orig_np = np.array(original)
enh_np  = np.array(enhanced)

psnr = peak_signal_noise_ratio(orig_np, enh_np, data_range=255)
ssim = structural_similarity(orig_np, enh_np, channel_axis=2, data_range=255)

jpeg_buf = io.BytesIO()
original.save(jpeg_buf, format="JPEG", quality=quality)
jpeg_kb = len(jpeg_buf.getvalue()) / 1024

# ======================================================
# IMAGE PREVIEW
# ======================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🖼 Image Preview")

c1,c2,c3 = st.columns(3)
with c1:
    st.image(original, caption="Original", width=240)
with c2:
    st.image(corrupted, caption="Corrupted", width=240)
with c3:
    st.image(enhanced, caption="Enhanced", width=240)

st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# METRICS DISPLAY
# ======================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Metrics")
st.write(f"**PSNR:** {psnr:.2f} dB")
st.write(f"**SSIM:** {ssim:.4f}")
st.write(f"**JPEG Size:** {jpeg_kb:.2f} KB")
st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# INTERACTIVE COMPARISON
# ======================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔍 Interactive Comparison")

mode = st.radio(
    "Compare",
    ["Original ↔ Enhanced", "Corrupted ↔ Enhanced"],
    horizontal=True
)

a = original if "Original" in mode else corrupted
b = enhanced

c1,c2 = st.columns(2)
with c1:
    st.image(a, width=300)
with c2:
    st.image(b, width=300)

st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# PDF REPORT (SAFE)
# ======================================================
def generate_pdf():
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W,H = A4

    c.setFont("Helvetica-Bold",18)
    c.drawCentredString(W/2, H-50,
        "Smart Image Compression & Enhancement Report")

    y = H-140
    img_w,img_h = 140,100

    c.drawImage(ImageReader(original), 40, y, img_w, img_h)
    c.drawImage(ImageReader(corrupted), 220, y, img_w, img_h)
    c.drawImage(ImageReader(enhanced), 400, y, img_w, img_h)

    c.setFont("Helvetica",11)
    c.drawString(40, y-40, f"PSNR : {psnr:.2f} dB")
    c.drawString(40, y-60, f"SSIM : {ssim:.4f}")
    c.drawString(40, y-80, f"JPEG Size : {jpeg_kb:.2f} KB")

    c.showPage()
    c.save()
    buf.seek(0)
    return buf

# ======================================================
# DOWNLOAD
# ======================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("⬇ Download")

st.download_button(
    " Download PDF Report",
    data=generate_pdf(),
    file_name="smart_image_report.pdf",
    mime="application/pdf"
)

st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# FOOTER
# ======================================================
st.markdown("""
<p style="text-align:center;color:#94a3b8;font-size:13px;">

</p>
""", unsafe_allow_html=True)
