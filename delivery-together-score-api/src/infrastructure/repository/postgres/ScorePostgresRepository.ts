import Score from "@Domain/score/Score";
import DatabaseException from "@Api/utils/errorHandler/DatabaseException";
import PostgresDatabase from "@Infrastructure/database/postgresDatabase";
import ScoreRepository, {
  type Criterial,
} from "@Infrastructure/repository/ScoreRepository";
import ScoreEntity from "@Infrastructure/database/postgresDatabase/entities/Score";
import { scoreEntityMapper } from "@Infrastructure/repository/postgres/adapter/scorePostgresAdapter";

class ScorePostgresRepository implements ScoreRepository {
  private context: PostgresDatabase;

  constructor() {
    this.context = PostgresDatabase.getInstance();
  }
  
  async create(score: Score) {
    try {
      await this.context.dataSource.manager.save(scoreEntityMapper(score));
    } catch (ex) {
      if (ex instanceof Error) {
        throw new DatabaseException(ex.message, ex.stack);
      }
    }
  }
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  get(_id: string): Score {
    throw new Error("Method not implemented.");
  }

  async filter(criterial: Criterial): Promise<ScoreEntity> {
    try {
      const score = await this.context.dataSource.getRepository(ScoreEntity).findOne({
        where: {
          routeId: criterial.routeId,
          offerId: criterial.offerId,
        },
      });

      return score;
    } catch (ex) {
      if (ex instanceof Error) {
        throw new DatabaseException(ex.message, ex.stack);
      }
    }
  }
}

export default ScorePostgresRepository;
