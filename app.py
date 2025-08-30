import gradio as gr
from typing import Tuple

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
        "nmi": 1852.0,   # nautical mile
    },
    "Mass": {
        "kg": 1.0,
        "g": 0.001,
        "mg": 1e-6,
        "lb": 0.45359237,
        "oz": 0.028349523125,
        "tonne": 1000.0,
        "stone": 6.35029318,
    },
    "Volume": {
        "L": 1.0,
        "mL": 0.001,
        "m^3": 1000.0,
        "gal": 3.785411784,
        "qt": 0.946352946,
        "pt": 0.473176473,
        "cup": 0.24,
        "fl oz": 0.0295735295625,
    },
    "Area": {
        "m²": 1.0,
        "cm²": 0.0001,
        "mm²": 1e-6,
        "km²": 1_000_000.0,
        "ft²": 0.092903,
        "in²": 0.00064516,
        "yd²": 0.836127,
        "acre": 4046.8564224,
        "hectare": 10_000.0,
    },
    "Temperature": {
        "C": None,
        "F": None,
        "K": None,
    },
}

# --- Temperature helpers ---
def temp_to_celsius(value: float, unit: str) -> float:
    if unit == "C": return value
    if unit == "F": return (value - 32.0) * 5.0/9.0
    if unit == "K": return value - 273.15
    raise ValueError(f"Unknown unit {unit}")

def celsius_to_target(value_c: float, unit: str) -> float:
    if unit == "C": return value_c
    if unit == "F": return value_c * 9.0/5.0 + 32.0
    if unit == "K": return value_c + 273.15
    raise ValueError(f"Unknown unit {unit}")

# --- Conversion logic ---
def convert_value(value, from_unit: str, to_unit: str, category: str, decimals: int) -> str:
    try:
        v = float(value)
    except Exception:
        return f"❗ Input '{value}' is not a number."

    if category == "Temperature":
        v_c = temp_to_celsius(v, from_unit)
        result = celsius_to_target(v_c, to_unit)
    else:
        units_map = UNITS[category]
        value_in_base = v * units_map[from_unit]
        result = value_in_base / units_map[to_unit]

    return f"{v} {from_unit} = {result:.{int(decimals)}f} {to_unit}"

# --- Helpers ---
def choices_for(category: str) -> list[str]:
    return sorted(list(UNITS[category].keys()))

def update_units(cat: str) -> Tuple[gr.Dropdown, gr.Dropdown]:
    opts = choices_for(cat)
    default_from = opts[0]
    default_to = opts[1] if len(opts) > 1 else opts[0]
    return (
        gr.update(choices=opts, value=default_from),
        gr.update(choices=opts, value=default_to),
    )

def swap(f: str, t: str) -> Tuple[str, str]:
    return t, f

# --- Gradio UI ---
with gr.Blocks(title="Unit Converter") as demo:
    gr.Markdown("## 🌐 Simple Unit Converter)")

    category = gr.Dropdown(choices=list(UNITS.keys()), value="Length", label="Category")

    with gr.Row():
        value_in = gr.Number(value=1, label="Value")
        from_unit = gr.Dropdown(choices=choices_for("Length"), value="m", label="From unit")
        to_unit = gr.Dropdown(choices=choices_for("Length"), value="ft", label="To unit")

    decimals = gr.Slider(0, 10, value=4, step=1, label="Decimal places")

    with gr.Row():
        convert_btn = gr.Button("Convert")
        swap_btn = gr.Button("Swap units")

    output = gr.Textbox(label="Result", interactive=False)

    # Events
    category.change(fn=update_units, inputs=category, outputs=[from_unit, to_unit])
    convert_btn.click(fn=convert_value, inputs=[value_in, from_unit, to_unit, category, decimals], outputs=output)
    swap_btn.click(fn=swap, inputs=[from_unit, to_unit], outputs=[from_unit, to_unit])

# Hugging Face Spaces automatically runs demo.launch()
if __name__ == "__main__":
    demo.launch()

