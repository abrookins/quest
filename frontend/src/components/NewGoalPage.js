import React from 'react'
import ReactDOM from 'react-dom'
import NewGoal from './NewGoal'
import GoalModel from './GoalModel'
import '../css/application.scss'

const wrapper = document.getElementById('goal')
let model = new GoalModel()

function render () {
  wrapper ? ReactDOM.render(<NewGoal model={model}/>, wrapper) : null
}

model.subscribe(render)
render()
