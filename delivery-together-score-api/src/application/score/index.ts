import { v4 as uuidv4 } from "uuid";
import SIZE from "@Domain/size/Size";
import Score from "@Domain/score/Score";
import ScoreRepository, {
  type Criterial,
} from "@Infrastructure/repository/ScoreRepository";
import { Logger } from "@Utils/logger";
import DatabaseException from "@Utils/errorHandler/DatabaseException";

const log = Logger(__filename);

const sizes = {
  LARGE: 1,
  MEDIUM: 0.5,
  SMALL: 0.25,
};

class ScoreApplication {
  constructor(private repository: ScoreRepository) {}

  private resolveSize(size: string) {
    let sizeValue = 0;
    switch (size) {
      case "SMALL":
        sizeValue = sizes[SIZE.SMALL];
        break;
      case "MEDIUM":
        sizeValue = sizes[SIZE.MEDIUM];
        break;
      case "LARGE":
        sizeValue = sizes[SIZE.LARGE];
        break;
    }

    return sizeValue;
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  async calculate(score: Score): Promise<Score> {
    try {
      log.info("Execution score calculation");
      const criterial: Criterial = {
        offerId: score.offerId,
        routeId: score.routeId,
      };
      const scoreFound = await this.repository.filter(criterial);

      if (scoreFound) {
        log.info("Score exist", {
          score: scoreFound,
        });
        score.id = scoreFound.id;
        score.score = scoreFound.score;
      } else {
        log.info("Score not exist");
        const uuid: string = uuidv4();
        score.id = uuid;
        const size: number = this.resolveSize(score.size.toString());
        score.score = score.offer - size * score.bagCost;
        await this.repository.create(score);
      }
      return score;
    } catch (ex) {
      if (ex instanceof DatabaseException) {
        log.error("Database error", {
          errorMessage: ex.message,
          stack: ex.stack,
        });
        throw new Error("Database error");
      }
      if (ex instanceof Error) {
        log.error("Some error ocurred in the calculation process", {
          errorMessage: ex.message,
          stack: ex.stack,
        });
        throw ex;
      }
      log.error("Something was wrong in calculation process");
      throw new Error("Something was wrong in calculation process");
    }
  }
}

export default ScoreApplication;
