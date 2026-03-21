# --- เพิ่มในส่วนของเมนู Sidebar ---
with st.sidebar:
    selected = option_menu(
        menu_title="เมนู Chomsuk.ai",
        options=["💡 หาไอเดีย/หัวข้อ", "✍️ เสกคอนเทนต์", "🎨 สตูดิโอเจนภาพ", "🎵 สตูดิโอแต่งเพลง", "💳 สมัคร VIP"],
        icons=["lightbulb", "pencil-square", "palette", "music-note-beamed", "person-badge"],
        menu_icon="cast",
        default_index=0,
    )

# --- เพิ่ม Logic สำหรับเมนู "สตูดิโอแต่งเพลง" ---
if selected == "🎵 สตูดิโอแต่งเพลง":
    st.title("🎵 AI Songwriter Studio (Suno Edition)")
    st.subheader("เปลี่ยนชื่อแบรนด์หรือไอเดีย ให้เป็นเพลงฮิตติดหู!")
    
    topic = st.text_area("อยากแต่งเพลงเกี่ยวกับอะไร? (เช่น ครีมหน้าใส, ช่างเชื่อมบุรีรัมย์):")
    
    if st.button("🎸 เสกเนื้อเพลง + สไตล์เพลง"):
        if topic:
            with st.spinner("Chomsuk.ai กำลังประพันธ์เพลง..."):
                # พรอมต์ที่ออกแบบมาเพื่อ Suno โดยเฉพาะ
                music_prompt = f"""คุณคือ Chomsuk.ai นักแต่งเพลงมือโปร
                หัวข้อเพลง: {topic}
                
                กรุณาสร้างข้อมูล 2 ส่วนสำหรับใช้ใน Suno.com:
                
                1. 📑 [Lyrics]: เขียนเนื้อเพลงภาษาไทยที่มีโครงสร้าง [Verse 1], [Chorus], [Verse 2], [Outro] 
                   เน้นคำที่ฟังแล้ว 'จอย' เข้าใจง่าย และสื่อถึงหัวข้อที่ให้มา
                   
                2. 🎧 [Style of Music]: เขียนคำสั่งภาษาอังกฤษ (Style Prompt) สำหรับ Suno 
                   ระบุแนวเพลง, เครื่องดนตรี, อารมณ์เพลง และ BPM (เช่น Melodic Thai Rock, 90s Pop, Heavy Drums, 120 BPM)
                """
                
                response = model.generate_content(music_prompt)
                st.markdown("---")
                st.success("ประพันธ์เพลงเสร็จแล้ว!")
                st.markdown(response.text)
        else:
            st.warning("กรุณากรอกหัวข้อก่อนนะครับอาจารย์!")