import streamlit as st
from google import genai

# 1. ตั้งค่าหน้าตาของเว็บ (Brand Identity)
st.set_page_config(page_title="Chomsuk.ai - VIP Access", page_icon="🔐")

# --- Custom CSS สำหรับธีม น้ำเงินเข้ม-ทอง ---
st.markdown("""
    <style>
    .main { background-color: #001f3f; color: white; }
    .stButton>button { 
        background-color: #FFD700; 
        color: #001f3f; 
        font-weight: bold; 
        border-radius: 10px; 
        width: 100%;
        height: 3.5em;
        font-size: 1.2em;
    }
    h1, h2, h3 { color: #FFD700; text-align: center; }
    .stTextInput>div>div>input { background-color: #f0f2f6; color: black; text-align: center; }
    .stTextArea>div>div>textarea { background-color: #f0f2f6; color: black; }
    /* ปรับแต่งหน้า Login ให้ดูพรีเมียม */
    .login-container { text-align: center; padding: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ระบบรหัสผ่าน VIP
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        # *** อาจารย์สามารถเปลี่ยนรหัสผ่านตรงนี้ได้ครับ ***
        if st.session_state["password"] == "chomsuk2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # ลบรหัสจาก session เพื่อความปลอดภัย
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # ส่วนแสดงหน้าจอประตู VIP
        st.markdown("<h1>🔒 ประตูสู่<br>Chomsuk.ai</h1>", unsafe_allow_html=True)
        st.write("<p style='text-align: center;'>กรุณาใส่รหัสผ่าน VIP เพื่อเข้าใช้งานระบบ</p>", unsafe_allow_html=True)
        st.text_input("รหัสผ่าน (Password):", type="password", on_change=password_entered, key="password")
        
        if "password_correct" in st.session_state:
            st.error("😕 รหัสผ่านไม่ถูกต้องครับอาจารย์ต้น ลองใหม่อีกครั้งนะ")
        return False
    elif not st.session_state["password_correct"]:
        # กรณีใส่ผิดซ้ำ
        st.markdown("<h1>🔒 ประตูสู่<br>Chomsuk.ai</h1>", unsafe_allow_html=True)
        st.text_input("รหัสผ่าน (Password):", type="password", on_change=password_entered, key="password")
        st.error("😕 รหัสผ่านไม่ถูกต้องครับอาจารย์ต้น")
        return False
    else:
        return True

# 3. ตรวจสอบรหัสผ่านก่อนเข้าแอป
if check_password():
    
    # --- เริ่มส่วนเนื้อหาแอปหลัก ---
    
    # เชื่อมต่อ Gemini API ผ่าน Secrets ของ Streamlit
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=API_KEY)
    except:
        st.error("❌ ไม่พบ API Key ในระบบ Secrets กรุณาตั้งค่าใน Streamlit Cloud")
        st.stop()

    st.title("🏆 Chomsuk.ai")
    st.subheader("ระบบเสกคอนเทนต์ทำเงินอัตโนมัติ")
    st.write("---")

    # ส่วนรับข้อมูล
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("📦 ชื่อสินค้าหรือบริการ:", placeholder="เช่น รับซ่อมมือถือ Chomsuk")
    with col2:
        style = st.selectbox("🎭 สไตล์ของคอนเทนต์:", ["น่าเชื่อถือ/พรีเมียม", "ฮาๆ/เข้าถึงง่าย", "รีวิวบ้านๆ/จริงใจ"])

    features = st.text_area("✨ จุดเด่นที่อยากให้คนจำได้:", placeholder="เช่น ช่างต้นซ่อมเอง อะไหล่แท้ ไม่ย้อมแมว ประสบการณ์กว่า 20 ปี")

    # ปุ่มรันระบบ
    if st.button("🚀 เริ่มการทำงานของ Chomsuk.ai"):
        if product_name and features:
            with st.spinner('สมองกล Chomsuk กำลังคราฟต์สคริปต์ที่ดีที่สุดให้คุณ...'):
                try:
                    prompt = f"""
                    คุณคือ Copywriter มืออาชีพที่เก่งที่สุดในไทย เขียนสคริปต์วิดีโอสั้น 30 วินาที 
                    สำหรับแบรนด์ "Chomsuk" (ชมสุข)
                    สินค้า: {product_name} 
                    จุดเด่น: {features}
                    สไตล์: {style}
                    
                    ผลลัพธ์ต้องมี:
                    1. Hook (0-3 วิ): คำพูดหยุดนิ้ว
                    2. Body (3-25 วิ): เนื้อหาโน้มน้าวใจ
                    3. Call to Action (25-30 วิ): ปิดการขาย
                    4. Image Prompt: ภาษาอังกฤษ 1 ย่อหน้า สำหรับเจนภาพประกอบที่ดูรวยและพรีเมียม
                    """
                    
                    response = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=prompt
                    )
                    
                    st.success("✨ สคริปต์ระดับพรีเมียมของคุณเสร็จแล้ว!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.balloons() 
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณากรอกข้อมูลให้ครบก่อนนะครับอาจารย์")

    st.write("---")
    st.caption("© 2026 Chomsuk.ai - Trusted Tech by Kru Ton Thani Chomsuk")

# --- จบบทเรียนความสำเร็จ ---