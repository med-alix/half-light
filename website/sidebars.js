// Builds the sidebar from ../docs/SUMMARY.md so page order is edited in one place.
//   * [Title](path.md)  -> a page
//   ## Heading          -> a collapsible category holding the pages below it

const fs = require('fs');
const path = require('path');

const summary = fs.readFileSync(path.join(__dirname, '../docs/SUMMARY.md'), 'utf8');

const toDocId = (file) => file.replace(/\.md$/, '');

const sidebar = [];
let category = null;

for (const line of summary.split(/\r?\n/)) {
  const heading = line.match(/^##\s+(.+)/);
  if (heading) {
    category = {type: 'category', label: heading[1].trim(), collapsed: false, items: []};
    sidebar.push(category);
    continue;
  }
  const link = line.match(/^\s*[*-]\s+\[(.+?)\]\((.+?\.md)\)/);
  if (link) {
    const item = {type: 'doc', id: toDocId(link[2]), label: link[1]};
    (category ? category.items : sidebar).push(item);
  }
}

module.exports = {book: sidebar};
