import User from '@Domain/users/User';

interface UserRepository {
  getByToken(token: string): Promise<User | null>;
}

export default UserRepository;