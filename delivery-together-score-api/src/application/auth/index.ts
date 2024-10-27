import { Logger } from "@Utils/logger";
import User from "@Domain/users/User";
import UserRepository from "@Infrastructure/repository/UserRepository";

const log = Logger(__filename);

class AuthApplication {
  constructor(private repository: UserRepository) {}

  async tokenValidator(token: string): Promise<User> {
    log.info("Execution token validator", {
      token,
    });

    try {
      const user = await this.repository.getByToken(token);

      if (!user) {
        log.error("Error in token validation");
        return null;
      }

      return user;
    } catch (ex) {
      if (ex instanceof Error) {
        throw ex;
      }
      throw ex;
    }
  }
}

export default AuthApplication;
