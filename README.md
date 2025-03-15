# AI Career Advisor

## How to Run This Project

### 1. Install Required Packages
Ensure you have Python 3.9 installed. Then, install the necessary packages:

```bash
pip install streamlit pandas numpy matplotlib google-generativeai fpdf
```

### 2. Set Up API Key
In the `app.py` file, ensure your Google Gemini API key is configured properly:

```python
import google.generativeai as genai
API_KEY = "YOUR_API_KEY"
genai.configure(api_key=API_KEY)
```

Replace `YOUR_API_KEY` with your own API key.

### 3. Ensure Model Files are Present
Make sure the following files are in the same directory as `app.py`:
- `vectorizer.pkl`
- `career_vectors.pkl`
- `career_data.pkl`

### 4. Run the Streamlit App
Start the app by running:

```bash
streamlit run app.py
```

### 5. Access the Web App
Open your browser and visit:
```
http://localhost:8501
```

### Troubleshooting
- If `pickle.load` throws errors, ensure the `.pkl` files are not corrupted and are correctly formatted.
- If the API doesn’t respond, verify your API key and internet connection.
- For missing packages, rerun `pip install -r requirements.txt` (if you create one).

You're now ready to explore AI-powered career recommendations and chatbot guidance!

