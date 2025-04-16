import streamlit as st
from brand_detect import detect_brand
from vinted_pricing import vinted_price_stats
from trend_scraper import vinted_trending
import tracker

st.set_page_config(page_title="Resale Radar", layout="wide")

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.title("🛰️ Resale Radar")
page = st.sidebar.radio(
    "Go to",
    ["Item Valuer", "Trending", "Profit Tracker"],
    label_visibility="collapsed",
)

# ── 1 · Item Valuer ───────────────────────────────────────────────────────────
if page == "Item Valuer":
    st.header("📸 Item Valuer (Vinted)")

    up = st.file_uploader("Upload a photo (optional)", type=["jpg", "jpeg", "png"])
    guess = detect_brand(up) if up else ""
    query = st.text_input("Brand + item keywords", value=guess, placeholder="e.g. Ralph Lauren jumper")

    if st.button("Get price range", use_container_width=True):
        if not query.strip():
            st.warning("Please enter a few keywords.")
        else:
            stats = vinted_price_stats(query)
            if stats["count"] == 0:
                st.error("No listings found — try a broader search.")
            else:
                st.success(
                    f"Low: **£{stats['low']}**  ·  Median: **£{stats['median']}**  ·  High: **£{stats['high']}**"
                )
                st.caption(f"Based on {stats['count']} active listings")

# ── 2 · Trending ─────────────────────────────────────────────────────────────
elif page == "Trending":
    st.header("🔥 Trending on Vinted")
    trends = vinted_trending()
    if trends.empty:
        st.error("Couldn’t fetch trends right now — try again later.")
    else:
        st.write("Top 20 trending brands / tags right now:")
        st.table(trends.to_frame())

# ── 3 · Profit Tracker ────────────────────────────────────────────────────────
else:
    st.header("💰 Profit Tracker")
    with st.form("log"):
        col1, col2, col3 = st.columns(3)
        item   = col1.text_input("Item")
        bought = col2.number_input("Bought £", min_value=0.0, step=0.10)
        sold   = col3.number_input("Sold £",  min_value=0.0, step=0.10)
        if st.form_submit_button("Add flip", use_container_width=True):
            tracker.log_sale(item, bought, sold, "Vinted")
            st.success("Flip added!")

    st.subheader("History")
    st.dataframe(tracker.get_log(), use_container_width=True)

    st.subheader("📊 Monthly summary")
    st.dataframe(tracker.monthly_summary(), use_container_width=True)
