# setup_model.py
from fastembed import TextEmbedding

print("⬇️ Downloading AI Model... (This happens only once)")

# This triggers the download safely
model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

print("✅ Model Downloaded Successfully!")
print("You can now run 'streamlit run main.py'")