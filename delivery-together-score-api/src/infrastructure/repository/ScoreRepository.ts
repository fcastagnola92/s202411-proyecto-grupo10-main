import Score from "@Domain/score/Score";
import ScoreEntity from "@Infrastructure/database/postgresDatabase/entities/Score";

export type Criterial = {
  routeId: string;
  offerId: string;
};

interface ScoreRepository {
  create(score: Score);
  get(id: string): Score;
  filter(criterial: Criterial):  Promise<ScoreEntity>;
}

export default ScoreRepository;
