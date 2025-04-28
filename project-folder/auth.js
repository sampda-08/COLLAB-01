// auth.js
const connectDB = require('./db');

async function createUser(username, password, name, email, phone, address) {
  const db = await connectDB();
  const usersCollection = db.collection('users');
  try {
    await usersCollection.insertOne({ username, password, name, email, phone, address });
    console.log('User created successfully');
  } catch (error) {
    console.error('Failed to create user', error);
  }
}

async function loginUser(username, password) {
  const db = await connectDB();
  const usersCollection = db.collection('users');
  try {
    const user = await usersCollection.findOne({ username, password });
    if (user) {
      console.log('Login successful');
      return true;
    } else {
      console.log('Invalid credentials');
      return false;
    }
  } catch (error) {
    console.error('Login failed', error);
    return false;
  }
}

module.exports = { createUser, loginUser };
