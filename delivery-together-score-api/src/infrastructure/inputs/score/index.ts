import { Request, Response } from "express";
import { StatusCodes } from "http-status-codes";
import ScoreApplication from "@Application/score";
import ScorePostgresRepository from "@Infrastructure/repository/postgres/ScorePostgresRepository";
import { Logger } from "@Utils/logger";
import { validation } from "@Infrastructure/inputs/score/scoreValidation";
import Score from "@Domain/score/Score";

const log = Logger(__filename);

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const Score = async (request: Request, response: Response) => {
  log.info("Receive request for calculate a score");

  const scoreRequest = request.body;

  const scoreValidation = validation(scoreRequest);

  if (scoreValidation.error) {
    log.error("The request is invalid", scoreValidation.error);
    response.status(StatusCodes.BAD_REQUEST).end();
    return;
  }

  log.info("Request received", scoreValidation);

  const application = new ScoreApplication(new ScorePostgresRepository());
  try {
    const score = await application.calculate(scoreRequest as Score);
    log.info("Score calculated", {
      score,
    });

    response.status(StatusCodes.OK);
    response.json({
      id: score.id,
      score: score.score,
    });
  } catch (ex) {
    if (ex instanceof Error) {
      log.error("Something was wrong in the score calculation", {
        errorMessage: ex.message,
        stack: ex.stack,
      });
      response.status(StatusCodes.INTERNAL_SERVER_ERROR).end();
    }
  }
};

export default Score;
