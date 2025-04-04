## Getting started

First install python, Docker CLI and gcloud tools:

```zsh
brew install python
brew install --cask docker
brew install --cask google-cloud-sdk
```

<details>
    <summary>💡Hint if you don't have 'brew':</summary>

If you do not have the ``brew`` tool installed, open a terminal
window and type: 
```zsh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

If you are using an Intel Mac computer type the following after the installation:
```zsh
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```

If you are using an Apple Silicon (M1, M2, etc.) computer type the following after the installation:
```zsh
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

You can verify the instalation by typing:
```zsh
brew doctor
```

If terminal prints ``Your system is ready to brew`` everything worked OK.

</details>

Before you continue, create a service account on GCP and add a JSON key with edit permissions.
Safe the key to ``gcp-credentials/gcp-key.json`` - create the gcp-credentials folder if you don't have it.

Next, provide the proper application configurations. 
Create a ``.env`` file in the app root ``flstandards/app/`` with
the following content:
```text
NUM_ROUNDS=1
GCS_BUCKET_NAME=soteria-federated-learning
GOOGLE_APPLICATION_CREDENTIALS=app/gcp-credentials/gcp-key.json
```

Finally set the corect Google Cloud parameters:
```zsh
gcloud auth login
gcloud config set project <PROJECT_ID>
```

## Generate data and launch Streamlit App

First generate some synthentic data and review the data that has been generated with
the command below:
```bash
python app/data_generator.py
streamlit run app/app.py --server.port=8501 --server.address=127.0.0.1
```

Observe that each bank detections only a small set of transactiosn (red) but the vast majority
of illicit transactions isnot detected (yellow) because these are not part of the local knowledge/scenario pool.

## Launch Federated Learning stack
```bash
docker compose down --rmi all --volumes --remove-orphans
docker compose up --build --force-recreate
```

<details>
    <summary>💡Hint incase of docker issues:</summary>

If you are using multiple virtualization environments (e.g., colima) you may need to reset to the docker
socket with the below steps: 
```zsh
docker context use default
```
</details>


## Jupyter notebook
```bash
jupyter notebook --allow-root & 
```