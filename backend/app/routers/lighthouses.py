from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..models.lighthouse import Lighthouse
from ..models.user_card import UserCard
from ..models.user import User
from ..schemas.lighthouse import LighthouseResponse, LighthouseListResponse, IdentifyByUrlRequest, RegisterFromQrRequest
from ..core.security import decode_token
from ..services.qr_service import identify_lighthouse_by_url
from ..services.jcg_scraper import scrape_jcg_lighthouse_page

router = APIRouter(prefix="/lighthouses", tags=["lighthouses"])
bearer_scheme = HTTPBearer(auto_error=False)
bearer_scheme_required = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme_required),
    db: Session = Depends(get_db),
) -> User:
    from fastapi import status as http_status
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="無効なトークンです")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="ユーザーが見つかりません")
    return user


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if not credentials:
        return None
    payload = decode_token(credentials.credentials)
    if not payload:
        return None
    return db.query(User).filter(User.id == payload.get("sub")).first()


def to_response(lh: Lighthouse, user: Optional[User], db: Session) -> LighthouseResponse:
    is_collected = None
    if user:
        card = db.query(UserCard).filter(
            UserCard.user_id == user.id, UserCard.lighthouse_id == lh.id
        ).first()
        is_collected = card is not None
    data = LighthouseResponse.model_validate(lh)
    data.is_collected = is_collected
    return data


@router.get("", response_model=LighthouseListResponse)
def list_lighthouses(
    region: Optional[str] = Query(None),
    prefecture: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    collected: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    query = db.query(Lighthouse)
    if region:
        query = query.filter(Lighthouse.region == region)
    if prefecture:
        query = query.filter(Lighthouse.prefecture == prefecture)
    if q:
        query = query.filter(Lighthouse.name.contains(q))
    if collected is not None and user:
        collected_ids = [uc.lighthouse_id for uc in db.query(UserCard).filter(UserCard.user_id == user.id).all()]
        if collected:
            query = query.filter(Lighthouse.id.in_(collected_ids))
        else:
            query = query.filter(Lighthouse.id.notin_(collected_ids))

    lighthouses = query.order_by(Lighthouse.id).all()
    items = [to_response(lh, user, db) for lh in lighthouses]
    return LighthouseListResponse(items=items, total=len(items))


@router.get("/{lighthouse_id}", response_model=LighthouseResponse)
def get_lighthouse(
    lighthouse_id: int,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    lh = db.query(Lighthouse).filter(Lighthouse.id == lighthouse_id).first()
    if not lh:
        raise HTTPException(status_code=404, detail="灯台が見つかりません")
    return to_response(lh, user, db)


@router.post("/identify-by-url", response_model=LighthouseResponse)
def identify_by_url(
    body: IdentifyByUrlRequest,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    lh, is_jcg = identify_lighthouse_by_url(db, body.url)
    if lh:
        if lh.qr_code_url is None:
            lh.qr_code_url = body.url.strip()
            db.commit()
        return to_response(lh, user, db)
    if is_jcg:
        scraped = scrape_jcg_lighthouse_page(body.url)
        name = scraped.get("name")
        card_image_url = scraped.get("card_image_url")
        if name:
            existing = db.query(Lighthouse).filter(Lighthouse.name == name).first()
            if existing:
                existing.qr_code_url = body.url.strip()
                if card_image_url and not existing.card_image_url:
                    existing.card_image_url = card_image_url
                db.commit()
                return to_response(existing, user, db)
            new_lh = Lighthouse(
                name=name,
                region="不明",
                prefecture="不明",
                qr_code_url=body.url.strip(),
                card_image_url=card_image_url,
            )
            db.add(new_lh)
            db.commit()
            db.refresh(new_lh)
            return to_response(new_lh, user, db)
        raise HTTPException(status_code=404, detail="LIGHTHOUSE_CARD_NOT_REGISTERED")
    raise HTTPException(status_code=404, detail="QRコードに対応する灯台が見つかりません")


@router.post("/register-from-qr", response_model=LighthouseResponse, status_code=201)
def register_from_qr(
    body: RegisterFromQrRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    existing = db.query(Lighthouse).filter(Lighthouse.qr_code_url == body.qr_code_url.strip()).first()
    if existing:
        card = db.query(UserCard).filter(
            UserCard.user_id == user.id, UserCard.lighthouse_id == existing.id
        ).first()
        if not card:
            db.add(UserCard(user_id=user.id, lighthouse_id=existing.id))
            db.commit()
        return to_response(existing, user, db)

    lh = Lighthouse(
        name=body.name.strip(),
        region="不明",
        prefecture="不明",
        qr_code_url=body.qr_code_url.strip(),
    )
    db.add(lh)
    db.flush()
    db.add(UserCard(user_id=user.id, lighthouse_id=lh.id))
    db.commit()
    db.refresh(lh)
    return to_response(lh, user, db)
