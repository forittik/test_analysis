import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

# Initialize ChatGroq LLM
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=groq_api_key)

# Set page configuration
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Load data function
def load_data():
    file_path = 'https://raw.githubusercontent.com/forittik/test_analysis/refs/heads/main/jee_student_data_75_questions.csv'
    df = pd.read_csv(file_path, header=0, encoding='ISO-8859-1')
    return df

# Generate summary for a single student
def generate_single_student_summary(student_data_chunk):
    context = student_data_chunk.to_string(index=False)
    summary_chain = summary_prompt_single | llm | StrOutputParser()
    summary = summary_chain.invoke({"context": context})
    return summary

# Process student data in batches
def process_student_data_in_batches(student_data, batch_size=2):
    num_chunks = len(student_data) // batch_size + (1 if len(student_data) % batch_size > 0 else 0)
    summaries = []

    for i in range(num_chunks):
        chunk = student_data.iloc[i * batch_size:(i + 1) * batch_size]
        summary = generate_single_student_summary(chunk)
        summaries.append(summary)

    return summaries

# Summary prompt for single student
summary_prompt_single = PromptTemplate.from_template("""
I run an EdTech business focused on preparing students for the Joint Entrance Examination (JEE).
Below is the structured data for a student's performance, broken down by columns:

1. **Student Name**: Identifier for each student being analyzed.
2. **Physics Section**:
   - **Marks in Physics**: Score achieved on each Physics question (out of a maximum of 4).
3. **Chemistry Section**:
   - **Marks in Chemistry**: Score for each Chemistry question, with a maximum of 4.
4. **Mathematics Section**:
   - **Marks in Mathematics**: Score achieved on each Mathematics question (maximum of 4).
5. **Strength Indicators**:
   - **Strength in Physics**: Indicates whether the student is strong in Physics ("yes" or "no").
   - **Strength in Chemistry**: Indicates strength in Chemistry ("yes" or "no").
   - **Strength in Mathematics**: Indicates strength in Mathematics ("yes" or "no").

{context}

Using this dataset, please analyze the student's performance by evaluating their accuracy and consistency in answering questions across different topics within each subject. Identify their strengths and areas for improvement based on scores and correct answer patterns. Aim to provide a holistic view of the student’s readiness and competency in Physics, Chemistry, and Mathematics for the JEE.
""")

# Summary prompt for final output
final_summary_prompt = PromptTemplate.from_template("""
You have received the following detailed summaries for a student's performance across different subjects. Please summarize the key insights and present a concise overview highlighting strengths and areas for improvement.

{detailed_summaries}
""")

# Generate final summary from detailed summaries
def generate_final_summary(detailed_summaries):
    if len(detailed_summaries) <= 5:
        summary_chain = final_summary_prompt | llm | StrOutputParser()
        final_summary = summary_chain.invoke({"detailed_summaries": "\n".join(detailed_summaries)})
    else:
        intermediate_summaries = []
        for i in range(0, len(detailed_summaries), 5):
            segment = detailed_summaries[i:i + 5]
            summary_chain = final_summary_prompt | llm | StrOutputParser()
            intermediate_summary = summary_chain.invoke({"detailed_summaries": "\n".join(segment)})
            intermediate_summaries.append(intermediate_summary)
        final_summary = generate_final_summary(intermediate_summaries)

    return final_summary

# Process the data
df = load_data()

# Title
st.title(f"Performance Analysis - {df['student_name'].iloc[0]}")

# Create subject-wise data with handling for NaN values
physics_data = pd.DataFrame({
    'chapter': df['physics_chapters'].dropna().unique(),
    'marks': df.groupby('physics_chapters')['Marks_in_physics'].sum().reindex(df['physics_chapters'].dropna().unique(), fill_value=0).astype(int),
    'max_marks': 4
})

chemistry_data = pd.DataFrame({
    'chapter': df['chemistry_chapters'].dropna().unique(),
    'marks': df.groupby('chemistry_chapters')['Marks_in_chemistry'].sum().reindex(df['chemistry_chapters'].dropna().unique(), fill_value=0).astype(int),
    'max_marks': 4
})

math_data = pd.DataFrame({
    'chapter': df['mathematics_chapters'].dropna().unique(),
    'marks': df.groupby('mathematics_chapters')['Marks_in_mathematics'].sum().reindex(df['mathematics_chapters'].dropna().unique(), fill_value=0).astype(int),
    'max_marks': 4
})

# Update total marks for each subject
total_questions = 75
marks_per_question = 4
total_marks = total_questions * marks_per_question

# Create layout with columns
col1, col2 = st.columns(2)

# Subject-wise Performance Bar Chart
with col1:
    st.subheader("Subject-wise Scores")
    fig_scores = go.Figure(data=[
        go.Bar(name='Marks Obtained', x=['Physics', 'Chemistry', 'Mathematics'], 
               y=[df['Marks_in_physics'].sum(), df['Marks_in_chemistry'].sum(), df['Marks_in_mathematics'].sum()],
               marker_color='#0088FE'),
        go.Bar(name='Total Marks', x=['Physics', 'Chemistry', 'Mathematics'], 
               y=[total_marks, total_marks, total_marks],
               marker_color='#00C49F')
    ])
    fig_scores.update_layout(barmode='group', height=400)
    st.plotly_chart(fig_scores, use_container_width=True)

# Radar Chart for Performance Distribution
with col2:
    st.subheader("Performance Distribution (%)")
    percentage_scores = [
        (df['Marks_in_physics'].sum() / total_marks) * 100,
        (df['Marks_in_chemistry'].sum() / total_marks) * 100,
        (df['Marks_in_mathematics'].sum() / total_marks) * 100
    ]
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=percentage_scores,
        theta=['Physics', 'Chemistry', 'Mathematics'],
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

# Summary Statistics
st.subheader("Summary Statistics")
col6, col7, col8 = st.columns(3)

# Add strength indicators
def get_strength_status(subject):
    strength_column = f'Strength_in_{subject.lower()}'
    return "Strong" if df[strength_column].iloc[0] == 'yes' else "Needs Improvement"

# Physics Summary
with col6:
    physics_score = df['Marks_in_physics'].sum()
    st.metric(
        label=f"Physics Score (Strength: {get_strength_status('Physics')})",
        value=physics_score,
        delta=f"{physics_score / total_marks * 100:.2f}%",
        help=f"Max Marks: {total_marks} (75 questions * 4 marks each)"
    )

# Chemistry Summary
with col7:
    chemistry_score = df['Marks_in_chemistry'].sum()
    st.metric(
        label=f"Chemistry Score (Strength: {get_strength_status('Chemistry')})",
        value=chemistry_score,
        delta=f"{chemistry_score / total_marks * 100:.2f}%",
        help=f"Max Marks: {total_marks} (75 questions * 4 marks each)"
    )

# Mathematics Summary
with col8:
    math_score = df['Marks_in_mathematics'].sum()
    st.metric(
        label=f"Mathematics Score (Strength: {get_strength_status('Mathematics')})",
        value=math_score,
        delta=f"{math_score / total_marks * 100:.2f}%",
        help=f"Max Marks: {total_marks} (75 questions * 4 marks each)"
    )

# Additional insights
st.subheader("Additional Insights")
detailed_summaries = process_student_data_in_batches(df)
final_summary = generate_final_summary(detailed_summaries)
st.write(final_summary)

# End of Streamlit app
