import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Title
st.title("Student A - Performance Analysis")

# Create DataFrames for each subject
physics_data = pd.DataFrame([
    {"chapter": "Kinematics", "marks": 4, "max_marks": 4},
    {"chapter": "Laws of Motion", "marks": 3, "max_marks": 4},
    {"chapter": "Work, Energy and Power", "marks": 2, "max_marks": 4},
    {"chapter": "Gravitation", "marks": 4, "max_marks": 4},
    {"chapter": "Oscillations", "marks": 1, "max_marks": 4}
])

chemistry_data = pd.DataFrame([
    {"chapter": "Atomic Structure", "marks": 4, "max_marks": 4},
    {"chapter": "Chemical Bonding", "marks": 2, "max_marks": 4},
    {"chapter": "Thermodynamics", "marks": 3, "max_marks": 4},
    {"chapter": "Equilibrium", "marks": 4, "max_marks": 4},
    {"chapter": "Redox Reactions", "marks": 1, "max_marks": 4}
])

math_data = pd.DataFrame([
    {"chapter": "Quadratic Equations", "marks": 3, "max_marks": 4},
    {"chapter": "Matrices", "marks": 2, "max_marks": 4},
    {"chapter": "Determinants", "marks": 4, "max_marks": 4},
    {"chapter": "Probability", "marks": 1, "max_marks": 4},
    {"chapter": "Trigonometry", "marks": 4, "max_marks": 4}
])

# Calculate total scores
total_scores = pd.DataFrame([
    {"subject": "Physics", "obtained": physics_data["marks"].sum(), "total": len(physics_data) * 4},
    {"subject": "Chemistry", "obtained": chemistry_data["marks"].sum(), "total": len(chemistry_data) * 4},
    {"subject": "Mathematics", "obtained": math_data["marks"].sum(), "total": len(math_data) * 4}
])

# Calculate percentages
total_scores["percentage"] = (total_scores["obtained"] / total_scores["total"]) * 100

# Create layout with columns
col1, col2 = st.columns(2)

# Subject-wise Performance Bar Chart
with col1:
    st.subheader("Subject-wise Scores")
    fig_scores = go.Figure(data=[
        go.Bar(name='Marks Obtained', x=total_scores['subject'], y=total_scores['obtained'],
               marker_color='#0088FE'),
        go.Bar(name='Total Marks', x=total_scores['subject'], y=total_scores['total'],
               marker_color='#00C49F')
    ])
    fig_scores.update_layout(barmode='group', height=400)
    st.plotly_chart(fig_scores, use_container_width=True)

# Radar Chart for Performance Distribution
with col2:
    st.subheader("Performance Distribution (%)")
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=total_scores['percentage'],
        theta=total_scores['subject'],
        fill='toself',
        name='Score Percentage'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Create three columns for subject-wise chapter performance
col3, col4, col5 = st.columns(3)

# Physics Chapter Performance
with col3:
    st.subheader("Physics Chapter Performance")
    fig_physics = px.bar(physics_data, x='chapter', y='marks',
                        labels={'marks': 'Marks', 'chapter': 'Chapter'},
                        color_discrete_sequence=['#0088FE'])
    fig_physics.update_layout(
        xaxis_tickangle=-45,
        height=400
    )
    st.plotly_chart(fig_physics, use_container_width=True)

# Chemistry Chapter Performance
with col4:
    st.subheader("Chemistry Chapter Performance")
    fig_chemistry = px.bar(chemistry_data, x='chapter', y='marks',
                          labels={'marks': 'Marks', 'chapter': 'Chapter'},
                          color_discrete_sequence=['#00C49F'])
    fig_chemistry.update_layout(
        xaxis_tickangle=-45,
        height=400
    )
    st.plotly_chart(fig_chemistry, use_container_width=True)

# Mathematics Chapter Performance
with col5:
    st.subheader("Mathematics Chapter Performance")
    fig_math = px.bar(math_data, x='chapter', y='marks',
                      labels={'marks': 'Marks', 'chapter': 'Chapter'},
                      color_discrete_sequence=['#FFBB28'])
    fig_math.update_layout(
        xaxis_tickangle=-45,
        height=400
    )
    st.plotly_chart(fig_math, use_container_width=True)

# Add summary statistics
st.subheader("Summary Statistics")
col6, col7, col8 = st.columns(3)

# Physics Summary
with col6:
    st.metric(
        label="Physics Score",
        value=f"{physics_data['marks'].sum()}/{len(physics_data) * 4}",
        delta=f"{(physics_data['marks'].sum() / (len(physics_data) * 4) * 100):.1f}%"
    )

# Chemistry Summary
with col7:
    st.metric(
        label="Chemistry Score",
        value=f"{chemistry_data['marks'].sum()}/{len(chemistry_data) * 4}",
        delta=f"{(chemistry_data['marks'].sum() / (len(chemistry_data) * 4) * 100):.1f}%"
    )

# Mathematics Summary
with col8:
    st.metric(
        label="Mathematics Score",
        value=f"{math_data['marks'].sum()}/{len(math_data) * 4}",
        delta=f"{(math_data['marks'].sum() / (len(math_data) * 4) * 100):.1f}%"
    )
