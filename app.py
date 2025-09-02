import streamlit as st

# --- Unit tables ---
UNITS = {
    "Length": {
        "m": 1.0,
        "cm": 0.01,
        "mm": 0.001,
        "km": 1000.0,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mile": 1609.344,
    },
    "Mass": {
        "kg": 1.0,
        "g": 0.001,
        "mg": 1e-6,
        "lb": 0.45359237,
        "oz": 0.0283495,
        "tonne": 1000.0,
    },
    "Temperature": {"C": None, "F": None, "K": None},
    "Area": {
        "m²": 1.0,
        "cm²": 0.0001,
        "mm²": 1e-6,
        "km²": 1e6,
        "in²": 0.00064516,
        "ft²": 0.092903,
        "yd²": 0.836127,
        "acre": 4046.86,
        "hectare": 10000.0,
    },
    "Volume": {
        "m³": 1.0,
        "cm³": 1e-6,
        "mm³": 1e-9,
        "L": 0.001,
        "mL": 1e-6,
        "in³": 1.6387e-5,
        "ft³": 0.0283168,
        "yd³": 0.764555,
        "gal (US)": 0.00378541,
    },
    "Amount of Substance": {
        "mol": 1.0,
        "mmol": 0.001,
        "kmol": 1000.0,
    },
}

# --- Temperature helpers ---
def temp_to_celsius(value, unit):
    if unit == "C": return value
    if unit == "F": return (value - 32) * 5/9
    if unit == "K": return value - 273.15

def celsius_to_target(value_c, unit):
    if unit == "C": return value_c
    if unit == "F": return value_c * 9/5 + 32
    if unit == "K": return value_c + 273.15

# --- Conversion ---
def convert(value, from_unit, to_unit, category, decimals):
    try:
        v = float(value)
    except Exception:
        return "❗ Please enter a valid number."

    if category == "Temperature":
        v_c = temp_to_celsius(v, from_unit)
        result = celsius_to_target(v_c, to_unit)
    else:
        base = v * UNITS[category][from_unit]
        result = base / UNITS[category][to_unit]

    return f"{v} {from_unit} = {result:.{decimals}f} {to_unit}"

# --- Page config ---
st.set_page_config(page_title="🌐 Unique Unit Converter", layout="centered")

# --- Custom CSS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
h1 {
    text-align: center;
    color: #ffcc70;
    text-shadow: 0px 0px 10px rgba(255,200,100,0.8);
}
.stSelectbox label, .stNumberInput label, .stSlider label, .stTextInput label {
    font-weight: bold !important;
    color: #ffcc70 !important;
}
.result-box {
    margin-top: 20px;
    padding: 15px;
    border-radius: 10px;
    background: rgba(255,255,255,0.1);
    text-align: center;
    font-size: 18px;
    font-weight: bold;
}
/* Orange button style */
div.stButton > button:first-child {
    background-color: #ff7b00;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    padding: 0.6em 1.2em;
    transition: 0.3s;
}
div.stButton > button:first-child:hover {
    background-color: #ff9f40;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1>🌐 Unique Unit Converter</h1>", unsafe_allow_html=True)

# --- Session state ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Inputs ---
category = st.selectbox("Select category", list(UNITS.keys()))
units = list(UNITS[category].keys())
value = st.text_input("Enter value", "1")
col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From", units)
with col2:
    to_unit = st.selectbox("To", units)

decimals = st.slider("Decimal places", 0, 8, 4)

# --- Buttons ---
colA, colB = st.columns(2)
with colA:
    if st.button("Convert 🚀"):
        result = convert(value, from_unit, to_unit, category, decimals)
        st.markdown(f"<div class='result-box'>{result}</div>", unsafe_allow_html=True)
        if "❗" not in result:  # only store valid results
            st.session_state.history.insert(0, result)

with colB:
    if st.button("Reset 🔄"):
        st.session_state.history.clear()
        st.rerun()

# --- History Panel ---
if st.session_state.history:
    st.subheader("📜 Conversion History")
    for item in st.session_state.history[:5]:  # show last 5
        st.write(item)

# --- Tiny JS Sparkle ---
st.markdown("""
<script>
document.body.addEventListener("click", function(e) {
    let spark = document.createElement("span");
    spark.innerHTML = "✨";
    spark.style.position = "absolute";
    spark.style.left = e.pageX + "px";
    spark.style.top = e.pageY + "px";
    spark.style.fontSize = "20px";
    document.body.appendChild(spark);
    setTimeout(()=> spark.remove(), 600);
});
</script>
""", unsafe_allow_html=True)


