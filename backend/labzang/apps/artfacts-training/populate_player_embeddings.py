from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
# ?„ì—??ë§Œë“  ëª¨ë¸??import
from labzang.apps.soccer.models.bases import (
    PlayerEmbedding,
    TeamEmbedding,
    Player,
)

engine = create_engine("postgresql+psycopg://user:pass@host/dbname")
SessionLocal = sessionmaker(bind=engine)

embedder = KoElectraEmbeddings("./koelectra_orchestrator_finetuned")

def populate_player_embeddings():
    with SessionLocal() as db:
        players = db.query(Player).all()  # Player ëª¨ë¸ ê°€??        for player in tqdm(players):
            # content ì¡°í•© (?¹ì‹ ???í•˜???€ë¡?
            content = f"{player.player_name}, {player.e_player_name}, {player.position}, {player.nation}, ?±ë²ˆ??{player.back_no}, {player.nickname}"
            if not content.strip():
                continue

            embedding = embedder.embed_query(content)

            existing = db.query(PlayerEmbedding).filter_by(player_id=player.id).first()
            if existing:
                # ?…ë°?´íŠ¸?˜ê±°???¤í‚µ
                continue

            emb_record = PlayerEmbedding(
                player_id=player.id,
                content=content,
                embedding=np.array(embedding)
            )
            db.add(emb_record)
        db.commit()

# teams, schedules, stadiums???™ì¼ ?¨í„´?¼ë¡œ
