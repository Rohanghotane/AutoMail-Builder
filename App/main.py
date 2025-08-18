import streamlit as st

st.title("📧 COLD MAIL GENERATOR")
url_import = st.text_input("Enter a URL:", value="https://webkul.com/jobs/ai/machine-learning-developers/")
submit_button = st.button("Submit") 

if submit_button:
    try:
        loader = WebBaseLoader([url_input])
        data = clean_text(loader.load().pop().page_content)
        portfolio.load_portfolio()
        jobs = llm.extract_jobs(data)
        for job in jobs:
            skills = job.get('skills',[])
            links = portfolio.query_links(skills)
            email = llm.write_mail(job, links)
            st.code(email, language='markdown')
    except Exception as e:
        st.error(f"AN error occurred: {e}")
