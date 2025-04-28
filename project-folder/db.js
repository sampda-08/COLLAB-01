// db.js
const { MongoClient } = require('mongodb');

const url = 'mongodb://localhost:27017'; // Default MongoDB URL
const dbName = 'userDatabase';

const client = new MongoClient(url);

async function connectDB() {
  try {
    await client.connect();
    console.log('Connected successfully to MongoDB');
    const db = client.db(dbName);
    return db;
  } catch (error) {
    console.error('Connection failed', error);
  }
}

module.exports = connectDB;
