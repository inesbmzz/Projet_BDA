// questionModel.js
const { ObjectID } = require('mongodb');
const dbConfig = require('./db');

const collectionName = 'Q/A';

module.exports = {
  insertQuestion: async function (question) {
    const db = dbConfig.getDb();
    const result = await db.collection(collectionName).insertOne(question);
    console.log(`Question inserted with ID: ${result.insertedId}`);
  },
  insertManyQuestions: async function (questions) {
    const db = dbConfig.getDb();
    const result = await db.collection(collectionName).insertMany(questions);
    console.log(`Successfully done : ${result.insertedCount}`)
  },
  deleteAll: async function () {
    const db = dbConfig.getDb();
    await db.collection(collectionName).deleteMany({});
    console.log("Deleted all");
  },
};
