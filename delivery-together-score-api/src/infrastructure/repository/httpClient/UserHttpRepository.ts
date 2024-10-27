import User from "@Domain/users/User";
import { StatusCodes } from "http-status-codes";
import { UserMapper } from "./adapter/userHttpAdapter";
import UserRepository from "@Infrastructure/repository/UserRepository";
import config from "@Config/index";

class UserHttpRepository implements UserRepository {
  async getByToken(token: string): Promise<User | null> {
    const requestHeaders = new Headers();
    requestHeaders.set("Content-Type", "application/json");
    requestHeaders.set("Authorization", `Bearer ${token}`);
    try {
      const response = await fetch(`${config.USERS_PATH}/users/me`, {
        method: "GET",
        headers: requestHeaders,
      });

      if (response.status === StatusCodes.OK) {
        const data = await response.json();
        return UserMapper(data);
      }

      return null;
    } catch (ex) {
      if (ex instanceof Error) {
        throw ex;
      }
      throw ex;
    }
  }
}

export default UserHttpRepository;
