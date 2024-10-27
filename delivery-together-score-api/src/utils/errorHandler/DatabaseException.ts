class DatabaseException extends Error {
  constructor(message: string, stack: string) {
    super();
    this.message = message;
    this.stack = stack;
  }
}

export default DatabaseException;
