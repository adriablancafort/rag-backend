from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from functions_vector_search import save_database, nearest_vector
from pdf_scrapper import text_from_pdfURL
from web_scrapper import extract_content

app = FastAPI()
client = OpenAI(api_key="")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"response": "OK"}


@app.get("/ask/{prompt}")
def ask(prompt: str):
    return {"response": get_response(prompt)}

def get_response(prompt: str):
    context_list = nearest_vector(prompt, 1) # list of str if list len is 0 the text is not tlaking about the subject
    context_string = "--------".join(context_list) 
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": 'Answer questions based only on the following context:'+context_string+'if context does not exist, or you can\'t find the awnser, say it'},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content


@app.get("/get_url/{URL:path}")
def get_url(URL:str) -> None:
    if URL[-3:] == "pdf":
        text = text_from_pdfURL(URL)
    else:
        text = extract_content(URL)
    
    save_database(text)

    #preprocess del text


