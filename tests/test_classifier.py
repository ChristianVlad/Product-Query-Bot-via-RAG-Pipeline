from app.utils.query_classifier import is_product_query
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

def test_product_query_true():
    assert is_product_query("What is the price of the Zubale Fit Band 2?") is True

def test_product_query_false():
    assert is_product_query("How do I solve a quadratic equation?") is False

