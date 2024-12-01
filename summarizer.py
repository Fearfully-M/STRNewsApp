# ChatGPT was extremely helpful for helping to understand Hugging Face and finding a model that would fit this project
# used for summarizer transcripts
from transformers import pipeline # huggingface summarization transformer
import nltk
nltk.download('punkt') 
from nltk.tokenize import sent_tokenize

# Split the text by words to help avoid tokenization limits
def split_text_by_words(text, max_tokens):
    words = text.split()  # Split the text into words
    chunks = []
    current_chunk = []
    current_length = 0

    # inspired via ChatGPT
    # although this does have the issue of losing out on context because the transformer can only
    # summarize based on max tokenization limit and there is no control at where in a sentence/paragraph
    # the 'chunks' stop to summarize
    for word in words:
        if current_length + 1 > max_tokens:  # Check if adding another word exceeds the limit
            chunks.append(" ".join(current_chunk))  # Add the current chunk to chunks
            current_chunk = [word]  # Start a new chunk with the current word
            current_length = 1  # Reset the length for the new chunk
        else:
            current_chunk.append(word)  # Add the word to the current chunk
            current_length += 1  # Increment the current length

    if current_chunk:  # Add the last chunk if it's not empty
        chunks.append(" ".join(current_chunk))

    return chunks

# summarizes transcripts using bart using Hugging Face API
def summarize_transcript(text, max_tokens=1024):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = split_text_by_words(text, max_tokens - 200) # - 200 to give a buffer on max tokens
    
    summaries = []
    for chunk in chunks:
        print(f"Processing chunk of length: {len(chunk.split())}")
        try:
            summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            print(f"Error processing chunk: {e}")
    
    return " ".join(summaries)

# summarizes transcripts via Hugging Face cloud via Python's Request
# def summarize_transcript(transcript):

#     payload = {
#         "inputs": transcript,
#         "parameters":
#         {
#             "max_length": 50,
#             "min_length": 10,
#             "truncation": True,
#         }
#     }
#     response = requests.post(API_URL, headers=headers, json=payload)

#     return response.json()