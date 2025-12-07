# call_ollama_models.py
# 说明：确保 ollama 服务已用 `ollama serve` 启动，并且你已经 pull 了模型

import ollama
import time

def call_model_once(model_name: str, prompt: str):
    """
    同步调用示例（一次性返回）。
    返回字典 response，内容结构取决于 ollama 版本；通常 response['message']['content'] 包含生成文本。
    """
    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": prompt},
            ],
            # 可选参数：max_tokens, temperature, stop 等
            max_tokens=512,
            temperature=0.1,
        )
        # 兼容不同版本的返回结构
        content = None
        if isinstance(response, dict):
            # 新版通常是 response['message']['content']
            content = response.get("message", {}).get("content")
            # 旧版也可能直接有 response['content'] 或者 response['choices']
        print(f"Model {model_name} response:\n{content}\n")
        return content
    except Exception as e:
        print(f"Error calling {model_name}: {e}")
        raise

def stream_model_output(model_name: str, prompt: str):
    """
    流式调用示例（如果客户端支持流式）。这里用生成器风格演示（具体 API 以 ollama 版本为准）。
    """
    print(f"Streaming from {model_name} ...")
    try:
        # 部分 ollama-python 版本支持 streaming=True + callback 或返回可迭代对象。
        # 下面示例展示了常见的两种写法（任选其一，取决于你安装的 ollama 版本）。
        # 1) 若 chat 返回一个可迭代的事件流：
        stream = ollama.chat(
            model=model_name,
            messages=[{"role":"user","content":prompt}],
            stream=True,   # 注意：只有部分版本支持
            temperature=0.1
        )
        # 如果 stream 是个迭代器（每次产出片段）
        for chunk in stream:
            # chunk 的具体字段也依赖版本（示例中假设 chunk['delta'] 或 chunk['message']）
            if isinstance(chunk, dict):
                # 优先打印常见字段
                delta = chunk.get("delta") or chunk.get("message", {}).get("content")
                print(delta, end="", flush=True)
            else:
                print(chunk, end="", flush=True)
        print("\n-- end stream --")
    except TypeError:
        # 如果当前客户端不支持 stream 参数，会抛出 TypeError
        print("This ollama client version may not support stream=True; falling back to single-call.")
        call_model_once(model_name, prompt)
    except Exception as e:
        print("Streaming error:", e)

if __name__ == "__main__":
    # 替换为你实际的模型名（用 'ollama list' 确认）
    codegeex_model = "codegeex4:9b"
    qwen_model = "qwen2.5-1m:7b"  # 或 "qwen2.5:7b" 等，按实际 pull 的名字写

    # 示例 prompt（针对代码生成）
    prompt_code = "Implement a Python function that computes fibonacci numbers iteratively and returns a list of first n Fibonacci numbers. Add docstring and a short usage example."

    # 1) 同步调用 CodeGeeX
    print("== Call CodeGeeX (sync) ==")
    call_model_once(codegeex_model, prompt_code)

    time.sleep(1)

    # 2) 流式调用 Qwen（若支持）
    prompt_text = "Explain in simple terms what gradient descent is and provide a short Python example."
    print("== Stream Qwen (or fallback to sync) ==")
    stream_model_output(qwen_model, prompt_text)
