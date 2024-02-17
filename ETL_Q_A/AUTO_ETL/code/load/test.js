const { MongoClient } = require('mongodb');
// const { MongoMemoryServer } = require('mongodb-memory-server');
const {db_uri, db_name} = require('./config');

// Connect to the database
let db;
let client;

beforeAll(async () => {
    // Connect to the database
    client = await MongoClient.connect(db_uri);
    db = client.db();
    // const mongod = await MongoMemoryServer.create();
    // const uri = await mongod.getUri();

    // client = await MongoClient.connect(uri);
    // db = client.db();
});

describe('Database Tests', () => {
  it('should insert a document into the database', async () => {
    // Insert a document into the Q/A collection
    const question = { Question: "What's Moh's nickname ?", Answer: 'Legend', Source: 'Chakib :)' };
    await db.collection(db_name).insertOne(question);

    // Retrieve the inserted document
    const result = await db.collection(db_name).findOne({ Question: "What's Moh's nickname ?" });

    // Assert that the document was inserted successfully
    expect(result).toBeTruthy();
    expect(result.Question).toEqual("What's Moh's nickname ?");
    expect(result.Answer).toEqual('Legend');

    await db.collection(db_name).drop(question);
  });

  
});

describe('Metadata Tests', () => {
    it('document format', async () => {
        // Query the collection to retrieve documents
        const documents = await db.collection(db_name).find({}).toArray();
        // Verify that each document has attributes: Question, Answer and Source
        documents.forEach(document => {
            expect(document).toHaveProperty('Question');
            expect(document).toHaveProperty('Answer');
            expect(document).toHaveProperty('Source');
        })
    });

    it('should have a non-empty question', async () => {
        const documents = await db.collection('your_collection_name').find({}).toArray();
        // Verify that each document contains non-empty Question
        documents.forEach((document) => {
            expect(document.Question).toBeTruthy();
        });
    });

    it('should have a non-empty answer', async () => {
        const documents = await db.collection('your_collection_name').find({}).toArray();
        // Verify that each document contains non-empty Answer
        documents.forEach((document) => {
            expect(document.Answer).toBeTruthy();
        });
    });
})

// Clean up after tests
afterAll(async () => {
  //await db.dropDatabase();    // Drop if a virtual dataset
  await client.close();
});
