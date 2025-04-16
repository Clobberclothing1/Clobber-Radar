import streamlit as st
from vinted_pricing import vinted_price_stats
from trend_scraper import vinted_trending
from brand_detect import detect_brand
import tracker

# ---------- Page config ----------
st.set_page_config(page_title="Resale Radar – Vinted", layout="centered")
st.title("Resale Radar · Vinted Valuer")

# ---------- Item Valuer ----------
st.header("📸 Item Valuer (Vinted)")

uploaded = st.file_uploader("Upload a photo of the item", type=["jpg", "jpeg", "png"])
if uploaded:
    # (Optional) basic brand/logo guess – returns an empty string until you plug in a model
    brand_guess = detect_brand(uploaded)
else:
    brand_guess = ""

query = st.text_input("Search keywords (brand + item)", value=brand_guess)

if st.button("Get Vinted price range"):
    if not query.strip():
        st.warning("Enter some keywords first.")
    else:
        stats = vinted_price_stats(query)
        if stats["count"] == 0:
            st.warning("No listings found for that search.")
        else:
            st.markdown(
                f"**Price range (active Vinted listings):** £{stats['low']} – £{stats['high']}  \n"
                f"Median: **£{stats['median']}**  ·  Count: **{stats['count']}**"
            )

# ---------- Trending ----------
st.header("🔥 Trending on Vinted")
if st.button("Refresh trending list"):
    st.write(vinted_trending())

# ---------- Profit Tracker ----------
st.header("💰 Profit Tracker")

with st.form("log_form"):
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("Item description")
        bought = st.number_input("Bought for (£)", min_value=0.0, step=0.10)
    with col2:
        sold = st.number_input("Sold for (£)", min_value=0.0, step=0.10)
        platform = st.selectbox("Platform", ["Vinted"])
    submitted = st.form_submit_button("Log sale")
    if submitted:
        tracker.log_sale(item, bought, sold, platform)
        st.success("Sale logged!")

st.subheader("📈 Profit history")
st.dataframe(tracker.get_log())
