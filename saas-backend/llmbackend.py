'''
This file contains the backend logic for the language model application.
It includes functions for loading text data, creating a vector database, and interacting with the conversational model.
The conversational model is implemented using the Langchain library, which combines a language model with a retrieval system to generate responses to user queries.

# Some old apis are used here, need to change it later. The log from the terminal shows it need to change to 
# langchain_community.vectorstores import FAISS langchain_community, and langchain_openai, ...
# Please follow the log from the terminal if it is need refactor.

# TODO: It seems that langchain_comunity.llms OPENAI will be deprecated
# TODO: Open AI Key should be stored in a secure way, not hardcoded in the code
@author: Haoze Du
@commented by: Sanjit Verma 
'''

import os
import pickle as pkl
from langchain_openai import OpenAIEmbeddings               # import this to support creating the vector database from the text
from langchain_community.vectorstores import FAISS          # Facebook AI Similarity Search (Faiss) provides an implemenation of the vector database.
from langchain_community.llms import OpenAI                 # OpenAI is an open-source library for natural language understanding.
from langchain.chains import ConversationalRetrievalChain   # The one popular chain from langchain, which concatenates the previous model's output to the new model's input.


# This function is responsible for loading text data from a preprocessed pickle file. 
# It returns the data as a list of text chunks, which are typically segments of text that have been stored in a serialized format using Python's pickle module.
def get_text_chunks(filename: str) -> list: 
    '''
    Get  the text chunks from the preprocessed pickle file.

    Params:
    - filename(str): the filename of the preprocessed text chunks.

    Returns:
    - l(list): the list of all text chunks from the pickle file.
    ''' 
    # read the preprocessed text chunks from the pickle file
    with open(filename, "rb") as f:
        l = pkl.load(f)
    return l

# This function takes a list of text chunks and converts them into a vector database using FAISS (Facebook AI Similarity Search). 
# FAISS is designed for efficient similarity search and clustering of dense vectors, which makes it suitable for tasks such as searching within a large volume of text data.
def make_vector_database(chunks_list: list) -> FAISS:
    '''
    Make the vector database from the text chunks.

    Params:
    - chunks_list(list): the list of all text chunks.
    
    Returns:
    - db(FAISS): the vector database from the text chunks.
    '''
    # Get embedding model
    embeddings = OpenAIEmbeddings()

    # Create vector database from the text chunks, using the embedding model
    # TODO: make it only excute once.
    db = FAISS.from_documents(chunks_list, embeddings)
    return db

# This function handles the interaction with the conversational model. 
# It uses a conversational retrieval chain from the Langchain library, which allows chaining a language model with a retrieval system (in this case, FAISS).
# The function processes a user query, retrieves relevant information from the vector database, and uses a conversational model to generate a response based on this information and the history of the conversation.
def make_query(chat_history: list, question: str) -> str:
    '''
    This function processes a user question using the OpenAI API by first retrieving relevant context from a vectorized database,
    then sending the question along with the context to OpenAI for response generation.

    Params:
    - chat_history (list): The history of the conversation so far, used to maintain context.
    - question (str): The question to query the OpenAI model.

    Returns:
    - str: The answer generated by the OpenAI API based on the provided question and conversational context.
    '''
    
    # Set the OpenAI API key from an environment variable or directly in code.
    # It is generally safer to manage API keys using environment variables (@TODO we should fix this later).
    os.environ["OPENAI_API_KEY"] = "KEY HERE"

    # Load text chunks from a pickle file, which are pre-processed segments of text data stored for quick retrieval.
    db = make_vector_database(chunks_list=get_text_chunks("textbook.pkl"))

    # Instantiate a ConversationalRetrievalChain with an OpenAI language model and the vector database retriever.
    # Setting verbose to True will print detailed logs about the retrieval process.
    qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.1), db.as_retriever(), verbose=True)

    # Execute the conversational retrieval chain by passing the current chat history and the new question.
    # This process integrates both historical context and the current question to generate a relevant response.
    result = qa({"chat_history": chat_history, "question": question})

    last_answer = result['answer']

    # Append the new question and its answer to the chat history for future context management.
    chat_history.append((question, result['answer']))

    # Return the answer generated by the OpenAI API.
    return result
