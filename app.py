
import streamlit as st
from vinted_pricing import vinted_price_stats
from trend_scraper import vinted_trending
from brand_detect import detect_brand
import tracker

st.set_page_config(page_title="Resale Radar – Vinted", layout="centered")
st.title("Resale Radar – Vinted Valuer")

st.header("📸 Item Valuer (Vinted)")
uploaded = st.file_uploader("Upload a photo of the item", type=["jpg","jpeg","png"])
if uploaded:
    brand_guess = detect_brand(uploaded)
    query = st.text_input("Search keywords (brand / item)", value=brand_guess)
    if st.button("Get Vinted price range"):
        if query:
            stats = vinted_price_stats(query)
            if stats['count']==0:
                st.warning("No listings found for that query.")
            else:
                st.markdown(f"**Price range (active listings):** £{stats['low']} – £{stats['high']}  
Median: **£{stats['median']}** (across {stats['count']} listings)")
        else:
            st.warning("Enter some keywords first.")

st.header("🔥 Trending on Vinted")
if st.button("Refresh trending list"):
    tags = vinted_trending()
    st.write(tags)

st.header("💰 Profit Tracker")
with st.form("log_form"):
    col1,col2 = st.columns(2)
    with col1:
        item = st.text_input("Item description")
        bought = st.number_input("Bought for (£)", min_value=0.0, step=0.1)
    with col2:
        sold = st.number_input("Sold for (£)", min_value=0.0, step=0.1)
        platform = st.selectbox("Platform", ["Vinted"])
    submitted = st.form_submit_button("Log sale")
    if submitted:
        tracker.log_sale(item,bought,sold,platform)
        st.success("Sale logged!")

st.subheader("📈 Profit history")
df = tracker.get_log()
st.dataframe(df)
