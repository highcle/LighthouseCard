from sqlalchemy.orm import Session
from ..models.lighthouse import Lighthouse

# 海上保安庁の灯台カードURLの共通パス
_JCG_CARD_PATH = "kaiho.mlit.go.jp/info/lighthouse/card/"


def is_jcg_card_url(url: str) -> bool:
    """スキャンしたURLが海上保安庁の灯台カードURLかどうかを判定する。"""
    return _JCG_CARD_PATH in url


def identify_lighthouse_by_url(db: Session, url: str) -> tuple[Lighthouse | None, bool]:
    """
    QRコードのURLから灯台を特定する。

    Returns:
        (Lighthouse, True)  : 灯台が特定できた
        (None, True)        : 海保の灯台カードURLだがDBに未登録
        (None, False)       : 灯台カードとは無関係のURL
    """
    is_jcg = is_jcg_card_url(url)

    # qr_code_url と完全一致で照合（末尾スラッシュ・空白を正規化）
    normalized = url.strip().rstrip("/")
    lighthouses = db.query(Lighthouse).filter(Lighthouse.qr_code_url.isnot(None)).all()
    for lh in lighthouses:
        if lh.qr_code_url and lh.qr_code_url.strip().rstrip("/") == normalized:
            return lh, True

    return None, is_jcg
