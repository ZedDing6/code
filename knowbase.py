"""知识库管理服务
通过md5进行管理的好处就是效率，无论对比的文档内容多大，
只要内容完全一样，计算出来的都是32位的完全一样的结果，
非常的高效
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str:str):
    #检查传入的字符串的md5是否已经存在
    if not os.path.exists(config.md5_path):
        open(config.md5_path, "w",encoding="utf-8").close()  # 如果文件不存在，则创建一个空文件
        return False
    for line in open(config.md5_path, "r",encoding="utf-8").readlines():
        line = line.strip()#处理字符串前后的空格和回车
        if line == md5_str:
            return True
    return False

def save_md5(md5_str:str):
    #保存传入的字符串的md5
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")
def get_md5(input:str,encoding='utf-8'):
    #获取传入的字符串的md5
    
    #将字符串转换为bytes字节数组
    byte_array = input.encode(encoding)
    #创建md5对象
    md5_obj = hashlib.md5()
    md5_obj.update(byte_array)#更新内容，传入即将要转换的字节数组
    md5_hexdigest = md5_obj.hexdigest()#得到md5的16进制字符串
    return md5_hexdigest

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)  # 确保数据库存储路径存在,如果不存在则创建一个
        self.chroma = Chroma(
            collection_name=config.knowbase_name,#数据库的名字
            embeddings=DashScopeEmbeddings(model=config.embedding_model),#使用的向量化模型
            persist_directory=config.persist_directory,#数据库的存储路径
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,#分割后的文本最大长度
            chunk_overlap=config.chunk_overlap,#分割最大支持的重叠字符数
            separators=config.separators,  # 分隔符列表，按优先级顺序进行分割
            length_function=len,  # 使用内置的len函数计算文本长度
        )   

    def upload_file(self, data,file_name):
        #将上传文件进行向量化，存入数据库中
        #先计算文件的md5值，判断是否已经存在，如果存在则不进行存储
        md5_hex = get_md5(data)

        if check_md5(md5_hex):
            print(f"文件 {file_name} 已经存在，跳过存储。")
            return False
        #将文件内容进行切分,逻辑是，只有超过切分阈值，才需要切分
        if len(data) > config.chunk_size:
            chunks : list[str]= self.spliter.split_text(data)
        else:
            chunks : list[str] = [data]

        metadatas = {
            "source": file_name,
            "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }    

        self.chroma.add_texts(chunks,metadatas=[metadatas for _ in chunks])#将切分后的文本存入数据库中
        save_md5(md5_hex)#将文件的md5值存入md5.txt中
        return "内容已经成功存储到数据库中"
# if __name__ == "__main__":
#     #测试md5的功能
#     test_str = "Hello, World!"
#     md5_str = get_md5(test_str)
#     print(f"MD5 of '{test_str}': {md5_str}")

#     if check_md5(md5_str):
#         print("MD5 already exists.")
#     else:
#         print("MD5 does not exist. Saving...")
#         save_md5(md5_str)
#         print("MD5 saved.")