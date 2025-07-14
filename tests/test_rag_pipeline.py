import importlib
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace


def setup_fake_langchain():
    # Fake langchain_community.document_loaders
    doc_mod = ModuleType('langchain_community.document_loaders')
    class FakeLoader:
        def __init__(self, path, glob=None):
            pass
        def load(self):
            return [SimpleNamespace(page_content="doc1")]
    doc_mod.DirectoryLoader = FakeLoader
    sys.modules['langchain_community.document_loaders'] = doc_mod

    # Fake langchain.text_splitter
    split_mod = ModuleType('langchain.text_splitter')
    class FakeSplitter:
        def __init__(self, chunk_size=0, chunk_overlap=0):
            pass
        def split_documents(self, docs):
            return docs
    split_mod.RecursiveCharacterTextSplitter = FakeSplitter
    sys.modules['langchain.text_splitter'] = split_mod

    # Fake langchain.vectorstores
    vec_mod = ModuleType('langchain.vectorstores')
    class FakeFAISS:
        @classmethod
        def from_documents(cls, chunks, embeddings):
            return {'chunks': chunks, 'embeddings': embeddings}
    vec_mod.FAISS = FakeFAISS
    sys.modules['langchain.vectorstores'] = vec_mod

    # Fake langchain_openai
    emb_mod = ModuleType('langchain_openai')
    class FakeEmbeddings:
        def __init__(self, openai_api_key=None):
            self.key = openai_api_key
    emb_mod.OpenAIEmbeddings = FakeEmbeddings
    sys.modules['langchain_openai'] = emb_mod

    # Fake dotenv
    dotenv_mod = ModuleType('dotenv')
    def load_dotenv():
        pass
    dotenv_mod.load_dotenv = load_dotenv
    sys.modules['dotenv'] = dotenv_mod


def test_load_index_returns_vectorstore(monkeypatch):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    setup_fake_langchain()
    rag_module = importlib.import_module('learnbot.rag_pipeline')
    importlib.reload(rag_module)

    db = rag_module.load_index(openai_api_key='abc')
    assert db['chunks'][0].page_content == 'doc1'
    assert db['embeddings'].key == 'abc'


