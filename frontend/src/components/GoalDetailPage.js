import React from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
import DataProvider from './DataProvider'
import GoalDetail from './GoalDetail'
import TaskModel from './TaskModel'
import '../css/application.scss'
import '../css/tasks.scss'

const wrapper = document.getElementById('goal')
const goalId = document.getElementById('goal-id').dataset.id

let model = new TaskModel()

const GoalDetailPage = (props) => (
  <DataProvider endpoint={`/api/goal/${props.goalId}`} model={model}
    render={model => <GoalDetail model={model}/>}/>
)

GoalDetailPage.propTypes = {
  goalId: PropTypes.string.isRequired
}

function render () {
  wrapper ? ReactDOM.render(<GoalDetailPage goalId={goalId}/>, wrapper) : null
}

model.subscribe(render)
render()
