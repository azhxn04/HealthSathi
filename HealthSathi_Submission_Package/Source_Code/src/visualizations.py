"""
HealthSathi - Interactive Data Visualizations
Generates publication-quality Plotly figures for the wellness dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional


COLOR_PRIMARY = "#1e5128"
COLOR_ACCENT = "#d4a373"
COLOR_GOLD = "#e9c46a"
COLOR_TEAL = "#2a9d8f"
COLOR_RED = "#e76f51"
COLOR_TEXT = "#264653"


def create_wellness_gauge(score: float, band_name: str = "", band_color: Optional[str] = None) -> go.Figure:
    if band_color is None or not band_color:
        if score >= 85:
            band_color = COLOR_PRIMARY
            band_name = band_name or "Optimal Equilibrium (Sama Swasthya)"
        elif score >= 70:
            band_color = COLOR_TEAL
            band_name = band_name or "Moderate Balance (Madhyama Vihara)"
        elif score >= 55:
            band_color = COLOR_GOLD
            band_name = band_name or "Mild Imbalance (Kinchit Vishama)"
        else:
            band_color = COLOR_RED
            band_name = band_name or "Needs Attention (Hina Vihara)"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": " / 100", "font": {"size": 36, "color": band_color, "family": "Inter, sans-serif"}},
        title={"text": f"<b>Lifestyle Wellness Score</b><br><span style='font-size:14px;color:#555;'>{band_name}</span>", "font": {"size": 20, "color": COLOR_TEXT}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#888", "tickfont": {"size": 12}},
            "bar": {"color": band_color, "thickness": 0.28},
            "bgcolor": "#f0f2f0",
            "borderwidth": 1,
            "bordercolor": "#ccc",
            "steps": [
                {"range": [0, 55], "color": "rgba(231, 111, 81, 0.22)"},
                {"range": [55, 70], "color": "rgba(233, 196, 106, 0.22)"},
                {"range": [70, 85], "color": "rgba(42, 157, 143, 0.22)"},
                {"range": [85, 100], "color": "rgba(30, 81, 40, 0.25)"}
            ],
            "threshold": {
                "line": {"color": "#333", "width": 3},
                "thickness": 0.75,
                "value": score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(l=25, r=25, t=50, b=10),
        font={"family": "Inter, sans-serif"}
    )
    return fig


def create_sleep_reference_chart(duration_hrs: float) -> go.Figure:
    fig = go.Figure()

    fig.add_vrect(
        x0=7.0, x1=8.5,
        fillcolor="rgba(42, 157, 143, 0.20)",
        layer="below",
        line_width=1,
        line_color="rgba(42, 157, 143, 0.5)",
        annotation_text="Optimal Restorative Range (7.0 - 8.5 hrs)",
        annotation_position="top left",
        annotation_font=dict(size=11, color=COLOR_TEAL)
    )

    bar_color = COLOR_TEAL if (7.0 <= duration_hrs <= 8.5) else (COLOR_GOLD if (6.0 <= duration_hrs < 7.0 or 8.5 < duration_hrs <= 9.5) else COLOR_RED)
    
    fig.add_trace(go.Bar(
        y=["Your Sleep"],
        x=[duration_hrs],
        orientation="h",
        marker=dict(color=bar_color, line=dict(color="#222", width=1.2), opacity=0.85),
        text=f"{duration_hrs:.1f} hrs",
        textposition="inside",
        textfont=dict(size=14, color="#fff", family="Inter, sans-serif"),
        hoverinfo="text",
        hovertext=f"Reported Sleep: {duration_hrs:.1f} hours"
    ))

    fig.update_layout(
        title={"text": "<b>Sleep Duration vs Lifestyle Reference</b>", "font": {"size": 16, "color": COLOR_TEXT}},
        xaxis=dict(range=[0, 12], title="Sleep Duration (Hours)", tickmode="linear", tick0=0, dtick=1, gridcolor="#eee"),
        yaxis=dict(showticklabels=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=180,
        margin=dict(l=20, r=20, t=40, b=30),
        font={"family": "Inter, sans-serif"}
    )
    return fig


def create_stress_trend_chart(current_stress: int, history_data: Optional[List[int]] = None) -> go.Figure:
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    if history_data and len(history_data) == 7:
        stress_vals = history_data
    else:
        c = current_stress
        stress_vals = [
            min(10, max(1, c + 1)),
            min(10, max(1, c + 1)),
            min(10, max(1, c)),
            min(10, max(1, c - 1)),
            min(10, max(1, c)),
            min(10, max(1, c - 2)),
            min(10, max(1, c - 2))
        ]

    fig = go.Figure()
    fig.add_hrect(y0=1, y1=4, fillcolor="rgba(42, 157, 143, 0.12)", layer="below", line_width=0, annotation_text="Tranquil Zone (Sattva)", annotation_position="bottom right", annotation_font=dict(size=10, color=COLOR_TEAL))
    fig.add_hrect(y0=7, y1=10, fillcolor="rgba(231, 111, 81, 0.12)", layer="below", line_width=0, annotation_text="High Tension Zone (Rajas/Vata)", annotation_position="top right", annotation_font=dict(size=10, color=COLOR_RED))

    fig.add_trace(go.Scatter(
        x=days, y=stress_vals, mode="lines+markers+text",
        line=dict(color="#e76f51", width=3, shape="spline"),
        marker=dict(size=9, color="#b23a22", line=dict(width=2, color="#fff")),
        text=[f"{v}" for v in stress_vals], textposition="top center", textfont=dict(size=11, color=COLOR_TEXT),
        name="Daily Stress (1-10)"
    ))

    fig.update_layout(
        title={"text": "<b>Weekly Stress Dynamics (1-10 Scale)</b>", "font": {"size": 16, "color": COLOR_TEXT}},
        yaxis=dict(range=[0.5, 10.5], title="Reported Tension Level", tickvals=list(range(1, 11)), gridcolor="#eee"),
        xaxis=dict(title="Day of Week", gridcolor="#eee"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=25, r=25, t=45, b=35),
        showlegend=False,
        font={"family": "Inter, sans-serif"}
    )
    return fig


def create_activity_chart(physical_activity_min: float, outdoor_time_min: float) -> go.Figure:
    categories = ["Physical Activity", "Outdoor Sunlight"]
    actual_vals = [physical_activity_min, outdoor_time_min]
    target_vals = [45.0, 30.0]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories, y=actual_vals, name="Reported Daily",
        marker=dict(color=COLOR_TEAL, opacity=0.85, line=dict(color="#1f7a6f", width=1.2)),
        text=[f"{v:.0f} min" for v in actual_vals], textposition="inside", textfont=dict(color="#fff", size=13)
    ))
    fig.add_trace(go.Bar(
        x=categories, y=target_vals, name="Wellness Guideline",
        marker=dict(color="rgba(212, 163, 115, 0.45)", line=dict(color=COLOR_ACCENT, width=1.5)),
        text=[f"{v:.0f} min" for v in target_vals], textposition="outside", textfont=dict(color="#555", size=11)
    ))

    fig.update_layout(
        title={"text": "<b>Movement & Sunlight Minutes vs Guideline</b>", "font": {"size": 16, "color": COLOR_TEXT}},
        barmode="group",
        yaxis=dict(title="Minutes per Day", gridcolor="#eee"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=25, r=25, t=45, b=35),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font={"family": "Inter, sans-serif"}
    )
    return fig


def create_lifestyle_radar_chart(scores: Dict[str, float]) -> go.Figure:
    categories = [
        "Sleep Quality<br>& Duration", "Physical<br>Activity", "Nutrition<br>& Diet",
        "Hydration<br>Balance", "Stress<br>Management", "Routine<br>Consistency"
    ]
    values = [
        scores.get("sleep_score", 60.0), scores.get("activity_score", 60.0),
        scores.get("nutrition_score", 60.0), scores.get("hydration_score", 60.0),
        scores.get("stress_score", 60.0), scores.get("routine_score", 60.0),
    ]

    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    benchmark_vals = [80.0] * len(categories_closed)
    fig.add_trace(go.Scatterpolar(
        r=benchmark_vals, theta=categories_closed, fill=None, mode="lines",
        line=dict(color="rgba(150, 150, 150, 0.4)", width=1.5, dash="dash"),
        name="Target Balanced Frontier (80+)"
    ))

    fig.add_trace(go.Scatterpolar(
        r=values_closed, theta=categories_closed, fill="toself",
        fillcolor="rgba(30, 81, 40, 0.28)", mode="lines+markers",
        line=dict(color=COLOR_PRIMARY, width=2.8), marker=dict(size=7, color=COLOR_PRIMARY),
        name="Your Lifestyle Dimensions"
    ))

    fig.update_layout(
        title={"text": "<b>Lifestyle Hexagonal Wellness Radar</b>", "font": {"size": 17, "color": COLOR_TEXT}},
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickvals=[20, 40, 60, 80, 100], tickfont=dict(size=10, color="#666"), gridcolor="#e0e0e0"),
            angularaxis=dict(tickfont=dict(size=11, color=COLOR_TEXT, family="Inter, sans-serif"), rotation=90, direction="clockwise", gridcolor="#e0e0e0"),
            bgcolor="rgba(255, 255, 255, 0.7)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        height=340,
        margin=dict(l=35, r=35, t=50, b=25),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
        font={"family": "Inter, sans-serif"}
    )
    return fig


def create_weekly_comparison_chart(current_scores: Dict[str, float]) -> go.Figure:
    dimensions = ["Sleep Score", "Activity Score", "Stress Mgmt", "Overall Wellness"]
    cur_vals = [
        current_scores.get("sleep_score", 65.0), current_scores.get("activity_score", 50.0),
        current_scores.get("stress_score", 55.0), current_scores.get("overall_wellness_score", 60.0)
    ]
    prev_vals = [
        round(max(15.0, min(95.0, cur_vals[0] - 6.0 + (cur_vals[0] % 5))), 1),
        round(max(15.0, min(95.0, cur_vals[1] - 8.0 + (cur_vals[1] % 7))), 1),
        round(max(15.0, min(95.0, cur_vals[2] - 5.0 + (cur_vals[2] % 4))), 1),
        round(max(15.0, min(95.0, cur_vals[3] - 6.0 + (cur_vals[3] % 6))), 1)
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=dimensions, y=prev_vals, name="Previous Week", marker=dict(color="#cbd5e1", line=dict(color="#94a3b8", width=1.2)), text=[f"{v:.0f}" for v in prev_vals], textposition="inside", textfont=dict(color="#334155", size=12)))
    fig.add_trace(go.Bar(x=dimensions, y=cur_vals, name="Current Week", marker=dict(color=COLOR_PRIMARY, line=dict(color="#0f3014", width=1.2)), text=[f"{v:.0f}" for v in cur_vals], textposition="inside", textfont=dict(color="#ffffff", size=12)))

    fig.update_layout(
        title={"text": "<b>Weekly Trajectory: Current vs Previous Week</b>", "font": {"size": 16, "color": COLOR_TEXT}},
        barmode="group",
        yaxis=dict(range=[0, 105], title="Score (0-100)", gridcolor="#eee"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=25, r=25, t=45, b=35),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font={"family": "Inter, sans-serif"}
    )
    return fig
