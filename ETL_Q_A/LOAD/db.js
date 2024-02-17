// DB configuration and connection
const {db_uri, db_name} = require('./config');
const { MongoClient } = require('mongodb');

const client = new MongoClient(db_uri);

module.exports = {
  connect: async function () {
    try {
      await client.connect();
      console.log('Connected to MongoDB');
    } catch (err) {
      console.error('Error connecting to MongoDB', err);
    }
  },
  getDb: function () {
    return client.db(db_name);
  },
  getClient: function () {
    return client;
  },
  close: async function () {
    try {
      await client.close();
      console.log('Disconnected from MongoDB');
    } catch (err) {
      console.error('Error closing MongoDB', err);
    } finally {
      process.exit(0);
    }
  }
};

