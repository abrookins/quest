const path = require('path')

module.exports = {
  entry: {
    goals_list: './frontend/src/goals_list.js',
    goal: './frontend/src/goal.js',
    new_goal: './frontend/src/new_goal.js'
  },
  output: {
    path: path.resolve('./frontend/static/frontend/'),
    filename: '[name].bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        }
      },
      {
        test: /\.scss$/,
        use: [
          'style-loader',
          'css-loader',
          'sass-loader'
        ]
      }
    ]
  }
}
