from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from ..models.user import User
from ..models.user_card import UserCard
from ..models.lighthouse import Lighthouse
from ..schemas.card import CardCreate, CardUpdate, CardResponse, StatsResponse, RegionStat
from ..schemas.lighthouse import LighthouseResponse
from ..core.security import decode_token

router = APIRouter(prefix="/cards", tags=["cards"])
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="無効なトークンです")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ユーザーが見つかりません")
    return user


def card_to_response(card: UserCard) -> CardResponse:
    lh_data = LighthouseResponse.model_validate(card.lighthouse)
    lh_data.is_collected = True
    return CardResponse(
        id=card.id,
        user_id=card.user_id,
        lighthouse_id=card.lighthouse_id,
        collected_at=card.collected_at,
        note=card.note,
        lighthouse=lh_data,
    )


@router.get("", response_model=list[CardResponse])
def list_cards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cards = (
        db.query(UserCard)
        .filter(UserCard.user_id == current_user.id)
        .order_by(UserCard.collected_at.desc())
        .all()
    )
    return [card_to_response(c) for c in cards]


@router.post("", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(
    body: CardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lh = db.query(Lighthouse).filter(Lighthouse.id == body.lighthouse_id).first()
    if not lh:
        raise HTTPException(status_code=404, detail="灯台が見つかりません")

    card = UserCard(user_id=current_user.id, lighthouse_id=body.lighthouse_id, note=body.note)
    db.add(card)
    try:
        db.commit()
        db.refresh(card)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="このカードは既に収集済みです")

    return card_to_response(card)


@router.get("/stats", response_model=StatsResponse)
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total = db.query(Lighthouse).count()
    collected_ids = {
        uc.lighthouse_id
        for uc in db.query(UserCard).filter(UserCard.user_id == current_user.id).all()
    }
    collected = len(collected_ids)

    regions = db.query(Lighthouse.region).distinct().all()
    region_stats = []
    for (region,) in regions:
        region_lhs = db.query(Lighthouse).filter(Lighthouse.region == region).all()
        region_total = len(region_lhs)
        region_collected = sum(1 for lh in region_lhs if lh.id in collected_ids)
        region_stats.append(
            RegionStat(
                region=region,
                total=region_total,
                collected=region_collected,
                rate=round(region_collected / region_total * 100, 1) if region_total else 0,
            )
        )

    return StatsResponse(
        total_lighthouses=total,
        collected_count=collected,
        achievement_rate=round(collected / total * 100, 1) if total else 0,
        region_stats=sorted(region_stats, key=lambda x: x.region),
    )


@router.get("/{lighthouse_id}", response_model=CardResponse)
def get_card(
    lighthouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = db.query(UserCard).filter(
        UserCard.user_id == current_user.id,
        UserCard.lighthouse_id == lighthouse_id,
    ).first()
    if not card:
        raise HTTPException(status_code=404, detail="収集記録が見つかりません")
    return card_to_response(card)


@router.patch("/{lighthouse_id}", response_model=CardResponse)
def update_card(
    lighthouse_id: int,
    body: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = db.query(UserCard).filter(
        UserCard.user_id == current_user.id,
        UserCard.lighthouse_id == lighthouse_id,
    ).first()
    if not card:
        raise HTTPException(status_code=404, detail="収集記録が見つかりません")

    if body.note is not None:
        card.note = body.note
    db.commit()
    db.refresh(card)
    return card_to_response(card)


@router.delete("/{lighthouse_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    lighthouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = db.query(UserCard).filter(
        UserCard.user_id == current_user.id,
        UserCard.lighthouse_id == lighthouse_id,
    ).first()
    if not card:
        raise HTTPException(status_code=404, detail="収集記録が見つかりません")
    db.delete(card)
    db.commit()
