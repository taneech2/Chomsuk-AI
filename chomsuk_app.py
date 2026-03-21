import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

# 1. การตั้งค่าหน้าจอและธีม
st.set_page_config(page_title="Chomsuk.ai - All-in-One AI", page_icon="🏆", layout="wide")

# 🔑 ใส่ API Key ของอาจารย์ตรงนี้ (ห้ามลบเครื่องหมายคำพูดนะครับ)
genai.configure(api_key="ใส่_API_KEY_ของอาจารย์ตรงนี้")
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. เมนู Sidebar (เพิ่มเมนูแต่งเพลงเข้าไปแล้วครับ)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80) # โลโก้สมมติ
    selected = option_menu(
        menu_title="เมนู Chomsuk.ai",
        options=["💡 หาไอเดีย/หัวข้อ", "✍️ เสกคอนเทนต์", "🎨 สตูดิโอเจนภาพ", "🎵 สตูดิโอแต่งเพลง", "💳 สมัคร VIP"],
        icons=["lightbulb", "pencil-square", "palette", "music-note-beamed", "person-badge"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#0e1117"},
            "icon": {"color": "#FF4D00", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#FF4D00"},
        }
    )
    st.write("---")
    st.write(f"User: Kru Ton (Admin)")
    st.caption("© 2026 Chomsuk.ai")

# 3. Logic การทำงานของแต่ละเมนู
if selected == "💡 หาไอเดีย/หัวข้อ":
    st.title("💡 หาไอเดียทำคอนเทนต์เงินล้าน")
    topic = st.text_input("คุณอยากทำเรื่องอะไร?", placeholder="เช่น การซ่อมมือถือ, การลงทุน")
    if st.button("ปั้นไอเดีย!"):
        with st.spinner("กำลังใช้สมองกลคิดให้ครับ..."):
            res = model.generate_content(f"ขอ 5 ไอเดียทำคลิป TikTok เกี่ยวกับ {topic} ให้ไวรัล")
            st.info(res.text)

elif selected == "✍️ เสกคอนเทนต์":
    st.title("✍️ เสกคอนเทนต์ (Script Generator)")
    detail = st.text_area("ใส่รายละเอียดสินค้า/บริการ:")
    if st.button("เขียนสคริปต์เลย"):
        with st.spinner("กำลังเขียนบท..."):
            res = model.generate_content(f"เขียนสคริปต์ TikTok ขาย {detail} แบบเร้าใจ แยกเป็นฉากๆ")
            st.success(res.text)

elif selected == "🎨 สตูดิโอเจนภาพ":
    st.title("🎨 AI Image Prompt Studio")
    img_desc = st.text_input("บรรยายภาพที่อยากได้ (ภาษาไทย):")
    if st.button("แปลงเป็น Prompt อังกฤษ"):
        with st.spinner("กำลังแปลเป็นภาษา AI..."):
            res = model.generate_content(f"แปลและปรับแก้ข้อความนี้ให้เป็น Image Prompt ภาษาอังกฤษที่ละเอียดสำหรับ AI: {img_desc}")
            st.code(res.text, language='text')

# --- ฟีเจอร์ใหม่ที่อาจารย์ต้องการ ---
elif selected == "🎵 สตูดิโอแต่งเพลง":
    st.title("🎵 AI Songwriter Studio (Suno Edition)")
    st.subheader("เปลี่ยนไอเดียให้เป็นเพลงฮิตสำหรับ Suno.com")
    
    song_topic = st.text_area("อยากแต่งเพลงเกี่ยวกับอะไร? (ระบุชื่อแบรนด์หรือเนื้อหาที่ต้องการ):")
    
    if st.button("🎸 เสกเนื้อเพลง + สไตล์เพลง"):
        if song_topic:
            with st.spinner("Chomsuk.ai กำลังประพันธ์เพลง..."):
                music_prompt = f"""คุณคือ Chomsuk.ai นักแต่งเพลงมือโปร
                หัวข้อเพลง: {song_topic}
                
                กรุณาสร้างข้อมูล 2 ส่วนสำหรับใช้ใน Suno.com:
                1. 📑 [Lyrics]: เขียนเนื้อเพลงภาษาไทยที่มีโครงสร้าง [Verse 1], [Chorus], [Verse 2], [Outro] ให้ซึ้งหรือมันส์ตามความเหมาะสม
                2. 🎧 [Style of Music]: เขียนคำสั่งภาษาอังกฤษ (Style Prompt) สำหรับช่อง Style ใน Suno เช่นแนวเพลง, เครื่องดนตรี (เช่น Thai Rock, 808 Bass, Melodic)
                """
                response = model.generate_content(music_prompt)
                st.markdown("---")
                st.markdown(response.text)
        else:
            st.warning("ใส่หัวข้อก่อนนะครับอาจารย์!")

elif selected == "💳 สมัคร VIP":
    st.title("💳 Chomsuk.ai VIP")
    st.write("ปลดล็อกฟีเจอร์ทั้งหมดและใช้งานได้ไม่จำกัด!")
    st.button("สมัครสมาชิก VIP คลิก")