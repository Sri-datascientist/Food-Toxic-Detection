import requests
import json
import streamlit as st

# Replace with your actual OpenRouter API key (use Streamlit secrets!)
OPENROUTER_API_KEY = "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"

def predict_food_toxicity(ingredients, product_name=""):
    """Predicts food toxicity and parses for human-like response."""
    response_content = get_api_response(ingredients, product_name, "toxicity")
    return parse_human_response(response_content)

def get_supporting_docs(ingredients, product_name=""):
    """Gets supporting documents and parses for human-like response."""
    response_content = get_api_response(ingredients, product_name, "docs")
    return parse_human_response(response_content)

def get_research_hypothesis(ingredients, product_name=""):
    """Gets research hypothesis and parses for human-like response."""
    response_content = get_api_response(ingredients, product_name, "hypothesis")
    return parse_human_response(response_content)

def get_api_response(ingredients, product_name, request_type):
    """Gets the raw API response from OpenRouter."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    prompt = get_prompt(ingredients, product_name, request_type)
    data = json.dumps({
        "model": "google/gemini-2.0-pro-exp-02-05:free",
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    })
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"]
        else:
            return "Error: Could not retrieve information from the API."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON response: {e}"
    except KeyError as e:
        return f"Error: Unexpected JSON format: {e}"

def get_prompt(ingredients, product_name, request_type):
    """Generates the prompt based on the request type."""
    if request_type == "toxicity":
        return f"""
Here are the ingredients to analyze for potential toxicity and allergic reactions. Provide a risk level (High, Medium, Low) with a reason. Avoid starting with phrases like 'Okay, let's start' or similar introductions. Do not use <br> tags or asterisks (*) in the output. Ensure the table is perfectly aligned with consistent spacing.

Input Format:
Product Name: {product_name} (if available)
Ingredients: {ingredients}

Output Structure:
Toxicity Risk Level: (High/Medium/Low)
Allergy Risk Level: (High/Medium/Low)
give color symbols red for high 🔴, orange for moderate 🟠, green for low 🟢.
Reason: (Detailed explanation in a table with columns 'Ingredient', 'Toxicity Concern', 'Allergy Concern', perfectly aligned)
make it structured and humanized.
"""
    elif request_type == "docs":
        return f"""
Here are the ingredients to find supporting documents and links for potential toxicity and allergic reactions, limited to about 500 words. Avoid starting with phrases like 'Okay, let's start' or similar introductions. Do not use <br> tags or asterisks (*) in the output. Provide hyperlinks in Markdown format, e.g., [Title](URL), for clickable links.

Input Format:
Product Name: {product_name} (if available)
Ingredients: {ingredients}

Output Structure:
Supporting Documents: (Table with columns 'Document Title' and 'Link', in point-wise format, using Markdown hyperlinks like [Title](URL))
Not Supporting Documents: (Table with columns 'Document Title' and 'Link', in point-wise format, using Markdown hyperlinks like [Title](URL))
make it approachable and humanized, like a friendly explanation.
"""
    elif request_type == "hypothesis":
        return f"""
Here are the ingredients to develop a research hypothesis and procedure for investigating potential toxicity and allergic reactions, limited to about 500 words. Avoid starting with phrases like 'Okay, let's start' or similar introductions. Do not use <br> tags or asterisks (*) in the output.

Input Format:
Product Name: {product_name} (if available)
Ingredients: {ingredients}

Output Structure:
Research Hypothesis: (Short hypothesis statement)
Research Procedure: (Table with columns 'Step' and 'Description', in point-wise format)
make it approachable and humanized, like a friendly suggestion.
"""

def parse_human_response(response_content):
    """Parses the response to make it sound more human-like, removing unwanted tags and phrases."""
    if "Error:" in response_content:
        return response_content
    
    # Remove <br> tags and asterisks
    response_content = response_content.replace("<br>", "").replace("<br/>", "").replace("<br />", "").replace("*", "")
    
    # Remove unwanted introductory phrases
    unwanted_phrases = [
        "Okay, let's break down these ingredients and assess their potential toxicity and allergenicity:\n\n",
        "Here’s an analysis of the ingredients you provided:\n\n",
        "Let me analyze these ingredients for you:\n\n",
        "Okay, let's start:\n\n",
        "Alright, here we go:\n\n",
        "Let's begin with:\n\n"
    ]
    for phrase in unwanted_phrases:
        response_content = response_content.replace(phrase, "")
    
    return response_content

# Streamlit app styling with logo
st.markdown(
    """
    <style>
    body {
        background-image: url("https://images.unsplash.com/photo-1542838132-92c53300491e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-repeat: no-repeat;
        color: #333333;
    }
    .stApp {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        max-width: 800px;
        margin: 0 auto;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #f0f8ff;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 8px;
        width: 100%;
        box-sizing: border-box;
    }
    .stWarning {
        background-color: #ffcccc;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .logo {
        position: absolute;
        top: 10px;
        left: 10px;
        width: 100px;
        height: 70px;
        object-fit: contain; /* Ensures the entire image is visible without cropping */
    }
    .footer {
        text-align: center;
        font-size: 20px;
        margin-top: 20px;
        color:blue;
        text-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add clickable logo at the top-left
st.markdown(
    """
    
    """,
    unsafe_allow_html=True,
)

st.title("Food Toxicity Detection App")

product_name = st.text_input("Enter brand or product name (optional):")
ingredients = st.text_area("Enter food ingredients (comma-separated):")

# Initialize session state
if "toxicity_result" not in st.session_state:
    st.session_state.toxicity_result = None
if "docs_result" not in st.session_state:
    st.session_state.docs_result = None
if "hypothesis_result" not in st.session_state:
    st.session_state.hypothesis_result = None
if "show_docs" not in st.session_state:
    st.session_state.show_docs = False
if "show_hypothesis" not in st.session_state:
    st.session_state.show_hypothesis = False

if st.button("Analyze Ingredients"):
    if ingredients:
        with st.spinner("Analyzing..."):
            st.session_state.toxicity_result = predict_food_toxicity(ingredients, product_name)
            st.session_state.show_docs = False
            st.session_state.show_hypothesis = False
    else:
        st.warning("Please enter food ingredients.")

if st.session_state.toxicity_result:
    st.markdown(st.session_state.toxicity_result)

    if st.button("Supporting Documents"):
        with st.spinner("Retrieving documents..."):
            st.session_state.docs_result = get_supporting_docs(ingredients, product_name)
            st.session_state.show_docs = True

    if st.session_state.show_docs and st.session_state.docs_result:
        st.markdown(st.session_state.docs_result)

    if st.button("Research Hypothesis"):
        with st.spinner("Generating hypothesis..."):
            st.session_state.hypothesis_result = get_research_hypothesis(ingredients, product_name)
            st.session_state.show_hypothesis = True

    if st.session_state.show_hypothesis and st.session_state.hypothesis_result:
        st.markdown(st.session_state.hypothesis_result)

st.markdown("---")
st.markdown("Disclaimer: This tool provides general information and should not replace professional medical advice.")
st.markdown('<div class="footer">Powered By Bio-Gred</div>', unsafe_allow_html=True)