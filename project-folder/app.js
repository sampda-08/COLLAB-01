// app.js
const express = require('express');
const { createUser, loginUser } = require('./auth');
const path = require('path');

const app = express();

// Serve static files from the "public" folder
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: true }));

// Route for handling form submission
app.post('/login', async (req, res) => {
  const { option, username, password, name, email, phone, address } = req.body;

  if (option === 'login') {
    const loginResult = await loginUser(username, password);
    if (loginResult) {
      res.redirect('/dashboard.html'); // Redirect to dashboard after successful login
    } else {
      res.redirect('/index.html'); // Send error response
    }
  } else if (option === 'signup') {
    await createUser(username, password, name, email, phone, address);
    res.redirect('/dashboard.html'); // Redirect to dashboard after successful sign-up
  }
});

// Start the server
app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
