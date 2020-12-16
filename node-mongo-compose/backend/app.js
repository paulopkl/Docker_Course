const express = require('express');
const restful = require('node-restful');
const server = express();
const bodyparser = require('body-parser');
const cors = require('cors');

const mongoose = require('mongoose');

// Database
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://db/mydb', { useMongoClient: true });

// Middlewares
server.use(bodyparser.urlencoded({ extended: true }));
server.use(bodyparser.json());
server.use(cors());

// ODM
const Client = restful.model('Client', {
    name: { 
        type: String, 
        required: true 
    },
});

// Rest API
Client.methods(['get', 'post', 'put', 'delete']);
Client.updateOptions({ new: true, runValidators: true });
Client.register(server, '/clients');

// Start Server
const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Server is Running on port: ${PORT}!!`);
});