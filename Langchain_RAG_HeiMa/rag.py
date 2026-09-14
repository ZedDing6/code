from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from file_history_store import get_history
from operator import itemgetter


class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            DashScopeEmbeddings(model=config.embedding_model)
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "你是一个知识库问答机器人，你的任务是根据用户的问题和知识库中的内容，给出准确的答案。"
                    "参考资料：{context}"
                 ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "请回答用户提问：{input}"   ),
            ]
        )
        self.chat_model = ChatTongyi(model=config.chat_model_name)
        self.chain = self.__get_chain()
    def __get_chain(self):
        #获取最终的执行链
        retriever = self.vector_service.get_retriever()

        def format_documents(documents):
            if not documents:
                return "没有找到相关的参考资料。"
            formatted_docs_str = ""
            # 格式化检索到的文档内容
            for docu in documents:
                formatted_docs_str+=f"文档内容：{docu.page_content}\n文档元数据：{docu.metadata}\n\n"
            return formatted_docs_str
        chain = ({
            "input": itemgetter("input"),
            "context": itemgetter("input") | retriever | format_documents,
            "chat_history": itemgetter("chat_history"),
        }) | self.prompt_template | self.chat_model | StrOutputParser()
        return RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

if __name__ == "__main__":
    rag_service = RagService()
    question = "请问如何使用Langchain实现RAG？"
    answer = rag_service.chain.invoke({"input":question})
    print(answer)

        