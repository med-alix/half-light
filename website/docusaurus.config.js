// Docusaurus site for the HALF-LIGHT design book.
// Content lives in ../docs (plain Markdown); page order comes from ../docs/SUMMARY.md.

const {themes: prismThemes} = require('prism-react-renderer');

const repo = 'https://github.com/med-alix/half-light';

/** @type {import('@docusaurus/types').Config} */
module.exports = {
  title: 'HALF-LIGHT',
  tagline: "A tribe survival game on XEN's clock, and the NXN protocol that keeps DBXen burning.",
  favicon: 'img/favicon.svg',

  url: 'https://med-alix.github.io',
  baseUrl: '/half-light/',
  organizationName: 'med-alix',
  projectName: 'half-light',
  trailingSlash: true,

  onBrokenLinks: 'throw',

  markdown: {
    // .md files are read as plain CommonMark, not MDX, so GitBook-era Markdown works unchanged.
    format: 'detect',
    hooks: {onBrokenMarkdownLinks: 'throw'},
  },

  i18n: {defaultLocale: 'en', locales: ['en']},

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: '../docs',
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          exclude: ['SUMMARY.md', '.gitbook.yaml'],
          editUrl: `${repo}/edit/main/`,
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {customCss: require.resolve('./src/css/custom.css')},
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/social-card.jpg',
      colorMode: {defaultMode: 'dark', respectPrefersColorScheme: true},
      docs: {sidebar: {hideable: true}},
      navbar: {
        title: 'HALF-LIGHT',
        logo: {alt: 'HALF-LIGHT', src: 'img/favicon.svg'},
        items: [
          {type: 'doc', docId: 'protocols/README', label: 'Protocols', position: 'left'},
          {type: 'doc', docId: 'granary/README', label: 'NXN', position: 'left'},
          {type: 'doc', docId: 'game/README', label: 'Game', position: 'left'},
          {type: 'doc', docId: 'model/README', label: 'Model', position: 'left'},
          {href: repo, label: 'GitHub', position: 'right'},
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Read',
            items: [
              {label: 'Vision', to: '/vision/'},
              {label: 'The winter problem', to: '/the-winter-problem/'},
              {label: 'Glossary', to: '/glossary/'},
            ],
          },
          {
            title: 'Take part',
            items: [
              {label: 'Open questions', to: '/open-questions/'},
              {label: 'Contributing', to: '/contributing/'},
              {label: 'GitHub', href: repo},
            ],
          },
        ],
        copyright: `HALF-LIGHT design book · Built with Docusaurus`,
      },
      prism: {theme: prismThemes.github, darkTheme: prismThemes.dracula, additionalLanguages: ['solidity']},
    }),
};
