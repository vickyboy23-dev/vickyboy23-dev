const fs = require("fs");
const https = require("https");

const username = "Vicky_Boy_23";

https.get(`https://api.github.com/users/${username}`, {
  headers: { "User-Agent": "node" }
}, res => {

  let data = "";

  res.on("data", chunk => data += chunk);

  res.on("end", () => {

    const user = JSON.parse(data);

    const repos = user.public_repos;

    const template = fs.readFileSync("assets/jarvis-template.svg","utf8");

    const svg = template
      .replace("{{COMMITS}}","LIVE")
      .replace("{{REPOS}}", repos)
      .replace("{{LANGUAGES}}","Auto");

    fs.writeFileSync("assets/jarvis.svg", svg);

  });

});
