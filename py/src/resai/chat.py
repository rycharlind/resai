from langchain_community.llms import OpenAI
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo,
)
from resai.pgutil import get_vector_db

def ask_collection(collection_name: str, prompt: str):
    llm = OpenAI(temperature=0)
    db = get_vector_db(collection_name)

    agent = create_vectorstore_agent(
        llm=llm,
        toolkit=VectorStoreToolkit(vectorstore_info=VectorStoreInfo(
            name=collection_name,
            description=f"{collection_name} vector toolkit",
            vectorstore=db
        )),
        verbose=True
    )

    return f"{agent.run(prompt)}"