"""基于streamlit实现网页端基础服务
运行有点不一样，不是直接在python里面运行，而是需要在终端运行
python -m streamlit run app_file_uploader.py
因为 Streamlit 应用需要由 streamlit run 启动。
"""
import io

import streamlit as st
from pypdf import PdfReader
from docx import Document
from knowbase import KnowledgeBaseService


st.title("知识库更新服务")

# file_uploader，这里的最后一个参数指的是是否支持批量上传
files = st.file_uploader(
    "上传文件",
    type=["txt", "pdf", "docx"],
    accept_multiple_files=True,
)
#session_state是一个单独可以长期存在维护的状态字典，意味着
#不管web咋样，这个服务是单独存在，并且创建后不会消失的，如果不引入session_state，那么这个对象就会因为每一次页面刷新而代码重新执行导致重新创建一次
if "service" not in st.session_state:
    
    st.session_state.service = KnowledgeBaseService()

if files:
    for uploaded_file in files:
        # 获取文件名、类型和大小
        file_name = uploaded_file.name
        file_type = uploaded_file.type
        file_size = uploaded_file.size / 1024

        st.subheader(file_name)
        st.write(f"文件类型：{file_type}，文件大小：{file_size:.2f} KB")

        # 获取文件内容：不同类型的文件需要使用不同的读取方式
        if file_name.endswith(".txt"):
            content = uploaded_file.getvalue().decode("utf-8")

        elif file_name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            content = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        elif file_name.endswith(".docx"):
            document = Document(io.BytesIO(uploaded_file.getvalue()))
            content = "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

        st.write(content)
        result = st.session_state.service.upload_file(content, file_name)
        st.write(result)