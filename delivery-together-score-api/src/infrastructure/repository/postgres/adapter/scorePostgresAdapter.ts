import Score from "@Domain/score/Score";
import ScoreEntity from "@Infrastructure/database/postgresDatabase/entities/Score";
import SIZE from "@Domain/size/Size";

const scoreEntityMapper = (score: Score): ScoreEntity => {
  const scoreEntity = new ScoreEntity();
  scoreEntity.id = score.id;
  scoreEntity.bagCost = score.bagCost;
  scoreEntity.offer = score.offer;
  scoreEntity.offerId = score.offerId;
  scoreEntity.routeId = score.routeId;
  scoreEntity.score = score.score;
  scoreEntity.size = sizeResolvedFromEntity(score.size);
  return scoreEntity;
};

const sizeResolvedFromEntity = (size: SIZE) => {
  switch(size) {
    case SIZE.LARGE:
      return 'LARGE';
    case SIZE.MEDIUM:
        return 'MEDIUM';
    case SIZE.SMALL:
      return 'SMALL';
  }
};

const sizeResolved = (size: string) => {
  switch(size) {
    case 'LARGE':
      return SIZE.LARGE;
    case 'MEDIUM':
        return SIZE.MEDIUM;
    case 'SMALL':
      return SIZE.SMALL;
  }
};

const scoreMapper = (scoreEntity: ScoreEntity): Score => {
  const score: Score = {
    id: scoreEntity.id,
    offerId: scoreEntity.offerId,
    offer: scoreEntity.offer,
    routeId: scoreEntity.routeId,
    bagCost: scoreEntity.bagCost,
    score: scoreEntity.score,
    size: sizeResolved(scoreEntity.size)
  };
       
  return score;
};

export { scoreEntityMapper, scoreMapper };
