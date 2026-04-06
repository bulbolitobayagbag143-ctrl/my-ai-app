import streamlit as st
import trafilatura
from google import genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="ViralContent AI", page_icon="🚀", layout="centered")

# --- CUSTOM STYLING (Dark Mode Aesthetic) ---
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: white; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        background-color: #4f46e5; 
        color: white; 
        height: 3.5em;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_input=True)

# --- SIDEBAR (Settings) ---
with st.sidebar:
    st.title("⚙️ Setup")
    st.write("To get started, enter your Gemini API Key below.")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste key here...")
    st.markdown("---")
    st.markdown("### 💰 Monetization")
    st.write("Current Plan: **Free Tier**")
    if st.button("Upgrade to Pro (Stripe)"):
        st.info("Redirecting to payment gateway...")

# --- MAIN INTERFACE ---
st.title("🚀 ViralContent AI")
st.subheader("Turn 1 Article into 10 Social Posts in 30 Seconds.")

url = st.text_input("Paste a blog post or article URL:", placeholder="https://example.com/your-article")

# Options for the AI
platform = st.selectbox("Select Target Platform:", 
    ["Twitter (X) Thread", "LinkedIn Professional Post", "Instagram Educational Slide Script", "TikTok Script"])

if st.button("Generate Viral Content ✨"):
    if not api_key:
        st.error("❌ Please enter your API key in the sidebar first!")
    elif not url:
        st.warning("⚠️ Please provide a valid URL.")
    else:
        with st.spinner("🤖 AI is reading the article and writing your posts..."):
            try:
                # 1. Extract Content from URL
                downloaded = trafilatura.fetch_url(url)
                article_text = trafilatura.extract(downloaded)
                
                if article_text:
                    # 2. Setup AI Client
                    client = genai.Client(api_key=api_key)
                    
                    # 3. Create the Prompt
                    prompt = f"""
                    Act as a world-class social media manager. 
                    Below is an article. Transform it into a high-engagement {platform}.
                    
                    Instructions:
                    - Use a 'hook' that stops the scroll.
                    - Use emojis and bullet points for readability.
                    - Maintain a professional yet exciting tone.
                    - End with a call to action (CTA).

                    ARTICLE TEXT:
                    {article_text}
                    """
                    
                    # 4. Generate Content
                    response = client.models.generate_content(
                        model="gemini-2.0-flash", 
                        contents=prompt
                    )
                    
                    # 5. Display Result
                    st.markdown("---")
                    st.success("🔥 Your content is ready!")
                    st.markdown(response.text)
                    st.button("📋 Copy Results")
                else:
                    st.error("❌ We couldn't find any text on that page. Please try a different link.")
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")

# --- FOOTER ---
st.markdown("---")
st.caption("Built for Passive Income Creators. Powered by Gemini 2.0.")
