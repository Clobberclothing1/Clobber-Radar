import streamlit as st
from brand_detect import detect_brand
from vinted_pricing import vinted_price_stats
from trend_scraper import vinted_trending
import tracker

# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Resale Radar · Vinted", layout="centered")
st.title("Resale Radar · Vinted Valuer")

# ── 1 · Item Valuer ───────────────────────────────────────────────────────────
st.header("📸 Item Valuer")

uploaded = st.file_uploader("Upload a photo (optional)", type=["jpg", "jpeg", "png"])
brand_guess = detect_brand(uploaded) if uploaded else ""
query = st.text_input("Search keywords (brand + item)", value=brand_guess)

if st.button("Get Vinted price range"):
    if not query.strip():
        st.warning("Enter some keywords first.")
    else:
        stats = vinted_price_stats(query)
        if stats["count"] == 0:
            st.warning("No listings found for that search.")
        else:
            st.markdown(
                f"**Price range:** £{stats['low']} – £{stats['high']}  \n"
                f"Median: **£{stats['median']}**  · Listings: **{stats['count']}**"
            )

# ── 2 · Trending ─────────────────────────────────────────────────────────────
st.header("🔥 Trending on Vinted")
if st.button("Refresh trending list"):
    st.write(vinted_trending())

# ── 3 · Profit Tracker ────────────────────────────────────────────────────────
st.header("💰 Profit Tracker")

with st.form("log_form"):
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("Item description")
        bought = st.number_input("Bought for (£)", min_value=0.0, step=0.10)
    with col2:
        sold = st.number_input("Sold for (£)", min_value=0.0, step=0.10)
        platform = "Vinted"
    if st.form_submit_button("Log sale"):
        tracker.log_sale(item, bought, sold, platform)
        st.success("Sale logged!")

st.subheader("📈 Profit history")
st.dataframe(tracker.get_log(), use_container_width=True)

# Optional monthly summary (uncomment if you want to show)
# with st.expander("📊 Monthly profit summary"):
#     st.dataframe(tracker.monthly_summary(), use_container_width=True)
