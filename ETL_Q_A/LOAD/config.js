const dotenv = require('dotenv');
dotenv.config();

const db_uri = process.env.DBURI;
const db_username = process.env.USERNAME;
const db_password = process.env.PASSWORD;

module.exports = {
    db_uri,
    db_username,
    db_password
}