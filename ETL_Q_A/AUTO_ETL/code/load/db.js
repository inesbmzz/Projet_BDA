// DB configuration and connection
const {db_uri, db_name} = require('./config');
const { MongoClient } = require('mongodb');

async function performDatabaseOperations() {
  await new Promise(resolve => setTimeout(resolve, 5000));
  console.log('Database operations completed');
}

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
    } catch (err) {
      console.error('Error closing MongoDB', err);
    } finally {
      await performDatabaseOperations();
      // process.exit(0);
    }
  }
};

