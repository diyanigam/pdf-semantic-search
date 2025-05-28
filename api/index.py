from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import pymupdf
import re
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from mangum import Mangum

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

#reading text from pdf and splitting them into sentences
def extract_text(pdf):
  doc = pymupdf.open(pdf)
  text = ""
  for page in doc:
    text += page.get_text()
  #text = text.replace('\u2028', '').replace('\n', ' ')
  text = re.sub(r'[\u2028\u2029\n\r]+', ' ', text)
  return re.split(r'(?<=[.!?])\s+', text.strip())


# creates embeddings allowing semantic search
def sentences_to_encodings(sentences):
    embeddings = model.encode(sentences)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, embeddings, sentences


def answer(question, all_data, k = 5):
    q_embed = model.encode([question])
    D, I = all_data[0].search(np.array(q_embed), k)
    top_chunks = [all_data[2][i] for i in I[0]]
    return " \n ".join(top_chunks)


@app.post("/")
async def get_answer(file: UploadFile = File(...), question: str = Form(...), k : int =Form(5) ):
    try:
        contents = await file.read()
        tmp_path = f"/tmp/{file.filename}"
        with open(tmp_path, "wb") as f:
            f.write(contents)

        sentences = extract_text(tmp_path)
        all_data = sentences_to_encodings(sentences)
        result = answer(question, all_data, k)

        return JSONResponse(content={"Response": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

handler = Mangum(app)