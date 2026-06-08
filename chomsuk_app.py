"""
Chomsuk.ai — All-in-One AI Content Studio
Version 2.0 — จัดเต็ม Edition
by บริษัทชมสุข69 / Kru Ton
"""

import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Chomsuk.ai - AI Content Studio",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .stApp { background-color: #0e1117; }
  .block-container { padding-top: 1.5rem; }

  /* Page title */
  .page-header {
    background: linear-gradient(90deg, #FF4D00, #FF8C00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0.25rem;
  }
  .page-sub {
    color: #999;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  /* Mode badge */
  .kru-badge {
    background: linear-gradient(135deg, #FF4D00, #FF8C00);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 8px;
  }

  /* Result box */
  .result-header {
    color: #FF8C00;
    font-weight: 700;
    font-size: 1rem;
    margin: 1rem 0 0.25rem 0;
  }

  /* VIP card */
  .vip-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #FFD700;
    border-radius: 14px;
    padding: 24px;
  }
  .free-card {
    background: #1a1a2e;
    border: 1px solid #444;
    border-radius: 14px;
    padding: 24px;
  }

  /* Subtle info box */
  .tip-box {
    background: #1e2129;
    border-left: 3px solid #FF4D00;
    padding: 10px 14px;
    border-radius: 0 8px 8px 0;
    font-size: 0.85rem;
    color: #bbb;
    margin: 0.5rem 0 1rem 0;
  }

  /* Stats row */
  div[data-testid="metric-container"] {
    background: #1e2129;
    border-radius: 10px;
    padding: 12px 16px;
    border: 1px solid #2a2a3e;
  }
</style>
""", unsafe_allow_html=True)

# ─── API SETUP ───────────────────────────────────────────────────────────────
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception as e:
    st.error(f"🔑 เชื่อมต่อ Gemini API ไม่ได้: {e}")
    st.stop()

# ─── SESSION STATE ───────────────────────────────────────────────────────────
_defaults = {
    "idea_result":     "",
    "script_result":   "",
    "shopee_result":   "",
    "image_result":    "",
    "music_result":    "",
    "video_result":    "",
    "kru_mode":        False,
    "vip_unlocked":    False,
    "usage_count":     0,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def kru_ctx() -> str:
    """Return ครูช่าง context block when mode is on."""
    if st.session_state.kru_mode:
        return (
            "\n\n[บริบทผู้ใช้]\n"
            "ผู้ใช้คือ ครูช่างเชื่อมโลหะ วิทยาลัยการอาชีพบุรีรัมย์\n"
            "กลุ่มเป้าหมาย: นักเรียนอาชีวศึกษา ช่างเทคนิค ผู้สนใจงานช่าง\n"
            "โดเมน: งานเชื่อม MIG/TIG/MMA, CNC, NDT, ต่อเรือ, อาชีวศึกษา\n"
            "ให้เนื้อหาเชื่อมโยงกับงานช่าง/โรงฝึกงาน ถ้าเป็นไปได้\n"
        )
    return ""


def stream_ai(prompt: str, state_key: str):
    """
    สร้าง content แบบ streaming — ข้อความไหลทีละ chunk
    บันทึกผลลัพธ์ใน st.session_state[state_key]
    """
    placeholder = st.empty()
    full_text = ""
    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                full_text += chunk.text
                # แสดง cursor กระพริบขณะ stream
                placeholder.markdown(full_text + " ▌")
        # ลบ cursor ออกเมื่อเสร็จ
        placeholder.markdown(full_text)
        st.session_state[state_key] = full_text
        st.session_state.usage_count += 1
    except Exception as err:
        st.error(f"❌ Gemini Error: {err}")
        full_text = ""
    return full_text


def show_result(state_key: str, filename: str = "output.txt"):
    """
    แสดง result box พร้อม copy button (built-in ใน st.code) และ download
    """
    txt = st.session_state.get(state_key, "")
    if not txt:
        return
    st.markdown('<p class="result-header">📋 ผลลัพธ์  —  กด Copy ได้เลย (ไอคอนมุมขวา)</p>',
                unsafe_allow_html=True)
    # st.code() มี copy button ในตัว ✅
    st.code(txt, language="")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("💾 บันทึกเป็น .txt", txt,
                           file_name=filename, mime="text/plain",
                           use_container_width=True)
    with col2:
        if st.button("🗑️ ล้างผลลัพธ์", key=f"clear_{state_key}",
                     use_container_width=True):
            st.session_state[state_key] = ""
            st.rerun()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=70)

    selected = option_menu(
        menu_title="Chomsuk.ai",
        options=[
            "💡 หาไอเดีย/หัวข้อ",
            "✍️ เสกคอนเทนต์",
            "🛒 Shopee Affiliate",
            "🎨 สตูดิโอเจนภาพ",
            "🎵 สตูดิโอแต่งเพลง",
            "🎬 สตูดิโอเจนวีดีโอ",
            "💳 สมัคร VIP",
        ],
        icons=["lightbulb", "pencil-square", "cart3",
               "palette", "music-note-beamed", "camera-video", "person-badge"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container":         {"padding": "5!important", "background-color": "#0e1117"},
            "icon":              {"color": "#FF4D00", "font-size": "18px"},
            "nav-link":          {"font-size": "15px", "text-align": "left",
                                  "margin": "0px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#FF4D00"},
        }
    )

    st.markdown("---")

    # ───  ครูช่าง Mode Toggle
    new_mode = st.toggle(
        "🔧 ครูช่าง Mode",
        value=st.session_state.kru_mode,
        help="เปิด = AI จะปรับ Output ให้เหมาะกับครูช่าง/นักเรียนอาชีวะทุกครั้ง"
    )
    st.session_state.kru_mode = new_mode
    if new_mode:
        st.markdown('<div class="kru-badge">🔧 ครูช่าง Mode: ON</div>', unsafe_allow_html=True)
    else:
        st.caption("ครูช่าง Mode: Off")

    st.markdown("---")

    # Stats
    c1, c2 = st.columns(2)
    c1.metric("ใช้งานแล้ว", st.session_state.usage_count)
    c2.metric("สถานะ", "👑 VIP" if st.session_state.vip_unlocked else "Free")

    st.markdown("---")
    if st.session_state.vip_unlocked:
        st.success("👑 VIP Member")
    st.write("User: Kru Ton (Admin)")
    st.caption("© 2026 Chomsuk.ai · บริษัทชมสุข69")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — หาไอเดีย
# ═══════════════════════════════════════════════════════════════════════════════
if selected == "💡 หาไอเดีย/หัวข้อ":
    st.markdown('<div class="page-header">💡 หาไอเดียทำคอนเทนต์</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">ป้อนหัวข้อ → ได้ 5 ไอเดียพร้อม Hook + Hashtag</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("คุณอยากทำเรื่องอะไร?",
                              placeholder="เช่น การเชื่อม MIG, ซ่อมมือถือ, ปลูกผัก hydro, ขนมไทย")
    with col2:
        platform = st.selectbox("แพลตฟอร์ม",
                                ["TikTok", "YouTube Shorts", "YouTube (ยาว)", "Facebook", "Instagram Reels"])

    col3, col4 = st.columns(2)
    with col3:
        fmt = st.radio("รูปแบบ", ["ทั่วไป", "How-to สอน", "รีวิวสินค้า", "เล่าเรื่อง", "เทรนด์/ข่าว"],
                       horizontal=True)
    with col4:
        audience = st.text_input("กลุ่มเป้าหมาย (ไม่บังคับ)",
                                 placeholder="เช่น นักเรียนช่าง, แม่บ้าน, วัยรุ่น")

    if st.button("🚀 ปั้นไอเดีย 5 ข้อ!", type="primary", use_container_width=True):
        if not topic:
            st.warning("⚠️ ใส่หัวข้อก่อนนะครับ!")
        else:
            aud_line = f"กลุ่มเป้าหมาย: {audience}" if audience else ""
            prompt = f"""คุณคือ Content Strategist มืออาชีพที่เชี่ยวชาญ {platform} ในตลาดไทย
{kru_ctx()}
หัวข้อ: {topic}
รูปแบบ: {fmt}
แพลตฟอร์ม: {platform}
{aud_line}

สร้าง 5 ไอเดียคอนเทนต์ที่มีโอกาสไวรัลสูง แต่ละข้อต้องมีครบ:

🎯 ชื่อหัวข้อ: (กระชับ ดึงดูด น่าคลิก)
📌 แก่นเรื่อง: (1 ประโยค)
🪝 ฮุกเปิด: (ประโยคแรกที่ทำให้หยุดดูทันที — พูดหรือขึ้นจอ)
📊 เหตุผลที่ไวรัล: (1 บรรทัด)
#️⃣ Hashtag: (#แท็ก1 #แท็ก2 #แท็ก3 #แท็ก4 #แท็ก5)

ตอบภาษาไทย ให้ครบทั้ง 5 ไอเดีย อย่าย่อ"""
            with st.spinner(""):
                stream_ai(prompt, "idea_result")

    show_result("idea_result", "ideas.txt")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — เสกคอนเทนต์
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "✍️ เสกคอนเทนต์":
    st.markdown('<div class="page-header">✍️ เสกคอนเทนต์ — Script Generator Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">ใส่รายละเอียด → ได้ Script พูดได้เลย + Visual Guide</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        detail = st.text_area(
            "สินค้า / บริการ / หัวข้อที่ต้องการทำคอนเทนต์:",
            height=130,
            placeholder="เช่น  หน้ากากเชื่อม Auto-Darkening Solar ราคา 890 บาท ป้องกัน UV/IR ปรับแสงได้ DIN 9-13"
        )
    with col2:
        script_type = st.selectbox("ประเภท Script",
                                   ["TikTok/Reels ขายสินค้า", "YouTube รีวิวยาว",
                                    "How-to สาธิต", "Storytelling เล่าเรื่อง",
                                    "โฆษณา 15 วินาที", "Live สด"])
        tone = st.selectbox("โทนเสียง",
                            ["สนุก/เป็นกันเอง", "เชี่ยวชาญ/มืออาชีพ",
                             "ตื่นเต้น/เร้าใจ", "นุ่มนวล/น่าเชื่อถือ"])
        duration = st.selectbox("ความยาวคลิป",
                                ["15 วินาที", "30 วินาที", "60 วินาที",
                                 "3 นาที", "5–10 นาที"])

    if st.button("🎬 เขียน Script เลย!", type="primary", use_container_width=True):
        if not detail:
            st.warning("⚠️ ใส่รายละเอียดก่อนนะครับ!")
        else:
            prompt = f"""คุณคือ Script Writer มืออาชีพสำหรับ Content Creator ไทย
{kru_ctx()}
สินค้า/หัวข้อ: {detail}
ประเภท: {script_type}
โทน: {tone}
ความยาว: {duration}

เขียน Script สมบูรณ์แบบ ใช้งานได้ทันที ประกอบด้วย:

🪝 HOOK (3 วินาทีแรก — สิ่งที่พูดหรือขึ้นจอ เพื่อให้คนหยุดดู):

📖 BODY (แบ่งเป็นฉาก ระบุว่าช่วงนี้พูดอะไร ถ่ายอะไร):
  - ฉาก 1: [พูด] / [ภาพ]
  - ฉาก 2: [พูด] / [ภาพ]
  ... (ต่อตามความยาว)

💥 CTA (Call to Action — จบแล้วให้คนทำอะไร):

🎤 FULL SCRIPT (ทุกคำที่ต้องพูด — อ่านได้เลย):

📸 VISUAL GUIDE (รายการภาพ/มุมกล้องที่ต้องถ่ายแต่ละช่วง):

📱 CAPTION + HASHTAG (พร้อมโพสต์):"""
            with st.spinner(""):
                stream_ai(prompt, "script_result")

    show_result("script_result", "script.txt")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SHOPEE AFFILIATE  🆕
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "🛒 Shopee Affiliate":
    st.markdown('<div class="page-header">🛒 Shopee Affiliate Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">ป้อนสินค้า → ได้ Script รีวิว + Caption + Hashtag + แผน 7 วัน</div>', unsafe_allow_html=True)

    tab_review, tab_plan = st.tabs(["📦 สร้าง Content รีวิวสินค้า", "📅 แผน Content 7 วัน"])

    # ── Tab: รีวิวสินค้า ──────────────────────────────────────────────────────
    with tab_review:
        col1, col2 = st.columns([3, 1])
        with col1:
            product = st.text_input(
                "ชื่อสินค้า หรือ วางลิงก์ Shopee:",
                placeholder="เช่น  ลวดเชื่อม MIG 0.8mm 5kg  หรือ  https://shopee.co.th/..."
            )
        with col2:
            price = st.text_input("ราคา (บาท)", placeholder="890")

        product_detail = st.text_area(
            "รายละเอียดเพิ่มเติม (ไม่บังคับ)",
            height=70,
            placeholder="เช่น ทนความร้อนสูง เชื่อมเหล็ก-สแตนเลส ไม่มีสะเก็ดมาก"
        )

        col3, col4 = st.columns(2)
        with col3:
            aff_platform = st.radio(
                "สร้าง Content สำหรับ:",
                ["TikTok Shop", "YouTube", "Facebook", "ครบทุกแพลตฟอร์ม"],
                horizontal=True
            )
        with col4:
            aff_tone = st.radio(
                "โทนรีวิว:",
                ["เป็นกันเอง", "เชี่ยวชาญ", "ตื่นเต้น/กระตุ้นซื้อ"],
                horizontal=True
            )

        if st.button("🚀 สร้าง Affiliate Content!", type="primary", use_container_width=True):
            if not product:
                st.warning("⚠️ ใส่ชื่อสินค้าก่อนนะครับ!")
            else:
                price_txt = f"ราคา {price} บาท" if price else ""
                prompt = f"""คุณคือ Affiliate Marketing Expert เชี่ยวชาญ Shopee Thailand
{kru_ctx()}
สินค้า: {product} {price_txt}
รายละเอียด: {product_detail}
แพลตฟอร์ม: {aff_platform}
โทนรีวิว: {aff_tone}

สร้าง Affiliate Content ครบชุด:

━━━ 1. TITLE / ชื่อที่ดึงดูด ━━━
(ชื่อสำหรับ caption / thumbnail ที่ทำให้อยากคลิก)

━━━ 2. จุดเด่น 5 ข้อ ━━━
• ข้อ 1:
• ข้อ 2:
• ข้อ 3:
• ข้อ 4:
• ข้อ 5:

━━━ 3. SCRIPT รีวิว (พูดตามได้เลย) ━━━
🪝 Hook (3 วิแรก):
📖 เนื้อหารีวิว:
💥 CTA + ลิงก์ตะกร้า:

━━━ 4. CAPTION พร้อมโพสต์ ({aff_platform}) ━━━

━━━ 5. HASHTAG (15 แท็ก) ━━━

━━━ 6. FAQ — คำถามที่ลูกค้ามักถาม + คำตอบสั้น ━━━
Q1: / A1:
Q2: / A2:
Q3: / A3:

━━━ 7. กลุ่มเป้าหมาย & วิธีเจาะตลาด ━━━

ตอบภาษาไทย ให้ใช้ได้ทันที"""
                with st.spinner(""):
                    stream_ai(prompt, "shopee_result")

        show_result("shopee_result", "affiliate_content.txt")

    # ── Tab: แผน 7 วัน ────────────────────────────────────────────────────────
    with tab_plan:
        st.markdown('<div class="tip-box">💡 ทำสินค้าเดียวให้ครบ 7 คลิป = เพิ่มโอกาส commission 7 เท่า</div>',
                    unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            product_7 = st.text_input("สินค้าที่จะ push:", placeholder="เช่น หน้ากากเชื่อม Auto-Darkening", key="p7")
        with col2:
            main_platform_7 = st.selectbox("แพลตฟอร์มหลัก", ["TikTok", "YouTube", "Facebook"])

        if st.button("📅 สร้างแผน Content 7 วัน!", type="primary", use_container_width=True):
            if not product_7:
                st.warning("⚠️ ใส่ชื่อสินค้าก่อนนะครับ!")
            else:
                prompt = f"""คุณคือ Content Strategist ผู้เชี่ยวชาญ Affiliate Marketing บน {main_platform_7}
{kru_ctx()}
สินค้า: {product_7}
แพลตฟอร์มหลัก: {main_platform_7}

สร้าง Content Plan 7 วัน เพื่อ push ยอดขาย Affiliate
แต่ละวันต้องแตกต่างกัน ไม่ซ้ำแนวทาง:

วันที่ 1: (แนวรีวิวตรงๆ)
  หัวข้อ:
  Hook:
  จุดขาย:
  CTA:

วันที่ 2: (แนว How-to / สาธิตใช้งาน)
  ...

วันที่ 3: (แนว Storytelling / ปัญหาก่อนใช้ vs หลังใช้)
  ...

วันที่ 4: (แนว Comparison / เทียบของเก่า vs ใหม่)
  ...

วันที่ 5: (แนว FAQ / ตอบคำถามพบบ่อย)
  ...

วันที่ 6: (แนว Social Proof / คนอื่นใช้แล้วเป็นยังไง)
  ...

วันที่ 7: (แนว FOMO / โปรโมชัน ลดราคา รีบซื้อ)
  ...

สรุป: เวลาโพสต์ที่ดีที่สุดของแต่ละวัน"""
                with st.spinner(""):
                    stream_ai(prompt, "shopee_result")

        show_result("shopee_result", "7day_plan.txt")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — สตูดิโอเจนภาพ
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "🎨 สตูดิโอเจนภาพ":
    st.markdown('<div class="page-header">🎨 AI Image Prompt Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">แปลงไอเดียภาษาไทย → Prompt พร้อมใช้กับ Midjourney · DALL-E · Stable Diffusion · Adobe Firefly</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        img_desc = st.text_area(
            "บรรยายภาพที่อยากได้ (ภาษาไทยก็ได้):",
            height=130,
            placeholder="เช่น  ช่างเชื่อมใส่หน้ากาก Auto-Dark กำลังเชื่อม TIG บนท่อสแตนเลส มีประกายไฟสวยงาม บรรยากาศโรงงาน แสงดราม่า"
        )
    with col2:
        style = st.selectbox("สไตล์ภาพ",
                             ["Photorealistic 8K", "Cinematic Film", "Anime / Illustration",
                              "Product Photography", "Dark & Moody Industrial", "Corporate Clean"])
        ratio = st.selectbox("สัดส่วนภาพ (Aspect Ratio)",
                             ["16:9 — YouTube Thumbnail", "9:16 — TikTok/Reels",
                              "1:1 — Square/Feed", "4:5 — Instagram Portrait"])
        tool_target = st.selectbox("เครื่องมือที่ใช้",
                                   ["Midjourney", "DALL-E 3", "Stable Diffusion XL",
                                    "Adobe Firefly", "Leonardo AI", "ทั่วไป"])

    neg = st.text_input("Negative Prompt เพิ่มเติม:",
                        value="blurry, low quality, watermark, text overlay, bad anatomy",
                        placeholder="สิ่งที่ไม่ต้องการในภาพ")

    if st.button("✨ สร้าง Image Prompt!", type="primary", use_container_width=True):
        if not img_desc:
            st.warning("⚠️ บรรยายภาพก่อนนะครับ!")
        else:
            ar_code = ratio.split("—")[0].strip().replace(":", ":")
            prompt = f"""คุณคือ AI Image Prompt Engineer ผู้เชี่ยวชาญ {tool_target}
{kru_ctx()}
บรรยาย: {img_desc}
สไตล์: {style}
Aspect Ratio: {ar_code}
เครื่องมือ: {tool_target}

สร้างสิ่งต่อไปนี้:

━━━ MAIN PROMPT (ภาษาอังกฤษ ละเอียด ใช้ได้เลย) ━━━

━━━ NEGATIVE PROMPT (เพิ่มจาก: {neg}) ━━━

━━━ SETTINGS แนะนำสำหรับ {tool_target} ━━━
  - Aspect Ratio / Size:
  - Style / Version:
  - CFG / Guidance Scale:
  - Quality / Steps:
  - Seed แนะนำ (ถ้ามี):

━━━ VARIATION PROMPTS (3 แนวเสริม) ━━━
  1.
  2.
  3."""
            with st.spinner(""):
                stream_ai(prompt, "image_result")

    show_result("image_result", "image_prompt.txt")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — สตูดิโอแต่งเพลง
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "🎵 สตูดิโอแต่งเพลง":
    st.markdown('<div class="page-header">🎵 AI Songwriter Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">บอกแค่ว่าอยากได้เพลงแบบไหน → ได้ Lyrics + Style Tag สำหรับ Suno / Udio ทันที</div>',
                unsafe_allow_html=True)

    song_topic = st.text_area(
        "อยากได้เพลงแบบไหน? (บอกตรงๆ ภาษาอะไรก็ได้):",
        height=120,
        placeholder=(
            "เช่น  เพลงลูกทุ่งอีสาน ฮึกเหิม ปลุกใจนักเรียนช่างสู้ไม่ถอย\n"
            "หรือ  pop เศร้า ภาษาไทย เรื่องรอคนที่รัก\n"
            "หรือ  rock สนุก เกี่ยวกับการเชื่อมโลหะ"
        )
    )

    if st.button("🎸 แต่งเพลงเลย!", type="primary", use_container_width=True):
        if not song_topic:
            st.warning("⚠️ บอกว่าอยากได้เพลงแบบไหนก่อนนะครับ!")
        else:
            prompt = f"""คุณคือ Songwriter มืออาชีพที่เชี่ยวชาญเพลงไทย
{kru_ctx()}
โจทย์: {song_topic}

วิเคราะห์โจทย์แล้วเลือกแนวเพลง ภาษา และอารมณ์ที่เหมาะที่สุดเอง
จากนั้นแต่งเพลงให้สมบูรณ์:

━━━ ชื่อเพลง ━━━

━━━ LYRICS ━━━
[Verse 1]

[Chorus]

[Verse 2]

[Chorus]

[Bridge]

[Outro]

━━━ SUNO / UDIO STYLE TAG ━━━
(copy วางใน Style box ของ Suno.com หรือ Udio.com ได้เลย)
Style prompt:
BPM:
Key:"""
            with st.spinner(""):
                stream_ai(prompt, "music_result")

    show_result("music_result", "song_lyrics.txt")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — สตูดิโอเจนวีดีโอ
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "🎬 สตูดิโอเจนวีดีโอ":
    st.markdown('<div class="page-header">🎬 AI Video Prompt Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">สร้าง Prompt สำหรับ Kling AI · Luma Dream Machine · Runway Gen-3 · Sora</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        vid_topic = st.text_area(
            "ไอเดีย/เนื้อหาวีดีโอ:",
            height=130,
            placeholder="เช่น  ช่างเชื่อม MIG กำลังเชื่อมโครงสร้างเหล็ก H-Beam สูง 10 เมตร แสงอาทิตย์ตอนเย็น ประกายไฟสีทองพุ่ง"
        )
        vid_tool = st.selectbox("เครื่องมือ AI Video",
                                ["Kling AI 1.6", "Luma Dream Machine", "Runway Gen-3",
                                 "Sora (OpenAI)", "Pika 2.0", "ทั่วไป"])
    with col2:
        v_style = st.selectbox("สไตล์",
                               ["Cinematic / ภาพยนตร์", "Documentary สารคดี",
                                "Music Video", "Product Demo", "Social Media Short",
                                "Time-lapse / Hyperlapse"])
        v_dur = st.selectbox("ความยาว", ["5 วินาที", "10 วินาที", "15 วินาที", "30 วินาที"])
        cam_moves = st.multiselect(
            "การเคลื่อนกล้อง",
            ["Slow motion 240fps", "Extreme close-up", "Wide establishing shot",
             "Drone aerial", "Tracking shot", "Dolly push-in", "Handheld"],
            default=["Slow motion 240fps", "Extreme close-up"]
        )

    if st.button("🎬 สร้าง Video Prompt!", type="primary", use_container_width=True):
        if not vid_topic:
            st.warning("⚠️ ใส่ไอเดียก่อนนะครับ!")
        else:
            cam_txt = ", ".join(cam_moves) if cam_moves else "auto"
            prompt = f"""คุณคือ AI Video Director ผู้เชี่ยวชาญ {vid_tool}
{kru_ctx()}
เนื้อหา: {vid_topic}
เครื่องมือ: {vid_tool}
สไตล์: {v_style}
ความยาว: {v_dur}
กล้อง: {cam_txt}

สร้าง:

━━━ MAIN VIDEO PROMPT (ภาษาอังกฤษ ละเอียดมาก พร้อมใช้) ━━━

━━━ SCENE BREAKDOWN ━━━
  Scene 1 (0–2s):
  Scene 2 (2–4s):
  Scene 3 (4–{v_dur}):

━━━ CAMERA & MOTION ━━━

━━━ COLOR GRADE & MOOD ━━━

━━━ SOUND DESIGN แนะนำ ━━━

━━━ SETTINGS สำหรับ {vid_tool} ━━━
  Aspect Ratio:
  Motion Strength:
  Seed / Style Ref:

━━━ NEGATIVE PROMPT ━━━"""
            with st.spinner(""):
                stream_ai(prompt, "video_result")

    show_result("video_result", "video_prompt.txt")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — VIP
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "💳 สมัคร VIP":
    st.markdown('<div class="page-header">👑 Chomsuk.ai VIP</div>', unsafe_allow_html=True)

    if st.session_state.vip_unlocked:
        st.balloons()
        st.success("🎉 ยินดีต้อนรับ VIP Member! ใช้งานได้ไม่จำกัดครับ")
        st.markdown("""
        ### สิทธิ์ทั้งหมดของคุณ
        | สิทธิ์ | สถานะ |
        |--------|--------|
        | ใช้งานทุกฟีเจอร์ไม่จำกัด | ✅ |
        | 🛒 Shopee Affiliate Engine | ✅ |
        | 📅 แผน Content 7 วัน | ✅ |
        | 💾 Download ทุกไฟล์ | ✅ |
        | 🔧 ครูช่าง Mode | ✅ |
        | Priority Support | ✅ |
        | Early Access ฟีเจอร์ใหม่ | ✅ |
        """)
    else:
        col_free, col_vip = st.columns(2)

        with col_free:
            st.markdown('<div class="free-card">', unsafe_allow_html=True)
            st.markdown("### 🆓 Free")
            st.markdown("""
- ✅ หาไอเดีย
- ✅ เสกคอนเทนต์
- ✅ เจนภาพ Prompt
- ✅ แต่งเพลง
- ✅ เจนวีดีโอ Prompt
- ❌ Shopee Affiliate Engine
- ❌ แผน 7 วัน
- ❌ ครูช่าง Mode เต็ม
- ❌ Download ไฟล์

**ฟรีตลอดไป**
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_vip:
            st.markdown('<div class="vip-card">', unsafe_allow_html=True)
            st.markdown("### 👑 VIP Member")
            st.markdown("""
- ✅ ทุกอย่างใน Free
- ✅ **🛒 Shopee Affiliate Engine**
- ✅ **📅 แผน Content 7 วัน**
- ✅ **🔧 ครูช่าง Mode เต็ม**
- ✅ **💾 Download ทุกไฟล์**
- ✅ Priority Support
- ✅ อัปเดตฟีเจอร์ก่อนใคร

**299 บาท / เดือน**
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 💳 ชำระเงิน & รับโค้ด VIP")

        col_pay, col_code = st.columns(2)

        with col_pay:
            st.markdown("""
**PromptPay / พร้อมเพย์**
📱 เบอร์: `0XX-XXX-XXXX`
🏦 ธนาคาร: กรุงไทย / ไทยพาณิชย์

หลังโอน → ส่งสลิปที่ Line: **@chomsuk**
จะได้รับโค้ดภายใน 15 นาที ⚡
            """)

        with col_code:
            st.markdown("**มีโค้ดแล้ว? ใส่ได้เลย:**")
            vip_input = st.text_input("รหัส VIP:", placeholder="XXXX-XXXX",
                                      label_visibility="collapsed")
            if st.button("🔓 ปลดล็อก VIP", type="primary", use_container_width=True):
                # โค้ดจาก Streamlit Secrets (ถ้ามี) หรือ hardcode สำรอง
                valid = {"KRUTON2026", "CHOMSUK01", "VIP2026", "WELD2026"}
                try:
                    extra = set(st.secrets.get("VIP_CODES", "").split(","))
                    valid |= {c.strip().upper() for c in extra if c.strip()}
                except Exception:
                    pass

                if vip_input.upper() in valid:
                    st.session_state.vip_unlocked = True
                    st.balloons()
                    st.success("🎉 ยินดีต้อนรับสู่ VIP!")
                    st.rerun()
                elif not vip_input:
                    st.warning("กรุณาใส่โค้ดก่อนนะครับ")
                else:
                    st.error("❌ โค้ดไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง")
