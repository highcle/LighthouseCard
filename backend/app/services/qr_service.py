from sqlalchemy.orm import Session
from ..models.lighthouse import Lighthouse


def identify_lighthouse_by_url(db: Session, url: str) -> Lighthouse | None:
    """QRコードのURLから灯台を特定する。完全一致→部分一致の順で試みる。"""
    lighthouses = db.query(Lighthouse).filter(Lighthouse.qr_url_pattern.isnot(None)).all()
    for lh in lighthouses:
        if lh.qr_url_pattern and lh.qr_url_pattern in url:
            return lh
    # jcg_page_url でも試みる
    for lh in lighthouses:
        if lh.jcg_page_url and lh.jcg_page_url in url:
            return lh
    return None
