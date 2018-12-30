var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,

  entry: './static/js/index',

  output: {
    path: path.resolve('./static/bundles/'),
    filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  }

};
