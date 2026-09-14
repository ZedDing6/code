#此文件专门用于存储该项目所用到的一些配置信息，类似于头文件的作用，存放一些全局可用随意引用的全局变量
md5_path = "./md5.txt"  # 存放md5的文件路径
knowbase_name = "RAG_demo"
persist_directory = "./chroma_db"  # 数据库存储路径
embedding_model = "DashScope/CodeBERTa-small-v1"  # 向量化模型的名称
chunk_size = 1000  # 文本切分的块大小
chunk_overlap = 100  # 文本切分的重叠大小
separators = ["\n\n", "\n", " ", ""]  # 文本切分的分隔符列表，按优先级顺序进行分割
chat_model_name = "qwen-plus"  # 在线问答使用的聊天模型
session_config = {}  # 聊天链调用时使用的配置