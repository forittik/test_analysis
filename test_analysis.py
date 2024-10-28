import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Process the data
df = pd.read_csv("https://raw.githubusercontent.com/forittik/test_analysis/refs/heads/main/jee_student_data_75_questions.csv")

# Title
st.title(f"Performance Analysis - {df['student_name'].iloc[0]}")

# Create subject-wise data with handling for NaN values
physics_data = pd.DataFrame({
    'chapter': df['physics_chapters'].unique(),
    'marks': df['Marks_in_physics'].fillna(0).astype(int),  # Fill NaN with 0 and convert to int
    'max_marks': 4
})

chemistry_data = pd.DataFrame({
    'chapter': df['chemistry_chapters'].unique(),
    'marks': df['Marks_in_chemistry'].fillna(0).astype(int),  # Fill NaN with 0 and convert to int
    'max_marks': 4
})

math_data = pd.DataFrame({
    'chapter': df['mathematics_chapters'].unique(),
    'marks': df['Marks_in_mathematics'].fillna(0).astype(int),  # Fill NaN with 0 and convert to int
    'max_marks': 4
})

# Calculate total scores
total_scores = pd.DataFrame([
    {"subject": "Physics", "obtained": physics_data["marks"].sum(), "total": len(physics_data) * 4},
    {"subject": "Chemistry", "obtained": chemistry_data["marks"].sum(), "total": len(chemistry_data) * 4},
    {"subject": "Mathematics", "obtained": math_data["marks"].sum(), "total": len(math_data) * 4}
])
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

# Add strength indicators
def get_strength_status(subject):
    strength_column = f'Strength_in_{subject.lower()}'
    return "Strong" if df[strength_column].iloc[0] == 'yes' else "Needs Improvement"

# Physics Summary
with col6:
    physics_score = physics_data['marks'].sum()
    physics_total = len(physics_data) * 4
    st.metric(
        label=f"Physics Score (Strength: {get_strength_status('physics')})",
        value=f"{physics_score}/{physics_total}",
        delta=f"{(physics_score/physics_total * 100):.1f}%"
    )

# Chemistry Summary
with col7:
    chemistry_score = chemistry_data['marks'].sum()
    chemistry_total = len(chemistry_data) * 4
    st.metric(
        label=f"Chemistry Score (Strength: {get_strength_status('chemistry')})",
        value=f"{chemistry_score}/{chemistry_total}",
        delta=f"{(chemistry_score/chemistry_total * 100):.1f}%"
    )

# Mathematics Summary
with col8:
    math_score = math_data['marks'].sum()
    math_total = len(math_data) * 4
    st.metric(
        label=f"Mathematics Score (Strength: {get_strength_status('mathematics')})",
        value=f"{math_score}/{math_total}",
        delta=f"{(math_score/math_total * 100):.1f}%"
    )

# Display Detailed Analysis
st.subheader("Detailed Question Analysis")
with st.expander("Show Question-wise Analysis"):
    st.dataframe(df[['physics_chapters', 'Questions_from_physics', 'Marks_in_physics']], use_container_width=True)
    st.dataframe(df[['chemistry_chapters', 'Questions_from_chemistry', 'Marks_in_chemistry']], use_container_width=True)
    st.dataframe(df[['mathematics_chapters', 'Questions_from_mathematics', 'Marks_in_mathematics']], use_container_width=True)
