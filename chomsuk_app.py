import streamlit as st
from google import genai

# 1. ตั้งค่าหน้าตาของเว็บ (Brand Identity)
st.set_page_config(page_title="Chomsuk.ai - เครื่องจักรผลิตเงิน", page_icon="💰")

# Custom CSS ตกแต่งสีสันให้ดูพรีเมียม
st.markdown("""
    <style>
    .main { background-color: #001f3f; color: white; }
    .stButton>button { background-color: #FFD700; color: #001f3f; font-weight: bold; border-radius: 10px; width: 100%; height: 3em; }
    h1, h2, h3 { color: #FFD700; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🔒 ระบบ Login 1 ชั้น (Master Password)
# ==========================================
MASTER_PASSWORD = "CHOMSUK-VIP"  # 👈 อาจารย์เปลี่ยนรหัสผ่านตรงนี้ได้เลยครับ

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("🔒 ประตูสู่ Chomsuk.ai")
    st.write("กรุณาใส่รหัสผ่าน VIP เพื่อเข้าใช้งานระบบ")
    
    pwd = st.text_input("รหัสผ่าน (Password):", type="password")
    if st.button("ปลดล็อก 🔑"):
        if pwd == MASTER_PASSWORD:
            st.session_state["logged_in"] = True
            st.rerun() # รีเฟรชหน้าเว็บเพื่อเข้าสู่ระบบ
        else:
            st.error("❌ รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่ครับ")
    st.stop() # หยุดโค้ดไว้แค่นี้ถ้ายังไม่ล็อกอิน
# ==========================================

# โค้ดส่วนหลักของ Chomsuk.ai (จะแสดงก็ต่อเมื่อล็อกอินผ่านแล้ว)
API_KEY = st.secrets["GEMINI_API_KEY"] 
client = genai.Client(api_key=API_KEY)

st.title("🏆 Chomsuk.ai")
st.subheader("ระบบเสกคอนเทนต์ทำเงินอัตโนมัติ")
st.write("---")

col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("📦 ชื่อสินค้าหรือบริการ:", placeholder="เช่น รับซ่อมมือถือ Chomsuk")
with col2:
    style = st.selectbox("🎭 สไตล์ของคอนเทนต์:", ["น่าเชื่อถือ/พรีเมียม", "ฮาๆ/เข้าถึงง่าย", "รีวิวบ้านๆ/จริงใจ"])

features = st.text_area("✨ จุดเด่นที่อยากให้คนจำได้:", placeholder="เช่น ช่างต้นซ่อมเอง อะไหล่แท้ ไม่ย้อมแมว ประสบการณ์กว่า 20 ปี")

if st.button("🚀 เริ่มการทำงานของ Chomsuk.ai"):
    if product_name and features:
        with st.spinner('สมองกล Chomsuk กำลังคราฟต์สคริปต์ที่ดีที่สุดให้คุณ...'):
            try:
                prompt = f"""
                คุณคือ Copywriter มืออาชีพที่เก่งที่สุดในไทย หน้าที่ของคุณคือเขียนสคริปต์วิดีโอสั้น 30 วินาที 
                สำหรับแบรนด์ชื่อ "Chomsuk" (ชมสุข)
                สินค้าคือ: {product_name} 
                ที่มีจุดเด่นคือ: {features}
                ในสไตล์: {style}
                
                โครงสร้างผลลัพธ์ต้องประกอบด้วย:
                1. Hook (0-3 วิ): คำพูดหยุดนิ้วคนดู
                2. Body (3-25 วิ): เนื้อหาที่น่าเชื่อถือและโน้มน้าวใจ
                3. Call to Action (25-30 วิ): บอกให้คนทักหรือซื้อ
                4. Image Prompt: คำสั่งภาษาอังกฤษ (1 ย่อหน้า) สำหรับไปเจนภาพ AI ให้ดูรวยและสมจริง
                
                เขียนเป็นภาษาไทยที่ลื่นไหล ไม่เป็นหุ่นยนต์ และดูแพง
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
                st.error(f"เกิดข้อผิดพลาดจากระบบหลังบ้าน: {e}")
    else:
        st.warning("กรุณากรอกข้อมูลให้ครบก่อนนะครับ")

st.write("---")
st.caption("© 2026 Chomsuk.ai - Trusted Tech by Kru Ton Thani Chomsuk")