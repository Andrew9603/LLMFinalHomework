# bge_m3_embedding.py
import ollama

def embed_text_with_bge(text: str):
    """
    使用 Ollama 的 bge-m3 模型生成文本向量。
    """
    response = ollama.embeddings(
        model="bge-m3",   # 模型名需与你 pull 的一致
        prompt=text
    )
    # 返回结构通常包含 'embedding'
    return response["embedding"]

if __name__ == "__main__":
    text = "机器学习是人工智能中最重要的领域之一。"
    embedding = embed_text_with_bge(text)

    print("Embedding length:", len(embedding))
    print("First 10 dimensions:", embedding[:10])
