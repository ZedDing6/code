from langchain_chroma import Chroma
import config_data as config

class VectorStoreService(object):
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vector_store = Chroma(
            collection_name=config.knowbase_name,  # 数据库的名字
            embeddings=self.embedding_model,  # 使用的向量化模型
            persist_directory=config.persist_directory,  # 数据库存储路径
        )
    def get_retriever(self):
        # 获取向量存储的检索器
        return self.vector_store.as_retriever(search_kwargs={"k": 3})  # 设置检索的结果数量为3

if __name__ == "__main__":
    # 测试代码
    from langchain_community.embeddings import DashScopeEmbeddings

    embedding_model = DashScopeEmbeddings(model=config.embedding_model)
    vector_store_service = VectorStoreService(embedding_model)
    retriever = vector_store_service.get_retriever()
    print(retriever)

    