// server.js
const express = require('express');
const multer  = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// storage dir
const UPLOAD_DIR = path.join(__dirname, 'uploads');
if (!fs.existsSync(UPLOAD_DIR)) fs.mkdirSync(UPLOAD_DIR);

// multer setup
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, UPLOAD_DIR),
  filename: (req, file, cb) => {
    const ts = Date.now();
    const token = (req.body.token || 'notoken').replace(/[^a-zA-Z0-9-_]/g,'');
    cb(null, `${token}_${ts}.jpg`);
  }
});
const upload = multer({ storage });

app.use(express.static(path.join(__dirname, 'public')));

// endpoint for uploads
app.post('/upload', upload.single('photo'), (req, res) => {
  // req.body.token available
  if (!req.file) return res.status(400).send('Missing file');
  console.log('Received upload:', req.file.filename, 'token=', req.body.token);
  return res.send('OK');
});

// simple admin page to list images
app.get('/admin', (req, res) => {
  const files = fs.readdirSync(UPLOAD_DIR).filter(f=>f.endsWith('.jpg')).reverse();
  const html = `
    <html><head><meta name="viewport" content="width=device-width,initial-scale=1" /><title>Photos</title></head>
    <body style="font-family:Arial;padding:12px;">
      <h3>Uploaded photos (${files.length})</h3>
      ${files.map(f => `<div style="margin-bottom:12px;"><img src="/uploads/${f}" style="max-width:220px;border-radius:8px;display:block"/><div style="font-size:12px;color:#444">${f}</div></div>`).join('')}
    </body></html>`;
  res.send(html);
});

// serve uploads
app.use('/uploads', express.static(UPLOAD_DIR));

app.listen(PORT, () => console.log('Server listening on', PORT));
