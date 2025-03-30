## Generate data and launch Streamlit App

```bash
source venv/bin/activate
python app/data_generator.py
streamlit run app/app.py --server.port=8501 --server.address=0.0.0.0
```

## Launch FL learning
```bash
docker compose down --rmi all --volumes --remove-orphans
docker compose up --build --force-recreate
```

## Jupyter notebook
```bash
jupyter notebook --allow-root & 
```