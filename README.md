# rls-graphrag

This repository contains tools and scripts for using GraphRAG on your own custom CSV files, specifically designed to run on a free T4 instance offered by Google Colab.

## Cloning the Repository
To get started, clone the repository using the following command:
```
!git clone https://github.com/hcss-utils/rls-graphrag.git
```

## Setup
Install and run ollama:
```
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

Next, pull the base model required for your tasks (define it in [`./rls/settings.yaml`](./rls/settings.yaml)):
```
ollama pull llama3.1:8b
```

Then, create a new model with a higher `num_ctx` parameter (by default ollama uses 2048, but we need more than that-follow [this](https://github.com/ollama/ollama/issues/5965#issuecomment-2252354726) comment).
```
ollama show --modelfile llama3.1:8b > Modelfile
# edit the file, e.g. using vim
ollama create -f Modelfile custom-model
ollama rm llama3.1:8b
ollama run custom-model
```

Embedding model:
```
ollama pull nomic-embed-text
```

## GraphRAG
Indexing:
```
python -m graphrag.index --root ./rls
```
