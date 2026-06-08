from fastapi import FastAPI, Request, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from tavily import TavilyClient
from pypdf import PdfReader
from dotenv import load_dotenv
import tempfile
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

#WEB SEARCH

@app.get("/web_search")
def web_search(topic: str = Query(...)):

    result = client.search(
        query=topic,
        max_results=5
    )
    prompt = f"""
    Topic: {topic}

    Search Results:
    {result}

    Create a professional research report.

    Required Sections:

    1. Definition
    2. Overview
    3. Important Bullet Points
    4. Types / Categories
    5. Key Concepts
    6. Advantages
    7. Disadvantages
    8. Applications
    9. Conclusion

    Rules:
    - Do NOT copy text from the search results.
    - Summarize and rewrite in your own words.
    - Use headings.
    - Use bullet points.
    - Keep points concise.
    - Do not include website introductions, advertisements, image captions, or unrelated content.
    """

    response = llm.invoke(prompt)


    return {
        "response":response.content
    }


#PDF READER 

@app.post("/pdf_reader")
async def pdf_reader(
    file: UploadFile = File(...)
):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp:

        temp.write(await file.read())

        temp_path = temp.name

    reader = PdfReader(temp_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return {
        "text": text[:5000]
    }


# SUMMARIZER 

@app.post("/summarize")
async def summarize(request: Request):

    body = await request.json()

    text = body["text"]

    prompt = f"""
    Summarize the following content.

    {text}

    Give:
    1. Summary
    2. Key Points
    """

    result = llm.invoke(prompt)

    return {
        "response": result.content
    }


#  RESEARCH ASSISTANT

@app.post("/research")
async def research(request: Request):

    body = await request.json()

    topic = body["topic"]

    web_results = client.search(
        query=topic,
        max_results=5
    )

    prompt = f"""
    Research Topic:

    {topic}

    Search Results:

    {web_results}

    Generate:

    1. Executive Summary

    2. Key Points

    3. References

    4. Conclusion
    """

    result = llm.invoke(prompt)

    return {
        "response": result.content
    }


@app.get("/")
def home():

    return {
        "message": "AI Research Assistant Running"
    }