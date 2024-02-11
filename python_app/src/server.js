const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/set_joints', (req, res) => {
  console.log('Incoming robot joint data:', req.body);
  res.status(200).send('Data received');
});

app.listen(port, () => {
  console.log(`Server listening at http://10.0.0.12:${port}`);
});

app.use(express.static('public'));


// const express = require('express');
// const bodyParser = require('body-parser');
// const https = require('https');
// const fs = require('fs');

// const app = express();
// const port = 443;

// app.use(bodyParser.json());

// app.post('/set_joints', (req, res) => {
//   console.log('Incoming robot joint data:', req.body);
//   res.status(200).send('Data received');
// });

// const privateKey = fs.readFileSync('localhost.key', 'utf8');
// const certificate = fs.readFileSync('localhost.cert', 'utf8');

// const credentials = { key: privateKey, cert: certificate };
// const httpsServer = https.createServer(credentials, app);

// httpsServer.listen(port, () => {
//   console.log(`Server listening at https://10.0.0.12:${port}`);
// });

// app.use(express.static('public'));
