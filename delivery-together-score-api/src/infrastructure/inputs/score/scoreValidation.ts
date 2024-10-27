import Joi from "joi";

const scoreSchema = Joi.object({
  offerId: Joi.string().required(),
  routeId: Joi.string().required(),
  offer: Joi.number().required(),
  bagCost: Joi.number().required(),
  size: Joi.string().valid('LARGE', 'MEDIUM', 'SMALL').required()
});

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const validation = (score: any) => {
  const result = scoreSchema.validate(score);

  return result;
};

export { validation };
