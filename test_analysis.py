import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Function to process the raw data
def process_data(data):
    # Convert the data into a DataFrame
    df = pd.DataFrame([data.split() for data in data.strip().split('\n')])
    # Set the column names from the first row
    df.columns = ['student_name', 'physics_chapters', 'Questions_from_physics', 'Question', 
                 'Option1', 'Option2', 'Option3', 'Option4', 'Correct_Answer', 'Marks_in_physics',
                 'chemistry_chapters', 'Questions_from_chemistry', 'Marks_in_chemistry',
                 'mathematics_chapters', 'Questions_from_mathematics', 'Marks_in_mathematics',
                 'Strength_in_physics', 'Strength_in_chemistry', 'Strength_in_mathematics']
    return df

# Sample data input - you can replace this with file upload or database connection
data = """student_name physics_chapters Questions_from_that_physics_chapter Question Option1 Option2 Option3 Option4 Correct_Answer Marks_in_physics chemistry_chapters Questions_from_that_chemistry_chapter Marks_in_chemistry mathematics_chapters Questions_from_that_mathematics_chapter Marks_in_mathematics Strength_in_physics Strength_in_chemistry Strength_in_mathematics
Student_A Kinematics Projectile_motion In_projectile_motion_the_horizontal_range_is_maximum_when_the_angle_of_projection_is 30 45 60 90 45 4 Atomic_Structure Bohr's_model 4 Quadratic_Equations Roots_of_quadratic 3 yes yes yes
Student_A Laws_of_Motion Newton's_laws Newton's_second_law_of_motion_states_that_force_is_equal_to Mass_times_acceleration Mass_times_velocity Acceleration_divided_by_mass Velocity_divided_by_time Mass_times_acceleration 3 Chemical_Bonding Molecular_orbital_theory 2 Matrices Matrix_operations 2 yes no no
Student_A Work_Energy_Power Work_done_by_forces Work_done_by_a_constant_force_is_calculated_as Force_x_distance_x_sin Force_x_distance_x_cos Force_x_displacement_x_sin Force_x_displacement_x_cos Force_x_displacement_x_cos 2 Thermodynamics First_law_of_thermodynamics 3 Determinants Properties_of_determinants 4 no yes yes
Student_A Gravitation Gravitational_force Gravitational_force_between_two_objects_is_inversely_proportional_to_the Distance_squared Distance Sum_of_masses Square_of_sum_of_masses Distance_squared 4 Equilibrium Le_Chatelier's_principle 4 Probability Bayes_theorem 1 yes yes no
Student_A Oscillations Simple_harmonic_motion The_period_of_simple_harmonic_motion_is_given_by 2pi_sqrt_m_k pi_sqrt_m_k 2pi_sqrt_k_m pi_sqrt_k_m 2pi_sqrt_m_k 1 Redox_Reactions Oxidation_numbers 1 Trigonometry Sine_and_cosine_rules 4 no no yes"""

# Process the data
df = process_data(data)

# Title
st.title(f"Performance Analysis - {df['student_name'].iloc[0]}")

# Create subject-wise data
physics_data = pd.DataFrame({
    'chapter': df['physics_chapters'].unique(),
    'marks': df['Marks_in_physics'].astype(int).values,
    'max_marks': 4
})

chemistry_data = pd.DataFrame({
    'chapter': df['chemistry_chapters'].unique(),
    'marks': df['Marks_in_chemistry'].astype(int).values,
    'max_marks': 4
})

math_data = pd.DataFrame({
    'chapter': df['mathematics_chapters'].unique(),
    'marks': df['Marks_in_mathematics'].astype(int).values,
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
