import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
import os

# Load trained model files
vectorizer = joblib.load("vectorizer.pkl")
career_vectors = joblib.load("career_vectors.pkl")
career_data = joblib.load("career_data.pkl")

# Initialize session state for history and chatbot
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI
st.title("🎓 AI Career Advisor")
st.write("Enter your details to get personalized career recommendations!")

# **🔹 User Input Section**
skills_list = [
    "Programming", "Machine Learning", "Data Analysis", "Communication",
    "Project Management", "Design Thinking", "Cybersecurity",
    "Marketing", "Finance", "Healthcare", "Robotics", "Cloud Computing"
]
skills_selected = st.multiselect("Select Your Skills", skills_list)
skills_extra = st.text_area("Add More Skills (Comma-separated)", "")

education = st.selectbox("Select Your Education Level", ["High School", "Diploma", "Bachelor's", "Master's", "PhD"])
job_preference = st.radio("Job Outlook Preference", ["Any", "High Growth", "Competitive", "Emerging", "Declining"])

personal_interests = st.multiselect("Select Your Personal Interests", [
    "Technology", "Healthcare", "Business", "Arts & Design",
    "Science & Research", "Social Work", "Finance", "Marketing"
])

work_preference = st.radio("Preferred Work Type", ["Full-time", "Part-time", "Remote", "Freelance", "Hybrid"])
work_environment = st.slider("Flexibility in Work Environment (1 = Rigid, 10 = Flexible)", 1, 10, 5)

industry_preference = st.selectbox("Preferred Industry", ["Any", "Technology", "Healthcare", "Finance", "Education", "Business", "Science", "Arts"])

if st.button("Find My Career"):
    # Combine inputs into a single text representation
    user_input_text = " ".join(skills_selected) + " " + skills_extra + " " + education + " " + work_preference + " " + industry_preference

    # Convert user input into a vector
    user_input = vectorizer.transform([user_input_text])
    
    # Compute similarity scores
    similarities = cosine_similarity(user_input, career_vectors)
    
    # Add similarity scores to dataframe
    career_data["Similarity"] = similarities[0]
    
    # Filter by job preference if selected
    filtered_data = career_data.copy()
    if job_preference != "Any":
        filtered_data = filtered_data[filtered_data["Job Outlook"] == job_preference]

    # Get **top 5** career matches
    top_matches = filtered_data.nlargest(5, "Similarity")

    # **📌 Display Recommendations**
    st.subheader("🚀 Top 5 Career Recommendations:")
    for idx, row in top_matches.iterrows():
        st.success(f"🎯 Career: **{row['Career']}**")
        st.write(f"🛠 **Required Skills:** {row['Required Skills']}")
        st.write(f"🎓 **Education Level:** {row['Education Level']}")
        st.write(f"📈 **Job Outlook:** {row['Job Outlook']}")
        st.write(f"💰 **Salary Range:** {row['Salary Range']}")
        st.write("---")
    
    # Add search to history
    st.session_state.search_history.append((skills_selected, education, job_preference, top_matches.iloc[0]["Career"]))

    # **📊 Salary & Demand Comparison Chart**
    st.subheader("💰 Salary & Demand Comparison")
    plt.figure(figsize=(8, 4))
    salaries = top_matches["Salary Range"].str.extract(r"(\d+)")[0].dropna().astype(int)  # Extract numbers properly
    plt.bar(top_matches["Career"], salaries)
    plt.xlabel("Career")
    plt.ylabel("Salary ($k)")
    plt.title("Salary Range Comparison")
    st.pyplot(plt)

# **🔍 Display Past Career Searches**
if st.session_state.search_history:
    st.subheader("🔍 Past Career Searches")
    for history in st.session_state.search_history[-5:]:  # Show last 5 searches
        st.write(f"**Skills:** {history[0]}, **Education:** {history[1]}, **Preference:** {history[2]}, **Recommended:** {history[3]}")

# **📚 Career Insights Sidebar**
st.sidebar.header("📊 Career Insights")
st.sidebar.write("🔹 AI-driven insights on career trends, required skills, and job market demand.")
st.sidebar.write("🔹 Stay updated with high-demand careers and salaries.")
st.sidebar.write("🔹 Explore emerging fields and career transitions.")

# **💬 AI Career Chatbot**
st.sidebar.header("💬 Career Chatbot")
user_query = st.sidebar.text_input("Ask me about careers, skills, or job outlook!")

# Predefined chatbot responses
chatbot_responses = {
    
    "high salary": "Some high-paying careers include Data Science, AI Engineering, and Finance roles.",
    "tech industry": "The tech industry is booming! Roles like Software Developer, AI Engineer, and Cybersecurity Expert are in demand.",
    "healthcare": "Healthcare careers such as doctors, nurses, and biomedical engineers have strong job stability.",
    "data science": "Data Science is a top field with demand in finance, healthcare, and tech industries.",
    "remote jobs": "Many careers now offer remote work, including Software Development, Digital Marketing, and Freelancing.",
    "cybersecurity": "Cybersecurity is a crucial field protecting organizations from cyber threats.",
    "artificial intelligence": "AI careers include AI Researcher, Machine Learning Engineer, and Data Scientist.",
    "finance": "Finance careers like Investment Banking, Risk Analysis, and FinTech are lucrative options.",
    "marketing": "Marketing offers creative roles in branding, digital marketing, and market research.",
    "education": "Teaching, EdTech, and curriculum development are great options in the education sector.",
    "freelancing": "Freelancing is flexible and includes writing, graphic design, programming, and consulting.",
    "government jobs": "Government careers provide stability in sectors like administration, law enforcement, and public health.",
    "blockchain": "Blockchain technology powers cryptocurrencies and offers careers in blockchain development.",
    "robotics": "Robotics engineers work on automation, AI, and intelligent machines.",
    "green energy": "Renewable energy jobs are growing in solar, wind, and sustainability sectors.",
    "entrepreneurship": "Starting a business requires innovation, risk-taking, and strong management skills.",
    "law": "Legal careers include corporate law, criminal law, and intellectual property law.",
    "medicine": "Medicine is a high-demand field including doctors, nurses, and medical researchers.",
    "biotechnology": "Biotech careers focus on medical advancements, genetics, and pharmaceuticals.",
    "gaming industry": "Game development, animation, and esports are thriving industries.",
    "consulting": "Consulting careers exist in management, finance, IT, and HR.",
    "aviation": "Aviation includes careers as pilots, air traffic controllers, and aerospace engineers.",
    "space industry": "Space exploration careers include astronaut, aerospace engineer, and astrophysicist.",
    "supply chain": "Logistics and supply chain management are essential in global trade and e-commerce.",
    "hospitality": "Hotel management, tourism, and event planning offer exciting career opportunities.",
    "fashion industry": "Fashion careers range from design to marketing and merchandising.",
    "graphic design": "Graphic designers create visual content for branding, marketing, and digital platforms.",
    "writing": "Writing careers include content writing, journalism, and copywriting.",
    "HR": "Human Resources professionals manage recruitment, training, and employee relations.",
    "automotive": "Careers in the auto industry include vehicle design, engineering, and maintenance.",
    "telecommunications": "Telecom jobs involve network infrastructure, 5G development, and cybersecurity.",
    "agriculture": "Agricultural careers include farming, agribusiness, and food science.",
    "AI ethics": "AI ethics focuses on responsible AI development and preventing bias in algorithms.",
    "e-commerce": "E-commerce careers involve online retail, digital marketing, and supply chain logistics.",
    "sports": "Sports careers range from athletes and coaches to sports analysts and fitness trainers.",
    "chemistry": "Chemists work in pharmaceuticals, materials science, and environmental chemistry.",
    "psychology": "Psychologists help people with mental health, counseling, and behavioral research.",
    "architecture": "Architects design buildings, urban spaces, and sustainable structures.",
    "civil engineering": "Civil engineers work on infrastructure, construction, and urban planning.",
    "music industry": "Music careers include performance, production, and sound engineering.",
    "event management": "Event managers plan conferences, weddings, and corporate events.",
    "nanotechnology": "Nanotechnology explores materials and technology at the atomic scale.",
    "social work": "Social workers assist communities with healthcare, education, and welfare services.",
    "marine biology": "Marine biologists study ocean ecosystems, conservation, and aquatic life.",
    "photography": "Photography careers include journalism, fashion, and commercial photography.",
    "ethnography": "Ethnographers study cultures and human behavior through research and fieldwork.",
    "pharmaceuticals": "Pharmaceutical careers involve drug research, development, and manufacturing.",
    "animation": "Animation careers include 3D modeling, film, and video game production.",
}

if user_query:
    response = "I don't have an exact answer, but I can help with career guidance!"  # Default response
    for key in chatbot_responses:
        if key in user_query.lower():
            response = chatbot_responses[key]
            break
    
    st.sidebar.write("🤖 AI Bot: ", response)
    st.session_state.chat_history.append(f"You: {user_query}\nBot: {response}")

# Show chat history
if st.session_state.chat_history:
    st.sidebar.subheader("📜 Chat History")
    for chat in st.session_state.chat_history[-5:]:  # Show last 5 messages
        st.sidebar.text(chat) 