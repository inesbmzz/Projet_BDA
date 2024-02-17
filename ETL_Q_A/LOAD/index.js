// index.js
const dbConfig = require('./db');
const questionModel = require('./model');

// Lecture du fichier json 
// import * as data from './Clean_data.json';
const data = require('./Clean_data.json');


// Connexion à la base de données MongoDB
dbConfig.connect();
// dbConfig().catch(console.dir);

// questionModel.insertQuestion(newQuestion);
questionModel.deleteAll();
questionModel.insertManyQuestions(data);
questionModel.disconnect()
            .then(() => {
              console.log('Connection to MongoDB closed');
              // Exit the Node.js process
              process.exit(0);
            })
            .catch(err => {
              console.error('Error:', err);
              // Exit the Node.js process with an error code
              process.exit(1);
            })
            ;
// dbConfig.close();
