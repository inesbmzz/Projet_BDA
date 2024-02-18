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


dbConfig.close();

const { exec } = require('child_process');

// Run a command
exec('npm test', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`stderr: ${stderr}`);
    return;
  }
  console.log(`stdout: ${stdout}`);
});
