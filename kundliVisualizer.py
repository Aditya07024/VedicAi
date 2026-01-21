"""
kundliVisualizer.py
-------------------
Pure visualization utilities for Kundli charts.
NO Streamlit code should exist in this file.
"""

import plotly.graph_objects as go
import math


def create_circular_kundli(kundli):
    """
    Create an interactive circular Kundli chart using Plotly.
    Returns a Plotly Figure object.
    """

    fig = go.Figure()

    # Draw 12 house sectors
    for i in range(12):
        start_angle = i * 30
        end_angle = start_angle + 30

        fig.add_trace(go.Barpolar(
            r=[1],
            theta=[start_angle + 15],
            width=[30],
            marker_color="rgba(200,200,200,0.2)",
            marker_line_color="black",
            marker_line_width=1,
            hoverinfo="skip",
            showlegend=False
        ))

    # House labels
    for house in range(1, 13):
        angle = (house - 1) * 30 + 15
        fig.add_annotation(
            x=0.5 + 0.35 * math.cos(math.radians(angle)),
            y=0.5 + 0.35 * math.sin(math.radians(angle)),
            text=f"H{house}",
            showarrow=False
        )

    # Planet placements
    for house, planets in kundli["houses"].items():
        if not planets:
            continue

        angle = (house - 1) * 30 + 15
        planet_text = "<br>".join(p["planet"] for p in planets)

        fig.add_annotation(
            x=0.5 + 0.25 * math.cos(math.radians(angle)),
            y=0.5 + 0.25 * math.sin(math.radians(angle)),
            text=planet_text,
            showarrow=False,
            font=dict(size=10)
        )

    fig.update_layout(
        title=f"Circular Kundli (Lagna: {kundli['lagna']['rashi']})",
        polar=dict(
            radialaxis=dict(visible=False),
            angularaxis=dict(
                visible=False,
                direction="clockwise",
                rotation=90
            )
        ),
        showlegend=False
    )

    return fig