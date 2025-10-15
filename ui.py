import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Config
ENDPOINT = ""
KEY = ""
INDEX = "incidents-kb"

client = SearchClient(ENDPOINT, INDEX, AzureKeyCredential(KEY))

# UI
st.title("🤖 AIOps Incident Resolver")
query = st.text_input("Describe your issue:")

if query:
    results = list(client.search(query, top=1))
    if results:
        r = results[0]
        st.success("✅ Solution Found")
        st.write(f"**Category:** {r['service_category']}")
        st.write(f"**Root Cause:** {r['root_cause']}")
        st.write(f"**Resolution:** {r['resolution_steps']}")
        st.write(f"**KB:** {r['kb_article_id']}")
    else:
        st.error("No solution found")