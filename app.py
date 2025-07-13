import os, json, datetime
from pathlib import Path
import streamlit as st
from PIL import Image

# --------------- Constants ---------------- #
DATA_DIR = Path(__file__).parent / "data"
POSTER_DIR = DATA_DIR / "posters"
DATA_FILE = DATA_DIR / "data.json"

# --------------- Initial Setup ------------ #
def init_storage():
    DATA_DIR.mkdir(exist_ok=True)
    POSTER_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"posters": [], "programs": []}, f, ensure_ascii=False, indent=2)

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

init_storage()
data = load_data()

# --------------- Page Config -------------- #
st.set_page_config(page_title="SSF Mavoor Unit", page_icon="🌟", layout="wide")

st.title("SSF Mavoor Unit – Admin & Showcase")
st.caption("All‑in‑one web app to manage posters, programs, and winners")

# --------------- Sidebar Nav -------------- #
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Add Poster", "Posters Gallery", "Add Program & Winners", "Programs & Winners"],
    index=0,
)

# --------------- Home --------------------- #
if page == "Home":
    st.header("Welcome to SSF Mavoor Unit Portal")
    st.markdown(
        """Use the sidebar to add new posters, enter program details, or view existing items.
        * **Add Poster** – Upload event posters (image files).
        * **Posters Gallery** – Browse all uploaded posters.
        * **Add Program & Winners** – Record program details and winners.
        * **Programs & Winners** – View previously entered winners."""
    )
    st.success("Select an option from the sidebar to begin.")

# --------------- Add Poster --------------- #
elif page == "Add Poster":
    st.header("Upload a New Poster")
    poster_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg", "gif"])
    caption = st.text_input("Caption / Description")
    if st.button("Save Poster") and poster_file:
        # Save image to POSTER_DIR with unique name
        ext = poster_file.name.split(".")[-1]
        poster_bytes = poster_file.read()
        filename = f"poster_{hash(poster_bytes) & 0xffffffff}.{ext}"
        file_path = POSTER_DIR / filename
        with open(file_path, "wb") as f:
            f.write(poster_bytes)
        # Update data
        entry = {
            "file": file_path.name,
            "caption": caption,
            "date": datetime.date.today().isoformat(),
        }
        data["posters"].append(entry)
        save_data(data)
        st.success("Poster saved successfully!")

# --------------- Posters Gallery ---------- #
elif page == "Posters Gallery":
    st.header("All Posters")
    cols = st.columns(3)
    if not data["posters"]:
        st.info("No posters uploaded yet.")
    else:
        for idx, poster in enumerate(reversed(data["posters"])):
            col = cols[idx % 3]
            with col:
                img_path = POSTER_DIR / poster["file"]
                if img_path.exists():
                    st.image(str(img_path), caption=poster["caption"], use_column_width=True)
                st.caption(poster["date"])

# --------------- Add Program & Winners ---- #
elif page == "Add Program & Winners":
    st.header("Add Program Details & Winners")
    name = st.text_input("Program Name")
    date = st.date_input("Program Date", datetime.date.today())
    winners = st.text_area("Winners (one per line)")
    if st.button("Save Program"):
        if name.strip() and winners.strip():
            entry = {
                "name": name.strip(),
                "date": date.isoformat(),
                "winners": [w.strip() for w in winners.splitlines() if w.strip()],
            }
            data["programs"].append(entry)
            save_data(data)
            st.success("Program and winners saved!")
        else:
            st.error("Program name and winners are required.")

# --------------- Programs & Winners ------- #
elif page == "Programs & Winners":
    st.header("Programs & Winners")
    if not data["programs"]:
        st.info("No programs recorded yet.")
    else:
        for prog in reversed(data["programs"]):
            with st.expander(f"{prog['name']}  —  {prog['date']}"):
                st.subheader("Winners")
                for idx, winner in enumerate(prog["winners"], 1):
                    st.write(f"{idx}. {winner}")

# --------------- Footer ------------------- #
st.markdown("---")
st.caption("© 2025 SSF Mavoor Unit")
