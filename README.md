# About the Project
The Federate Learning Standards are part of the [Soteria Initiative](https://soteria-initiative.org/) to establish common financial
crime AI and specifically federated learning standards and includes conventions to train, exchange an aggregate 
shared financial crime intelligence.

As in every interaction standards smooth the way. Imagine the <b>internet without HTML</b> and international business without
the English language. Crucially in the fight against financial crime standards help to:
- keep costs down
- focus innovation where it matter most
- <b>safe lives</b> because detection of suspicious activity will become more effective<
- faster to respond to emerging threats
- more resilient to individual participant failures

With so many reasons....


- Data Standards
- FL standads

The standards are a minimum set of data elements for the objective but build on
existing more comprehensive definitions such as:
- [Financial Market Standard Body Customer Onboarding Standard](https://fmsb.com/wp-content/uploads/2024/12/20241217_Standard-for-COB_FINAL.pdf)
- [SWIFT ISO 20022 Messaging Standard](https://www2.swift.com/knowledgecentre/publications/iso_20022_fnc_instit_get_st/4.0?topic=technical-implementation.htm) (free account required)

To make the standards useful synthetic data generators will be provided and a reference
implementation of a data editor will allow the encoding of actual financial crime patterns.


# Getting started
1. Clone the repo
```zsh
git clone https://github.com/SoteriaInitiative/coredata.git
cd coredata
```

2. Install the required dependencies
```zsh
brew install python
brew install --cask docker
brew install --cask google-cloud-sdk
pip install -r requirements.txt
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
Safe the key to ``gcp-credentials/gcp-key.json`` - create the gcp-credentials folder if you don't have it.
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

5. Run synthetic data generator and review results
```bash
python app/data_generator.py
streamlit run app/app.py --server.port=8501 --server.address=127.0.0.1
```
<details>
    <summary>💡Hint how to read the data:</summary>

Observe that each bank detections only a small set of transactiosn (red) but the vast majority
of illicit transactions is not detected (yellow) because these are not part of the local knowledge/scenario pool.

</details>

6. Launch Federated Learning stack
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

# Project Structure
To find your way around please find a quick overview of the project structure.
```
coredata/
├── documentation/              # Standard design documentation
├── example/                    # Example dataset implementing the standard
├── implementation/             # Example data generator and pattern editor
├── standard                    # Standard specification
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
