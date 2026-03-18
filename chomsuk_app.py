import streamlit as st
from google import genai

# 1. ตั้งค่าหน้าตาของเว็บ (Brand Identity)
st.set_page_config(page_title="Chomsuk.ai - VIP Access", page_icon="🔐")

# --- Custom CSS ใหม่ (เน้นความเป๊ะ ไม่ซ้อนกัน) ---
st.markdown("""
    <style>
    .main { background-color: #001f3f; color: white; }
    
    /* สไตล์ปุ่มสีเหลืองทอง */
    .stButton>button { 
        background-color: #FFD700 !important; 
        color: #001f3f !important; 
        font-weight: bold !important; 
        border-radius: 10px !important; 
        width: 100% !important;
        height: 3.5em !important;
        margin-top: 15px !important;
        border: none !important;
    }
    
    /* จัดการช่อง Input */
    .stTextInput>div>div>input { 
        background-color: #f0f2f6 !important; 
        color: black !important; 
        border-radius: 8px !important;
        height: 3em !important;
    }
    
    h1 { color: #FFD700; text-align: center; margin-bottom: 0px; }
    h2 { color: #FFD700; text-align: center; }
    p { text-align: center; font-size: 1.1em; }
    
    /* แก้ไขปัญหาระยะห่าง */
    .block-container { padding-top: 5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. ระบบรหัสผ่าน VIP พร้อมปุ่มกด
def check_password():
    if "password_correct" not in st.session_state:
        # แสดงหน้าจอ Login
        st.markdown("<h1>🔒 ประตูสู่</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom:20px;'>Chomsuk.ai</h1>", unsafe_allow_html=True)
        st.write("กรุณาใส่รหัสผ่าน VIP เพื่อเข้าใช้งานระบบ")
        
        # ช่องใส่รหัส
        password_input = st.text_input("รหัสผ่าน (Password):", type="password")
        
        # ปุ่มปลดล็อก (เพิ่มกลับมาให้แล้วครับ)
        if st.button("ปลดล็อก 🔑"):
            if password_input == "chomsuk2026":
                st.session_state["password_correct"] = True
                st.rerun() # รีเฟรชหน้าเพื่อเข้าสู่ระบบ
            else:
                st.error("😕 รหัสผ่านไม่ถูกต้องครับอาจารย์ต้น")
        
        return False
    return True

# 3. ตรวจสอบรหัสผ่านก่อนเข้าแอป
if check_password():
    # --- ส่วนเนื้อหาแอปหลัก (เริ่มทำงานเมื่อรหัสผ่านถูกต้อง) ---
    
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=API_KEY)
    except:
        st.error("❌ ไม่พบ API Key ในระบบ Secrets")
        st.stop()

    st.title("🏆 Chomsuk.ai")
    st.subheader("ระบบเสกคอนเทนต์ทำเงินอัตโนมัติ")
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("📦 ชื่อสินค้าหรือบริการ:", placeholder="เช่น รับซ่อมมือถือ Chomsuk")
    with col2:
        style = st.selectbox("🎭 สไตล์ของคอนเทนต์:", ["น่าเชื่อถือ/พรีเมียม", "ฮาๆ/เข้าถึงง่าย", "รีวิวบ้านๆ/จริงใจ"])

    features = st.text_area("✨ จุดเด่นที่อยากให้คนจำได้:", placeholder="เช่น ช่างต้นซ่อมเอง ประสบการณ์กว่า 20 ปี")

    if st.button("🚀 เริ่มการทำงานของ Chomsuk.ai"):
        if product_name and features:
            with st.spinner('สมองกล Chomsuk กำลังคราฟต์สคริปต์...'):
                try:
                    prompt = f"เขียนสคริปต์วิดีโอ 30 วินาที สำหรับแบรนด์ Chomsuk สินค้า: {product_name} จุดเด่น: {features} สไตล์: {style} พร้อม Image Prompt ภาษาอังกฤษ"
                    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                    
                    st.success("✨ สคริปต์ของคุณเสร็จแล้ว!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.balloons() 
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณากรอกข้อมูลให้ครบก่อนนะครับ")

    st.write("---")
    st.caption("© 2026 Chomsuk.ai - Trusted Tech by Kru Ton Thani Chomsuk")