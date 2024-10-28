import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=groq_api_key)

# Updated detailed prompt structure for single student analysis
summary_prompt_single = PromptTemplate.from_template("""
I run an EdTech business focused on preparing students for the Joint Entrance Examination (JEE).
Below is the structured data for a student's performance, broken down by columns:

1. **Student Name**: Identifier for each student being analyzed.
2. **Physics Section**:
   - **Physics Chapters**: Specific chapters from which questions are derived (e.g., "Kinematics" or "Laws of Motion").
   - **Questions from that Physics Chapter**: Topic within the chapter (e.g., "Projectile Motion") specifying the focus of each question.
   - **Question**: The actual MCQ presented to the student.
   - **Option 1 to Option 4**: Four answer options provided for each question.
   - **Correct Answer**: The correct option for each question.
   - **Marks in Physics**: Score achieved on each Physics question (out of a maximum of 4).
3. **Chemistry Section**:
   - **Chemistry Chapters**: Chapters for Chemistry questions (e.g., "Atomic Structure" or "Thermodynamics").
   - **Questions from that Chemistry Chapter**: Topic within each chapter, such as "Bohr’s Model" or "Le Chatelier’s Principle".
   - **Question, Options 1–4, Correct Answer**: Structure as in Physics, with a unique MCQ per topic and correct option.
   - **Marks in Chemistry**: Score for each Chemistry question, with a maximum of 4.
4. **Mathematics Section**:
   - **Mathematics Chapters**: Chapters for Mathematics questions (e.g., "Quadratic Equations" or "Probability").
   - **Questions from that Mathematics Chapter**: Topic within each chapter, like "Roots of Quadratic" or "Bayes' Theorem".
   - **Question, Options 1–4, Correct Answer**: Similar format as Physics and Chemistry, with four options and correct answer.
   - **Marks in Mathematics**: Score achieved on each Mathematics question (maximum of 4).
5. **Strength Indicators**:
   - **Strength in Physics**: Indicates whether the student is strong in Physics ("yes" or "no").
   - **Strength in Chemistry**: Indicates strength in Chemistry ("yes" or "no").
   - **Strength in Mathematics**: Indicates strength in Mathematics ("yes" or "no").

{context}

Based on this data, provide a detailed summary of the student's strengths, opportunities, and challenges.
Offer specific, actionable suggestions for improvement.
""")

# Updated prompt for multiple students analysis
summary_prompt_multiple = PromptTemplate.from_template("""
I run an EdTech business focused on preparing students for the Joint Entrance Examination (JEE).
The following dataset provides detailed information on multiple students' performance, structured as follows:

1. **Student Name**: Identifier for each student being analyzed.
2. **Physics Section**: 
   - **Physics Chapters**, **Questions from that Physics Chapter**, **Question**, **Options 1–4**, **Correct Answer**, **Marks in Physics**
3. **Chemistry Section**:
   - **Chemistry Chapters**, **Questions from that Chemistry Chapter**, **Question**, **Options 1–4**, **Correct Answer**, **Marks in Chemistry**
4. **Mathematics Section**:
   - **Mathematics Chapters**, **Questions from that Mathematics Chapter**, **Question**, **Options 1–4**, **Correct Answer**, **Marks in Mathematics**
5. **Strength Indicators**:
   - **Strength in Physics**, **Strength in Chemistry**, **Strength in Mathematics**

{context}

For each student, generate a detailed summary of their strengths, opportunities, and challenges.
Include comparative insights for students, identifying where they can learn from each other's strengths and work on similar challenges. Provide actionable improvement suggestions for each student.
""")

@st.cache_data
def load_data():
    file_path = 'https://raw.githubusercontent.com/forittik/updated_soca_tool/refs/heads/main/Dummy_questions.csv'
    df = pd.read_csv(file_path, header=0, encoding='ISO-8859-1')
    return df

def get_student_data(name, df):
    student_data = df[df['user_id'] == name]
    if student_data.empty:
        return None
    return student_data

def generate_single_student_summary(student_data):
    context = student_data.to_string(index=False)
    summary_chain = summary_prompt_single | llm | StrOutputParser()
    summary = summary_chain.invoke({"context": context})
    return summary

def generate_multiple_students_summary(student_data):
    context = student_data.to_string(index=False)
    summary_chain = summary_prompt_multiple | llm | StrOutputParser()
    summary = summary_chain.invoke({"context": context})
    return summary

def process_students(names, df):
    if isinstance(names, str):
        student_data = get_student_data(names, df)
        if student_data is None:
            return f"No data found for student: {names}"
        return generate_single_student_summary(student_data)
    elif isinstance(names, list):
        combined_data = pd.concat([get_student_data(name, df) for name in names if get_student_data(name, df) is not None])
        if combined_data.empty:
            return "No data found for the given students."
        return generate_multiple_students_summary(combined_data)

st.title("B2B Dashboard")
df = load_data()
student_names = df['user_id'].tolist()
selected_names = st.multiselect("Select student(s) to analyze:", student_names)

if st.button("Analyze student data"):
    if selected_names:
        summary = process_students(selected_names, df)
        st.write(summary)
    else:
        st.warning("Please select at least one student.")
