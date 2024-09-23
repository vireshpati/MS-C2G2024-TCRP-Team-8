self.__BUILD_MANIFEST = {
  "polyfillFiles": [
    "static/chunks/polyfills.js"
  ],
  "devFiles": [
    "static/chunks/react-refresh.js"
  ],
  "ampDevFiles": [],
  "lowPriorityFiles": [],
  "rootMainFiles": [],
  "pages": {
    "/_app": [
      "static/chunks/webpack.js",
      "static/chunks/main.js",
      "static/chunks/pages/_app.js"
    ],
    "/_error": [
      "static/chunks/webpack.js",
      "static/chunks/main.js",
      "static/chunks/pages/_error.js"
    ],
    "/chatbot": [
      "static/chunks/webpack.js",
      "static/chunks/main.js",
      "static/chunks/pages/chatbot.js"
    ],
    "/matches": [
      "static/chunks/webpack.js",
      "static/chunks/main.js",
      "static/chunks/pages/matches.js"
    ],
    "/meet": [
      "static/chunks/webpack.js",
      "static/chunks/main.js",
      "static/chunks/pages/meet.js"
    ],
    "/message": [
      "static/chunks/webpack.js",
      "static/chunks/main.js",
      "static/chunks/pages/message.js"
    ],
    "/portal": [
      "static/chunks/webpack.js",
      "static/chunks/main.js",
      "static/chunks/pages/portal.js"
    ]
  },
  "ampFirstPages": []
};
self.__BUILD_MANIFEST.lowPriorityFiles = [
"/static/" + process.env.__NEXT_BUILD_ID + "/_buildManifest.js",
,"/static/" + process.env.__NEXT_BUILD_ID + "/_ssgManifest.js",

];