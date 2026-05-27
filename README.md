# funathon-project2
Repository of the 2nd funathon project (NLP)

Subject's website deployed here : https://aiml4os.github.io/funathon-project2/

$ uv sync

# simple run file not alvays working ..
$ uv run lk-ml-py
# working enstead ..


## Environment

You will have to create and fill a `.env` file to manage your connections (qdrant, llm.lab, etc.).
You can use this template to make it easier : 

```txt
QDRANT_URL=https://YOURNAMESPACE-qdrant.user.lab.sspcloud.fr/
QDRANT_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
QDRANT_API_PORT=443
LLMLAB_API_KEY=xxxxxxxxxxxxxxxxxxxxxx
LLMLAB_URL=https://llm.lab.sspcloud.fr/api
MLFLOW_TRACKING_URI=<add the MLflow server URL> (ex: ``https://projet-funathon-mlflow.user.lab.sspcloud.fr/``)
MLFLOW_TRACKING_USERNAME=<add your username>
MLFLOW_TRACKING_PASSWORD=<add your password>
```
MLflow credentials are given in the panel that opens when you launch the MLflow service on the SSPCloud.

MLFLOW_TRACKING_URI=https://user-kshlkosztya-mlflow.user.lab.sspcloud.fr/
MLFLOW_TRACKING_USERNAME=...kshlkosztya
MLFLOW_TRACKING_PASSWORD=t5xybc62v??egeyvx2h2cf

