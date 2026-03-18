import streamlit as st
from google import genai

# --- 1. ตั้งค่าหน้าเว็บและดีไซน์ ---
st.set_page_config(page_title="Chomsuk.ai - All-in-One AI", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #001f3f; }
    /* ปรับแต่ง Sidebar ให้ดูแพง */
    [data-testid="stSidebar"] { background-color: #001529; border-right: 2px solid #FFD700; }
    .stButton>button { background-color: #FFD700; color: #001f3f; font-weight: bold; border-radius: 10px; width: 100%; }
    h1, h2 { color: #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ระบบ Login (กุญแจเดิมของอาจารย์) ---
if "password_correct" not in st.session_state:
    st.title("🔒 Chomsuk.ai VIP")
    password = st.text_input("กรุณาใส่รหัสผ่าน VIP:", type="password")
    if st.button("เข้าสู่ระบบ"):
        if password == "chomsuk2026":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("รหัสผ่านไม่ถูกต้อง")
    st.stop()

# --- 3. เมื่อ Login ผ่านแล้ว จะเจอเมนูด้านข้าง ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.title("เมนู Chomsuk.ai")
    menu = st.radio("เลือกฟีเจอร์ที่ต้องการ:", 
                    ["💡 หาไอเดีย/หัวข้อ", "✍️ เสกคอนเทนต์", "🎨 สตูดิโอเจนภาพ", "💳 สมัคร VIP"])
    st.write("---")
    st.caption("User: Kru Ton (Admin)")

# --- 4. ลอจิกการเปลี่ยนหน้าตามเมนู ---

# เชื่อมต่อ API (ก๊อปปี้คีย์จาก Secrets)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if menu == "💡 หาไอเดีย/หัวข้อ":
    st.header("💡 หาไอเดียทำคอนเทนต์เงินล้าน")
    topic = st.text_input("คุณอยากทำเรื่องอะไร?", placeholder="เช่น การซ่อมมือถือ, การลงทุน")
    if st.button("ปั้นไอเดีย!"):
        with st.spinner("กำลังคิดไอเดียให้คุณ..."):
            prompt = f"ช่วยคิด 5 หัวข้อคอนเทนต์ที่น่าสนใจและมีโอกาสเป็นไวรัลเกี่ยวกับเรื่อง: {topic}"
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.write(response.text)

elif menu == "✍️ เสกคอนเทนต์":
    st.header("✍️ ระบบเสกคอนเทนต์ทำเงิน (Master Engine)")
    # (อาจารย์ก๊อปปี้โค้ดรับ Input เดิมจากตัวเก่ามาใส่ตรงนี้ได้เลยครับ)
    product = st.text_input("ชื่อสินค้า:")
    if st.button("เสกคอนเทนต์!"):
        st.success(f"เสกคอนเทนต์สำหรับ {product} เรียบร้อย!")

elif menu == "🎨 สตูดิโอเจนภาพ":
    st.header("🎨 AI Image Prompt Studio")
    desc = st.text_area("บรรยายภาพที่อยากได้ (ภาษาไทย):")
    if st.button("แปลงเป็น Prompt อังกฤษ"):
        prompt = f"Translate and enhance this image description into a high-quality AI image prompt: {desc}"
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        st.code(response.text)

elif menu == "💳 สมัคร VIP":
    st.header("💳 ยกระดับสู่ Chomsuk AI พรีเมียม")
    st.write("เลือกแผนที่ใช่สำหรับคุณ:")
    col1, col2 = st.columns(2)
    with col1:
        st.info("💰 **รายเดือน (Pro)**\n\n499 บาท / เดือน\n- เจนคอนเทนต์ไม่จำกัด\n- เข้าถึงคลังพรอมต์ลับ")
    with col2:
        st.success("🔥 **รายปี (Elite)**\n\n5,990 บาท / ปี\n- ทุกอย่างใน Pro\n- ปรึกษา Kru Ton ส่วนตัว")

st.sidebar.write("---")
st.sidebar.caption("© 2026 Chomsuk.ai")