# About the Project
The Federate Learning Standards are part of the [Soteria Initiative](https://soteria-initiative.org/) to establish common financial
crime AI and specifically federated learning standards and includes conventions to train, exchange and aggregate 
shared financial crime intelligence. For a technical overview consult the [technical documentation](https://deepwiki.com/SoteriaInitiative/flstandards) - auto generation courtesy of DeepWiki.

As in every interaction standards smooth the way. Imagine the <b>internet without HTML</b> and international business without
the English language. Crucially in the fight against financial crime standards help to:
- reduce costs of sharing typologies and implementing technology
- focus innovation where it matter most, such as algorithms, human investigation and support/case management
- <b>safe lives</b> because detection of suspicious activity will become more effective
- faster to respond to emerging threats as typologies and patters can be machine processed
- more resilient to individual participant failures as detection is always against a shared knowledge of patterns

Even though the current demonstration is severely limited and largely work in progress, 
the current release already highlights the power of federated learning for financial crime prevention
(metrics below are expressed in AuC - Area under the Curve):

| Bank - Detection Focus                | Local Model Detection Quality | Federated Learning Detection Quality |
|---------------------------------------|-------------------------------|--------------------------------------|
| Bank 1 - Large Cash Deposits 💰         | 0.5735             | 0.8739                          |
| Bank 2 – High-Risk Transactions 🏴‍☠️ | 0.5738                   | 0.8814                           |
| Bank 3 - Many UBOs 🤼                 | 0.6689                  | 0.8660                         |
| Bank 4 - Watchlist Entities 📋        | 0.6977                 | 0.8820                         |
> NOTE: Differences in federated learning metrics are a result of individuals transaction characteristics.

While sharing knowledge is vital, Soteria will not share actual detection patterns or models. The project
does not target the most effective detection algorithm either. We believe that there is ample opportunity
for vendors and financial institutions to design optimized systems. 

Critically, an actual collectively learned detection model is (currently) not applicable for public consumption, 
because such a model would make it far too easy for criminals to evade detection.

The Soteria federated learning standards are building on: 
- [IEEE Guide for Architectural Framework and Application of Federated Machine Learning](https://standards.ieee.org/ieee/3652.1/7453/)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/pdf/1912.04977) 
- [Soteria Data Standards](https://github.com/SoteriaInitiative/coredata)


# 🕹️ Getting started
### 1. Clone the repo
```zsh
git clone https://github.com/SoteriaInitiative/flstandards.git
cd flstandards
```

### 2. Install the required dependencies
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

You can verify the installation by typing:
```zsh
brew doctor
```

If terminal prints ``Your system is ready to brew`` everything worked OK.

</details>

### 3. Setting project configuration & credentials
 
Provide application configuration and create a service account on GCP with a JSON key that has edit permissions.
You can supply the credentials to the application in two ways:

1. **Path to key file** – Save the key in ``gcp-credentials/gcp-key.json`` (create the folder if necessary) and set ``GOOGLE_APPLICATION_CREDENTIALS`` to that path.
2. **Environment variables** – Export the individual service-account fields (``GCP_PROJECT_ID``, ``GCP_PRIVATE_KEY``\, ``GCP_CLIENT_EMAIL``\, etc.).

Create a ``.env`` file in the project root with at least the following content:
```text
NUM_ROUNDS=1
GCS_BUCKET_NAME=soteria-federated-learning
# Either provide a path to the key file
# GOOGLE_APPLICATION_CREDENTIALS=gcp-credentials/gcp-key.json
# or supply the fields directly
# GCP_PROJECT_ID=your-project
# GCP_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...
# GCP_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
```

### 4. Set the Google Cloud parameters
```zsh
gcloud auth login
gcloud config set project <PROJECT_ID>
```
Now create the storage bucket specified in the ```.env``` above (only required once):
```zsh
gcloud storage buckets create gs://soteria-federated-learning \
    --location=us-central1 \
    --default-storage-class=STANDARD

```
<details>
    <summary>💡Hint if bucket creation fails:</summary>

You may have created a bucket with the same name. Verify in the GCP console if the
bucket already exists and if it does, and you like to retain the bucket, rename the bucket 
in the ```gcloud``` command above and in the ```.env``` file.

</details>

### 5. Run synthetic data generator:

The following assumes that you are in the project root. If you run ```ls``` you should see the files listed in the
[Project Structure](#Project Structure). In that directory run:
```zsh
python app/data_generator.py
```
If Google Cloud credentials are not configured, the script still generates the
JSON files locally but skips uploading them to GCS.
Now review the synthetic data that has been generated:
```zsh
streamlit run app/app.py --server.port=8501 --server.address=127.0.0.1
```

<details>
    <summary>💡Hint how to interpret the data:</summary>

Observe that each bank detects only a small set of transaction (red) but the vast majority
of illicit transactions is not detected (yellow) because these are not part of the local knowledge/scenario pool.

</details>

### 6. Launch federated learning stack
Ensure that you have started your docker software and then run the federated learning demo:
```zsh
docker compose down --rmi all --volumes --remove-orphans
docker compose up --build --force-recreate
```
To stop the demonstration press ```ctrl-c``` once to allow for resource shutdown and twice to force the exit.
<details>
    <summary>💡Hint in case of docker issues:</summary>

If you are using multiple virtualization environments (e.g., colima) you may need to reset to the docker
socket with the below steps: 
```zsh
docker context use default
```
</details>

#### Run server and clients locally (without Docker)
If Docker is unavailable, the stack can run directly on the host. Start the server:

```zsh
NUM_ROUNDS=1 SERVER_ADDRESS=localhost:8080 python app/server.py
```

Then, in a separate shell, launch the four clients:

```zsh
for i in 1 2 3 4; do \
    SERVER_ADDRESS=localhost:8080 BANK_ID=$i python app/client.py & \
done
wait
```

Use `localhost` (not `127.0.0.1`) for `SERVER_ADDRESS` to avoid gRPC proxy errors.

### 7. Observe the model training and evaluation
A lot will scroll through the screen, especially now while the demonstration software is in its early stages. 
The guide below provides and indication what to watch out for. 
Observe specifically after the building steps have completed 
(when ```[+] Building``` becomes ```[+] Running```):
- One server (```server-1```) has been created
- Four clients (```flstandards-client1``` to ```flstandards-client4```) were created 
- The server requests local models from the simulated banks (```Requesting initial parameters```)
- The clients load the previously generated data (```Successfully downloaded data from Bank...```)
- Each client trains a local model (```Model created```)
- The server uses the first local model to initialize & start model training (```FL starting```, ```fit_round 1```)
- All the clients submit their local models (```━.../step```)
- The server completes local model collection & aggregates models (```fit_round 1 received```, ```Aggregated local training AUC```)
- The server runs a model evaluation for the first round (```evaluate_round 1```)
- Results of the aggregated loc model are printed (```Aggregated local test AUC```)
- Results of the federated learning for the global model are printed (```Aggregated global test AUC```)

You can compare the AUC for local and global model to get an indication how well the federated learning performed.

Test and training data splits are automatic and the parameter ```NUM_ROUNDS``` in the ```.env``` file controls
how many rounds of training to perform. It is set to one round as the demonstrator does not regenerate more transactions
with new detection patterns currently.


# 🗄️ Project structure
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
# 🛠️ Contributing
Contributions are welcome! To get started:

1. Fork the project. 
2. Create an issue to work on at git-hub
2. Create a new feat, doc or std branch (replace feat with doc or std): git checkout -b feat/<issue-#>-<change>. 
3. Commit your changes: git commit -m 'Commit message'. 
4. Push to your branch: git push origin feat/<issue-#>-<change>. 
5. Open a pull request in the main repository.

# 🚀 Features

This release includes the following key features:
- Synthetic data generation in alignment with [Soteria Initiative Data Standards](https://github.com/SoteriaInitiative/coredata)
- Four simulated financial institutions with unique scenario knowledge
- Example scenarios for high-risk country transaction, large deposits, watch lists and large number of UBOs
- A Flower based client/server model exchange model
- A local model training and inference client
- A central server to receive local partial models and to distribute global models for inference

# ⚠️ Limitations:
Please consider the following limitations or known issues:
- The [Soteria Initiative Data Standards](https://github.com/SoteriaInitiative/coredata) are not included as a component, but rather an integral component because of an error in the account element specification, this is targeted for separation next
- Clients currently cannot run outside the lab environment, which will be enabled in one of the next iterations
- By design the demonstrator is limited to just a few detection scenarios.
- Model limitations to perceptron and simple embeddings, as tuning this (e.g., using GNN) would be outside the standard work in scope of the initiative and more of a model implementation aspect.
- There are no differential privacy or noise insertion considerations included.
- The system is not using secured connections and encryption currently.
# 📄 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute this project as per the terms of the license.
# 📬 Contact
Project Maintainer: Soteria Initiative – @SoteriaInitiative – contact@soteria-initiative.org
Repository: SoteriaInitiative/coredata
For general inquiries or discussion, please open an issue.
