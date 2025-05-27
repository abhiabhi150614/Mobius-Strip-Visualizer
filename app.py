import streamlit as st
import plotly.graph_objects as go
import numpy as np
from mobius import MobiusStrip

# App config
st.set_page_config(page_title="Mobius Strip Visualizer", layout="wide", initial_sidebar_state="expanded")

st.title("Mobius Strip Explorer")

# Sidebar controls
st.sidebar.header("Adjust Parameters")
R = st.sidebar.slider("Radius (R)", 0.5, 2.0, 1.0, 0.1)
w = st.sidebar.slider("Width (w)", 0.1, 1.0, 0.3, 0.05)
n = st.sidebar.slider("Resolution (n)", 100, 500, 300, 50)

# Style controls
st.sidebar.header("Display Settings")
color_map = st.sidebar.selectbox("Color Map", ["Viridis", "Blues", "Cividis", "Plasma", "Inferno"])
show_grid = st.sidebar.checkbox("Show Grid", value=True)  # Default True
auto_rotate = st.sidebar.checkbox("Auto Rotate", value=False)
light_mode = st.sidebar.toggle("Light Theme")

# Generate strip
strip = MobiusStrip(R=R, w=w, n=n)
x, y, z = strip.get_surface()

# Plotly surface
surface = go.Surface(x=x, y=y, z=z, colorscale=color_map, opacity=0.95, showscale=False)

# Base layout
layout = go.Layout(
    title="Mobius Strip",
    margin=dict(l=0, r=0, t=40, b=0),
    scene=dict(
        xaxis=dict(visible=show_grid),
        yaxis=dict(visible=show_grid),
        zaxis=dict(visible=show_grid),
        aspectmode='auto'
    ),
    paper_bgcolor='white' if light_mode else 'black',
    font_color='black' if light_mode else 'white',
)

if auto_rotate:
    # Create animation frames rotating camera around the strip
    frames = []
    steps = 60  # frames for full rotation
    for i in range(steps):
        angle = i * 360 / steps
        camera = dict(
            eye=dict(
                x=1.5 * np.cos(np.radians(angle)),
                y=1.5 * np.sin(np.radians(angle)),
                z=0.6
            )
        )
        frames.append(go.Frame(layout=dict(scene_camera=camera)))

    layout.updatemenus = [
        dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None,
                                dict(frame=dict(duration=50, redraw=True),
                                     fromcurrent=True,
                                     transition=dict(duration=0),
                                     mode="immediate",
                                     loop=True
                                )
                          ])],
            x=0.1,
            y=0,
            xanchor="right",
            yanchor="top"
        )
    ]

    fig = go.Figure(data=[surface], layout=layout, frames=frames)
else:
    fig = go.Figure(data=[surface], layout=layout)

st.plotly_chart(fig, use_container_width=True)

# Geometry info
st.subheader("Geometric Properties")
col1, col2 = st.columns(2)
col1.metric("Surface Area", f"{strip.surface_area():.4f} units²")
col2.metric("Edge Length", f"{strip.edge_length():.4f} units")

# Generate .obj file for download
filename = "mobius_strip.obj"
with open(filename, "w") as f:
    for i in range(n):
        for j in range(n):
            f.write(f"v {x[i][j]} {y[i][j]} {z[i][j]}\n")
    for i in range(n - 1):
        for j in range(n - 1):
            v1 = i * n + j + 1
            v2 = i * n + j + 2
            v3 = (i + 1) * n + j + 2
            v4 = (i + 1) * n + j + 1
            f.write(f"f {v1} {v2} {v3}\n")
            f.write(f"f {v1} {v3} {v4}\n")

with open(filename, "rb") as f:
    st.download_button("Download .obj file", f, filename)
