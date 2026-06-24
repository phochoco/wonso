const { JSDOM } = require('jsdom');
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf-8');
const js = fs.readFileSync('script.js', 'utf-8');
const dataJs = fs.readFileSync('elements_data.js', 'utf-8');

const dom = new JSDOM(html, { runScripts: "dangerously", resources: "usable" });
const window = dom.window;

window.eval(dataJs);
try {
  window.eval(js);
  console.log("Script loaded successfully");
  window.openModal(window.elementsData[0]);
  console.log("openModal ran successfully");
} catch(e) {
  console.error("Error:", e);
}
