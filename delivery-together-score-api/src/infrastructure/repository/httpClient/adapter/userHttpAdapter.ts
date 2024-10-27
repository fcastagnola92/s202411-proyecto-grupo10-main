import User from "@Domain/users/User";

const UserMapper = (data: unknown): User => {
  const { id, username, email, fullName, dni, phoneNumber, status } =
    data as User;
  return {
    id,
    username,
    email,
    fullName,
    dni,
    phoneNumber,
    status,
  };
};

export { UserMapper };
