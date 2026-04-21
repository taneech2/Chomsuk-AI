import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

# 1. การตั้งค่าหน้าจอและธีม
st.set_page_config(page_title="Chomsuk.ai - All-in-One AI", page_icon="🏆", layout="wide")

# 🔒 ใช้ Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"🔑 เชื่อมต่อ API ไม่ได้: {e}")

# 2. กำหนด session_state เริ่มต้น (ป้องกันข้อมูลหาย เมื่อสลับเมนู)
defaults = {
    "idea_result": "",
    "script_result": "",
    "image_result": "",
    "music_result": "",
    "video_result": "",
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# 3. เมนู Sidebar
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
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#FF4D00"},
        }
    )
    st.write("---")
    st.write("User: Kru Ton (Admin)")
    st.caption("© 2026 Chomsuk.ai")

# 4. Logic การทำงานของแต่ละเมนู

# ─────────────────────────────────────────
if selected == "💡 หาไอเดีย/หัวข้อ":
    st.title("💡 หาไอเดียทำคอนเทนต์เงินล้าน")
    st.subheader("🧠 ปั้นไอเดียคอนเทนต์")

    topic = st.text_input("คุณอยากทำเรื่องอะไร?", placeholder="เช่น การซ่อมมือถือ, การลงทุน")

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
                    st.session_state.idea_result = res.text   # ✅ บันทึกผลลัพธ์
                except Exception as e:
                    st.error(f"🔌 Error: {e}")
        else:
            st.warning("กรุณาใส่หัวข้อก่อนนะครับ!")

    # ✅ แสดงผลลัพธ์ที่เก็บไว้ (ไม่หายเมื่อสลับเมนู)
    if st.session_state.idea_result:
        st.info(st.session_state.idea_result)
        if st.button("🗑️ ล้างผลลัพธ์", key="clear_idea"):
            st.session_state.idea_result = ""
            st.rerun()

# ─────────────────────────────────────────
elif selected == "✍️ เสกคอนเทนต์":
    st.title("✍️ เสกคอนเทนต์ (Script Generator)")

    detail = st.text_area("ใส่รายละเอียดสินค้า/บริการ:")

    if st.button("เขียนสคริปต์เลย"):
        if detail:
            with st.spinner("กำลังเขียนบท..."):
                try:
                    res = model.generate_content(f"เขียนสคริปต์ TikTok ขาย {detail} แบบเร้าใจ แยกเป็นฉากๆ")
                    st.session_state.script_result = res.text   # ✅ บันทึกผลลัพธ์
                except Exception as e:
                    st.error(f"🔌 Error: {e}")
        else:
            st.warning("ใส่รายละเอียดก่อนนะครับ")

    # ✅ แสดงผลลัพธ์ที่เก็บไว้
    if st.session_state.script_result:
        st.success(st.session_state.script_result)
        if st.button("🗑️ ล้างผลลัพธ์", key="clear_script"):
            st.session_state.script_result = ""
            st.rerun()

# ─────────────────────────────────────────
elif selected == "🎨 สตูดิโอเจนภาพ":
    st.title("🎨 AI Image Prompt Studio")

    img_desc = st.text_input("บรรยายภาพที่อยากได้ (ภาษาไทย):")

    if st.button("แปลงเป็น Prompt อังกฤษ"):
        if img_desc:
            with st.spinner("กำลังแปลเป็นภาษา AI..."):
                try:
                    res = model.generate_content(f"แปลและปรับแก้ข้อความนี้ให้เป็น Image Prompt ภาษาอังกฤษที่ละเอียดสำหรับ AI: {img_desc}")
                    st.session_state.image_result = res.text   # ✅ บันทึกผลลัพธ์
                except Exception as e:
                    st.error(f"🔌 Error: {e}")
        else:
            st.warning("บอกรายละเอียดภาพก่อนนะครับ")

    # ✅ แสดงผลลัพธ์ที่เก็บไว้
    if st.session_state.image_result:
        st.code(st.session_state.image_result, language='text')
        if st.button("🗑️ ล้างผลลัพธ์", key="clear_image"):
            st.session_state.image_result = ""
            st.rerun()

# ─────────────────────────────────────────
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
                    st.session_state.music_result = response.text   # ✅ บันทึกผลลัพธ์
                except Exception as e:
                    st.error(f"🔌 Error: {e}")
        else:
            st.warning("ระบุหัวข้อเพลงก่อนนะครับ")

    # ✅ แสดงผลลัพธ์ที่เก็บไว้
    if st.session_state.music_result:
        st.markdown("---")
        st.markdown(st.session_state.music_result)
        if st.button("🗑️ ล้างผลลัพธ์", key="clear_music"):
            st.session_state.music_result = ""
            st.rerun()

# ─────────────────────────────────────────
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
                    st.session_state.video_result = res.text   # ✅ บันทึกผลลัพธ์
                except Exception as e:
                    st.error(f"🔌 Error: {e}")
        else:
            st.warning("ใส่ไอเดียก่อนนะครับ!")

    # ✅ แสดงผลลัพธ์ที่เก็บไว้
    if st.session_state.video_result:
        st.code(st.session_state.video_result, language='text')
        st.caption("✅ ก๊อปปี้ Prompt ด้านบนไปวางในเครื่องมือเจนวิดีโอได้เลยครับ!")
        if st.button("🗑️ ล้างผลลัพธ์", key="clear_video"):
            st.session_state.video_result = ""
            st.rerun()

# ─────────────────────────────────────────
elif selected == "💳 สมัคร VIP":
    st.title("💳 Chomsuk.ai VIP")
    st.write("ปลดล็อกฟีเจอร์ทั้งหมดและใช้งานได้ไม่จำกัด!")
    st.button("สมัครสมาชิก VIP คลิก")
