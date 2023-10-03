#!/usr/bin/env python
import subprocess
import os
import tracemalloc
import git


# Define the package(s) you want to install
packages_to_install = ["langchain", "openai", "tiktoken", "chromadb", "unstructured", "markdown"]

# Run the pip install command
for package in packages_to_install:
    try:
        subprocess.check_call(["pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")

from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from chromadb.errors import InvalidDimensionException

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

repository_url = 'https://github.com/wavemaker/docs.git'

# Local path where you want to clone the repository
local_path = 'docsRepo'

# Clone the repository
#git.Repo.clone_from(repository_url, local_path)
# Path to the folder containing markdown files
all_texts = []


# Start tracing memory allocations
#tracemalloc.start()

# Load and process documents
for foldername, subfolders, filenames in os.walk(local_path+'/learn/app-development/widgets/basic'):
    for filename in filenames:
        if filename.endswith(".md"):  # Ensure the file is a Markdown file
            file_path = os.path.join(foldername, filename)

            try:
                    loader = UnstructuredMarkdownLoader(file_path, mode="elements", strategy="fast")
                    documents = loader.load()
                    
                    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
                    texts = text_splitter.split_documents(documents)
                    if texts:
                        all_texts.extend(texts)
            except Exception as e:
                print(f"Error occurred while processing {file_path}: {e}")

# snapshot = tracemalloc.take_snapshot()
# top_stats = snapshot.statistics('lineno')
# top_stats = sorted(top_stats, key=lambda stat: stat.size, reverse=True)[:10]  # Get top 10 allocations
# for stat in top_stats:
#     print(stat)
#
#
# # Stop tracing memory
# tracemalloc.stop()

# Embedding and Chroma initialization
os.environ["OPENAI_API_KEY"] = "sk-3GJrgsAKjPcnsoTqBT5iT3BlbkFJErZUaNwaveVwbLhpkdZUN"
embeddings = OpenAIEmbeddings(model_kwargs={"model_name": "gpt-3.5-turbo"})

try:
    db = Chroma.from_documents(all_texts, embeddings)
except InvalidDimensionException:
    Chroma().delete_collection()
    db = Chroma.from_documents(all_texts, embeddings)

db._collection.get(include=['embeddings'])

# Create a retriever outside the loop
retriever = db.as_retriever(search_type="mmr",
                search_kwargs={'k': 6, 'lambda_mult': 0.25})

qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(),
                                  chain_type="stuff",
                                  retriever=retriever,
                                  return_source_documents=True)


def question(qtn):
    return retriever.get_relevant_documents(qtn);

def process_llm_response(llm_response):
    print(llm_response['result'])
    print('\n\nSources:')
    for source in llm_response["source_documents"]:
        print(source.metadata['source'])

def test(questionFromApi):
    query = questionFromApi
    llm_response = qa_chain(query)
    process_llm_response(llm_response)
    return llm_response

