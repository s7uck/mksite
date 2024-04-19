var express = require("express");
var cookieParser = require('cookie-parser');
var router = express.Router();

router.get('/', async (req, res, nex) => {
  let site = req.app.locals.site;

  res.render('index', site);
});

module.exports = router
