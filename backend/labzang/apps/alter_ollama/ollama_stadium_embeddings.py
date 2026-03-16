from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from pathlib import Path

model_path = "artifacts/base-models/exaone-2.4b"
output_file = "app/domain/v1/soccer/models/bases/stadium_embeddings.py"

# stadiums.py ?Œì¼ ?½ê¸°
stadiums_file = Path("app/domain/v1/soccer/models/bases/stadiums.py")
stadiums_content = stadiums_file.read_text(encoding="utf-8")

# ?„ë¡¬?„íŠ¸ ?‘ì„±
prompt = f"""?¤ìŒ SQLAlchemy Stadium ëª¨ë¸??ì°¸ê³ ?˜ì—¬ StadiumEmbedding ORM ?´ë˜?¤ë? ?‘ì„±?˜ì„¸??

=== Stadium ëª¨ë¸ ì½”ë“œ ===
{stadiums_content}

=== Alembic ë§ˆì´ê·¸ë ˆ?´ì…˜ ?Œì´ë¸??¤í‚¤ë§?===
?Œì´ë¸”ëª…: stadium_embeddings
ì»¬ëŸ¼:
- id: BigInteger, PK, autoincrement=True, nullable=False, comment='?„ë² ???ˆì½”??ê³ ìœ  ?ë³„??
- stadium_id: BigInteger, FK -> stadiums.id, nullable=False, ondelete='CASCADE', comment='ê²½ê¸°??ID'
- content: Text, nullable=False, comment='?„ë² ???ì„±???¬ìš©???ë³¸ ?ìŠ¤??
- embedding: Vector(768), nullable=False, comment='768ì°¨ì› ?„ë² ??ë²¡í„° (KoElectra)'
- created_at: TIMESTAMP(timezone=True), server_default=now(), nullable=False, comment='?ˆì½”???ì„± ?œê°„'

=== ?”êµ¬?¬í•­ ===
1. Base ?´ë˜?? from labzang.shared.bases import Base ?¬ìš©
2. pgvector: from pgvector.sqlalchemy import Vector ?¬ìš©
3. SQLAlchemy imports: Column, BigInteger, Text, ForeignKey, TIMESTAMP, relationship
4. ?€?„ìŠ¤?¬í”„: from sqlalchemy.sql import func ?¬ìš©?˜ì—¬ server_default=func.now() ?¤ì •
5. relationship: stadium (back_populates="embeddings") ?¤ì •
6. stadiums.py??ì½”ë”© ?¤í??¼ê³¼ ?¼ê???? ì? (ì£¼ì„ ?•ì‹, Column ?•ì˜ ë°©ì‹ ??
7. ëª¨ë“  Column??comment ì¶”ê?
8. __tablename__ = "stadium_embeddings" ?¬ìš©
9. Python ì½”ë“œë§?ì¶œë ¥ (ì£¼ì„?´ë‚˜ ?¤ëª… ?†ì´ ?œìˆ˜ ì½”ë“œë§?
10. docstring?€ Stadium ëª¨ë¸ê³?? ì‚¬???•ì‹?¼ë¡œ ?‘ì„±

=== ì¶œë ¥ ?•ì‹ ===
?Œì¼ ?„ì²´ ì½”ë“œë¥?ì¶œë ¥?˜ì„¸?? import ë¬¸ë????œì‘?˜ì—¬ ?„ì „??Python ?Œì¼ ?•íƒœë¡??‘ì„±?˜ì„¸??"""

# ëª¨ë¸ ë¡œë“œ
print("[ExaOne] ëª¨ë¸ ë¡œë”© ì¤?..")
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

print("[ExaOne] ì½”ë“œ ?ì„± ì¤?..")
# ExaOne ëª¨ë¸??chat template ?¬ìš© (ê¶Œì¥ ë°©ì‹)
messages = [
    {
        "role": "system",
        "content": "You are EXAONE model from LG AI Research, a helpful assistant specialized in generating Python SQLAlchemy ORM code."
    },
    {
        "role": "user",
        "content": prompt
    }
]

input_ids = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)

outputs = model.generate(
    input_ids,
    max_new_tokens=1200,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.pad_token_id
)

# ?ì„±??ì½”ë“œ ì¶”ì¶œ
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# ?‘ë‹µ?ì„œ ?¬ìš©???„ë¡¬?„íŠ¸ ë¶€ë¶??œê±° (chat template ?¬ìš© ??
if "assistant" in generated_text.lower() or "?µë?" in generated_text:
    # chat template ?‘ë‹µ?ì„œ ?¤ì œ ì½”ë“œ ë¶€ë¶„ë§Œ ì¶”ì¶œ
    if "```python" in generated_text:
        code_start = generated_text.find("```python") + 9
        code_end = generated_text.find("```", code_start)
        if code_end != -1:
            generated_code = generated_text[code_start:code_end].strip()
        else:
            generated_code = generated_text[code_start:].strip()
    elif "```" in generated_text:
        code_start = generated_text.find("```") + 3
        code_end = generated_text.find("```", code_start)
        if code_end != -1:
            generated_code = generated_text[code_start:code_end].strip()
        else:
            generated_code = generated_text[code_start:].strip()
    else:
        # assistant ?‘ë‹µ ë¶€ë¶„ë§Œ ì¶”ì¶œ
        if "assistant" in generated_text.lower():
            parts = generated_text.split("assistant", 1)
            if len(parts) > 1:
                generated_code = parts[-1].strip()
            else:
                generated_code = generated_text
        else:
            generated_code = generated_text
else:
    generated_code = generated_text

print("\n=== ?ì„±??ì½”ë“œ ===")
print(generated_code)
print("\n=== ì½”ë“œ ?ì„± ?„ë£Œ ===\n")

# ?Œì¼???€??output_path = Path(output_file)
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(generated_code, encoding="utf-8")

print(f"[?„ë£Œ] ì½”ë“œê°€ {output_file}???€?¥ë˜?ˆìŠµ?ˆë‹¤.")

