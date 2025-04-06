# About the Project
The Federate Learning Standards are part of the [Soteria Initiative](https://soteria-initiative.org/) to establish common financial
crime AI and specifically federated learning standards and includes conventions to train, exchange an aggregate 
shared financial crime intelligence.

As in every interaction standards smooth the way. Imagine the <b>internet without HTML</b> and international business without
the English language. Crucially in the fight against financial crime standards help to:
- reduce costs of sharing typologies and implementing technology
- focus innovation where it matter most, such algorithms, human investigation and support/case management
- <b>safe lives</b> because detection of suspicious activity will become more effective
- faster to respond to emerging threats as typologies and patters can be machine processed
- more resilient to individual participant failures as detection is always against a shared knowledge of patterns

While sharing knowledge is vital, Soteria will not share actual detection patterns or models. The project
does not target the most effective detection algorithm either. We believe that there is ample opportunity
for vendors and financial institutions to design optimized systems. 

Critically, an actual collectively learned detection model is (currently) not applicable for public consumption, 
because such a model would make it far too easy for criminal to evade detection.

The Soteria federated learning standards are building on: 
- [IEEE Guide for Architectural Framework and Application of Federated Machine Learning](https://standards.ieee.org/ieee/3652.1/7453/)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/pdf/1912.04977) 
- [Soteria Data Standards](https://github.com/SoteriaInitiative/coredata)


# Getting started
1. Clone the repo
```zsh
git clone https://github.com/SoteriaInitiative/flstandards.git
cd flstandards
```

2. Install the required dependencies
```zsh
brew install python
brew install --cask docker
brew install --cask google-cloud-sdk
pip install -r app/requirements.txt
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

3. Provide application configuration and create a service account on GCP and add a JSON key with edit permissions.
Safe the key to ``app/gcp-credentials/gcp-key.json`` - create the gcp-credentials folder if you don't have it.
Next, provide the proper application configurations. 
Create a ``.env`` file in the app root ``flstandards/app/`` with
the following content:
```text
NUM_ROUNDS=1
GCS_BUCKET_NAME=soteria-federated-learning
GOOGLE_APPLICATION_CREDENTIALS=app/gcp-credentials/gcp-key.json
```

4. Set the Google Cloud parameters
```zsh
gcloud auth login
gcloud config set project <PROJECT_ID>
```
Now create the storage bucket:
```zsh
gcloud storage buckets create gs://soteria-federated-learning \
    --location=us-central1 \
    --default-storage-class=STANDARD

```

5. Run synthetic data generator and review results
```bash
python app/data_generator.py
streamlit run app/app.py --server.port=8501 --server.address=127.0.0.1
```
<details>
    <summary>💡Hint how to read the data:</summary>

Observe that each bank detects only a small set of transaction (red) but the vast majority
of illicit transactions is not detected (yellow) because these are not part of the local knowledge/scenario pool.

</details>

6. Launch Federated Learning stack
```bash
docker compose down --rmi all --volumes --remove-orphans
docker compose up --build --force-recreate
```
<details>
    <summary>💡Hint in case of docker issues:</summary>

If you are using multiple virtualization environments (e.g., colima) you may need to reset to the docker
socket with the below steps: 
```zsh
docker context use default
```
</details>

# Project Structure
To find your way around please find a quick overview of the project structure.
```
flstandards/
├── app/                        # Example federated learning model implementation
├── gcp-credentials/            # Credentials for Google Cloud (you may need to create the folder)
├── documentation/              # Use cases & design documentation
├── standard/                   # Standard specification
├── README.md                   # This file
└── LICENSE                     # License file
```
# Contributing
Contributions are welcome! To get started:

1. Fork the project. 
2. Create a new feature branch: git checkout -b feature/<new-feature>. 
3. Commit your changes: git commit -m 'Add some feature'. 
4. Push to your branch: git push origin feature/<new-feature>. 
5. Open a Pull Request in the main repository.
# License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute this project as per the terms of the license.
# Contact
Project Maintainer: Soteria Initiative – @SoteriaInitiative – contact@soteria-initiative.org
Repository: SoteriaInitiative/coredata
For general inquiries or discussion, please open an issue.
