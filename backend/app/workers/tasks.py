from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.upload import Upload
from app.models.message import Message
from app.core.config import settings
import pandas as pd
import os
import subprocess
from datetime import datetime

@celery_app.task(acks_late=True)
def parse_upload(upload_id: str, file_path: str):
    print(f"Start parsing upload {upload_id} from {file_path}")
    
    db = SessionLocal()
    try:
        # Simple parsing logic
        data = []
        
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            # Normalize columns
            if 'content' in df.columns:
                data = df.to_dict('records')
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Try to parse standard WeChat format: "SenderName: Message" or "Time SenderName: Message"
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Heuristic split
                if ':' in line:
                    parts = line.split(':', 1)
                    sender = parts[0].strip()
                    content = parts[1].strip()
                    data.append({
                        'sender': sender,
                        'content': content,
                        'timestamp': datetime.now()
                    })
                else:
                    # Treat whole line as content from 'Unknown'
                    data.append({
                        'sender': 'System',
                        'content': line,
                        'timestamp': datetime.now()
                    })
        
        # Save to DB
        for item in data:
            msg = Message(
                upload_id=upload_id,
                sender=item.get('sender', 'Unknown'),
                content=item.get('content', ''),
                timestamp=item.get('timestamp', datetime.now()),
                role='user' 
            )
            db.add(msg)
        
        # Update Upload status
        upload = db.query(Upload).filter(Upload.id == upload_id).first()
        if upload:
            upload.status = "parsed"
            
        db.commit()
        print(f"Finished parsing upload {upload_id}. Parsed {len(data)} messages.")
        return {"status": "completed", "message_count": len(data)}
        
    except Exception as e:
        print(f"Error parsing: {e}")
        db.rollback()
        
        # Update status to failed
        upload = db.query(Upload).filter(Upload.id == upload_id).first()
        if upload:
            upload.status = "failed"
            db.commit()
            
        return {"status": "failed", "error": str(e)}
    finally:
        db.close()

@celery_app.task(acks_late=True)
def train_model(dataset_id: str, config: dict):
    print(f"Start training with dataset {dataset_id} using base model {settings.OLLAMA_BASE_MODEL}")
    
    # 1. Create Modelfile content
    # In a real scenario, extract system prompt from data analysis
    model_suffix = dataset_id[:8]
    new_model_name = f"wechat-finetune-{model_suffix}"
    
    modelfile_content = f"""
FROM {settings.OLLAMA_BASE_MODEL}
SYSTEM "You are a specialized assistant trained on WeChat chat history. You mimic the tone and style found in the dataset."
PARAMETER temperature 0.7
"""
    
    # 2. Save Modelfile
    if not os.path.exists(settings.LOCAL_STORAGE_PATH):
        os.makedirs(settings.LOCAL_STORAGE_PATH)
        
    modelfile_path = os.path.join(settings.LOCAL_STORAGE_PATH, f"{new_model_name}.Modelfile")
    
    with open(modelfile_path, "w", encoding="utf-8") as f:
        f.write(modelfile_content)
        
    # 3. Run Ollama Create
    print(f"Running ollama create {new_model_name} -f {modelfile_path}")
    try:
        result = subprocess.run(
            ["ollama", "create", new_model_name, "-f", modelfile_path], 
            capture_output=True, 
            text=True,
            check=True
        )
        print(f"Ollama create output: {result.stdout}")
        
        return {"model_id": new_model_name, "status": "completed"}
    except subprocess.CalledProcessError as e:
        print(f"Ollama create failed: {e.stderr}")
        # If model already exists, we might want to remove it first, but for now just fail
        return {"status": "failed", "error": e.stderr}
    except FileNotFoundError:
         print("Ollama executable not found in PATH")
         return {"status": "failed", "error": "Ollama not found"}
