import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

# 1. การตั้งค่าหน้าจอและธีม
st.set_page_config(page_title="Chomsuk.ai - All-in-One AI", page_icon="🏆", layout="wide")

# 🔒 ใช้ Streamlit Secrets และเปลี่ยนเป็นรุ่น 2.0 Flash เพื่อความเสถียรครับ
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("🔑 กรุณาตรวจสอบการตั้งค่า GEMINI_API_KEY ใน Streamlit Secrets นะครับ")

# 2. เมนู Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80) 
    selected = option_menu(
        menu_title="เมนู Chomsuk.ai",
        options=["💡 หาไอเดีย/หัวข้อ", "✍️ เสกคอนเทนต์", "🎨 สตูดิโอเจนภาพ", "🎵 สตูดิโอแต่งเพลง", "🎬 สตูดิโอเจนวีดีโอ", "💳 สมัคร VIP"],
        icons=["lightbulb", "pencil-square", "palette", "music-note-beamed", "camera-video", "person-badge"],
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

    # --- ส่วนที่ 1: สร้างไอเดีย/หัวข้อ ---
    st.subheader("🧠 ปั้นไอเดียคอนเทนต์")
    topic = st.text_input("คุณอยากทำเรื่องอะไร?", placeholder="เช่น การซ่อมมือถือ, การลงทุน", key="idea_topic")

    if st.button("ปั้นไอเดีย!"):
        if topic:
            with st.spinner("Chomsuk.ai กำลังใช้สมองกลคิดให้ครับ..."):
                try:
                    idea_prompt = f"""คุณคือ Chomsuk.ai นักปั้น Content Creator
                    หัวข้อ: {topic}
                    ขอ 5 ไอเดียทำคลิปสั้นให้ไวรัล โดยแต่ละไอเดียต้องมี:
                    1. ชื่อหัวข้อที่น่าดึงดูด
                    2. สรุปเนื้อหาใน 1 ประโยค
                    3. ฮุกเปิดคลิป (ประโยคแรกที่ดึงดูดคนดู)
                    """
                    res = model.generate_content(idea_prompt)
                    st.info(res.text)
                except Exception as e:
                    st.error("🔌 ระบบขัดข้อง: โควต้าอาจจะเต็ม หรือการเชื่อมต่อมีปัญหา ลองกดใหม่อีกครั้งนะครับอาจารย์")
        else:
            st.warning("กรุณาใส่หัวข้อก่อนนะครับ!")

elif selected == "✍️ เสกคอนเทนต์":
    st.title("✍️ เสกคอนเทนต์ (Script Generator)")
    detail = st.text_area("ใส่รายละเอียดสินค้า/บริการ:")
    if st.button("เขียนสคริปต์เลย"):
        if detail:
            with st.spinner("กำลังเขียนบท..."):
                try:
                    res = model.generate_content(f"เขียนสคริปต์ TikTok ขาย {detail} แบบเร้าใจ แยกเป็นฉากๆ")
                    st.success(res.text)
                except:
                    st.error("🔌 โควต้าใช้งานวันนี้อาจจะเต็มแล้วครับ")
        else:
            st.warning("ใส่รายละเอียดก่อนนะครับ")

elif selected == "🎨 สตูดิโอเจนภาพ":
    st.title("🎨 AI Image Prompt Studio")
    img_desc = st.text_input("บรรยายภาพที่อยากได้ (ภาษาไทย):")
    if st.button("แปลงเป็น Prompt อังกฤษ"):
        if img_desc:
            with st.spinner("กำลังแปลเป็นภาษา AI..."):
                try:
                    res = model.generate_content(f"แปลและปรับแก้ข้อความนี้ให้เป็น Image Prompt ภาษาอังกฤษที่ละเอียดสำหรับ AI: {img_desc}")
                    st.code(res.text, language='text')
                except:
                    st.error("🔌 ระบบไม่ตอบสนอง ลองใหม่อีกครั้งครับ")
        else:
            st.warning("บอกรายละเอียดภาพก่อนนะครับ")

elif selected == "🎵 สตูดิโอแต่งเพลง":
    st.title("🎵 AI Songwriter Studio (Suno Edition)")
    st.markdown("เปลี่ยนไอเดียให้เป็นเพลงฮิตสำหรับ [Suno.com](https://suno.com) 🔗")
    
    song_topic = st.text_area("ระบุชื่อแบรนด์หรือเนื้อหาที่ต้องการแต่งเพลง:", placeholder="เช่น ช่างเชื่อมบุรีรัมย์...")
    
    if st.button("🎸 เสกเนื้อเพลง + สไตล์เพลง"):
        if song_topic:
            with st.spinner("Chomsuk.ai กำลังแต่งเพลง..."):
                try:
                    music_prompt = f"""คุณคือ Chomsuk.ai นักแต่งเพลงมือโปร
                    หัวข้อเพลง: {song_topic}
                    กรุณาสร้างข้อมูลสำหรับ Suno.com ดังนี้:
                    1. 📑 [Lyrics]: เขียนเนื้อเพลงภาษาไทยที่มีโครงสร้าง [Verse 1], [Chorus], [Verse 2], [Bridge], [Outro]
                    2. 🎧 [Style of Music]: เขียนคำสั่งภาษาอังกฤษสำหรับช่อง Style
                    """
                    response = model.generate_content(music_prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                except:
                    st.error("🔌 เครื่องมือแต่งเพลงใช้พลังงานครบโควต้าแล้วครับ")
        else:
            st.warning("ระบุหัวข้อเพลงก่อนนะครับ")

elif selected == "🎬 สตูดิโอเจนวีดีโอ":
    st.title("🎬 สตูดิโอเจนวีดีโอ")
    st.markdown("สร้าง Video Prompt พร้อมใช้งานกับ Kling, Luma, Sora และ AI Video ทุกตัว")

    video_topic = st.text_input("ใส่ไอเดีย/หัวข้อที่ต้องการเจนวิดีโอ:", placeholder="เช่น ช่างซ่อมมือถือช่วยลูกค้าแก้ปัญหาเร็วสุดๆ")

    if st.button("🎬 สร้าง Video Prompt"):
        if video_topic:
            with st.spinner("กำลังสร้าง Video Prompt..."):
                try:
                    video_prompt = f"""คุณคือผู้เชี่ยวชาญด้าน AI Video Prompt
                    หัวข้อ: {video_topic}
                    สร้าง Video Prompt ภาษาอังกฤษที่พร้อมใช้งานกับ Kling, Luma, Sora โดยระบุ:
                    1. Scene description (ฉาก/บรรยากาศ)
                    2. Camera movement (การเคลื่อนกล้อง)
                    3. Style & mood (สไตล์และอารมณ์ภาพ)
                    4. Lighting (แสง)
                    ให้ครบในรูปแบบ Prompt เดียว พร้อมใช้ได้เลย
                    """
                    res = model.generate_content(video_prompt)
                    st.code(res.text, language='text')
                    st.caption("✅ ก๊อปปี้ Prompt ด้านบนไปวางในเครื่องมือเจนวิดีโอได้เลยครับ!")
                except Exception as e:
                    st.error("🔌 ระบบขัดข้อง ลองกดใหม่อีกครั้งนะครับ")
        else:
            st.warning("ใส่ไอเดียก่อนนะครับ!")

elif selected == "💳 สมัคร VIP":
    st.title("💳 Chomsuk.ai VIP")
    st.write("ปลดล็อกฟีเจอร์ทั้งหมดและใช้งานได้ไม่จำกัด!")
    st.button("สมัครสมาชิก VIP คลิก")

import google.generativeai as genai

def generate_shopee_content(product_name, details):
    # ใช้ Gemini 2.5 Flash เป็นสมองกล
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    คุณคือผู้เชี่ยวชาญการขายใน Shopee 
    ช่วยเขียนคำโฆษณาสำหรับสินค้า: {product_name}
    ข้อมูลดิบ: {details}
    เป้าหมาย: เขียนให้คนอยากกดตะกร้าทันที พร้อมติด Hashtag ที่เป็นกระแส
    """
    
    response = model.generate_content(prompt)
    return response.text