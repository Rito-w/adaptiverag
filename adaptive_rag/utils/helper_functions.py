import os
import yaml

def load_yaml_config(file_path: str) -> dict:
    """
    加载 YAML 配置文件。

    Args:
        file_path (str): YAML 文件的路径。

    Returns:
        dict: 加载的配置字典。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found at: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_project_root() -> str:
    """
    获取项目根目录的绝对路径。
    假设项目根目录是包含此函数所在文件（或其父目录）的顶层目录。
    """
    # 假设 adaptive_rag 位于 rag_project/adaptive_rag
    # 那么项目根目录就是 rag_project
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 向上两级目录到达 rag_project/
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    return project_root

# 其他辅助函数，例如：
# def calculate_cosine_similarity(vec1, vec2):
#     # 实现余弦相似度计算
#     pass

# def chunk_text(text: str, chunk_size: int, overlap: int):
#     # 实现文本分块逻辑
#     pass 