// app.js
const dbConfig = require('./db');
const questionModel = require('./model');

// Lecture du fichier json 
// import * as data from './Clean_data.json';
const data = require('./Clean_data.json');


// Connexion à la base de données MongoDB
dbConfig.connect();
// dbConfig().catch(console.dir);


// Utilisation du modèle pour insérer une question dans la base de données
const newQuestion = {
  Question: 'What Is Autism Spectrum Disorder?',
  Answer: {
    definition: 'Autism spectrum disorder (ASD) is a neurodevelopmental disorder...',
    // ... (other parts of the answer)
  },
  Source: 'childmind',
};

// questionModel.insertQuestion(newQuestion);
questionModel.insertManyQuestions(data);
