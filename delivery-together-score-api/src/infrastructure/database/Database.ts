interface Database {
    context();
    connection();
    close();
}

export default Database;