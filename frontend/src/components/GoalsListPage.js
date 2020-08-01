import React from 'react'
import ReactDOM from 'react-dom'
import Goals from './Goals'
import Utils from './Utils'
import GoalsList from './GoalsList'
import '../css/application.scss'

class GoalsListPage extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      goals: [],
      loaded: false,
      placeholder: 'Loading...'
    }
    this.handleDelete = this.handleDelete.bind(this)
    this.handleStart = this.handleStart.bind(this)
  }

  componentDidMount () {
    Goals.getAll()
      .catch(() => {
        this.setState({ placeholder: 'Something went wrong' })
      })
      .then(response => this.setState({ goals: response.data, loaded: true }))
  }

  handleDelete (id) {
    if (!window.confirm('Delete learning goal?')) {
      return
    }

    let goal = this.state.goals.filter(goal => goal.id === id)[0]

    Goals.delete(id).then(() => {
      if (goal.is_public) {
        this.setState({
          goals: this.state.goals.map((goal) => {
            return goal.id !== id
              ? goal
              : Utils.extend({}, goal, { user_has_started: false })
          })
        })
        return
      }
      this.setState({
        goals: this.state.goals.filter(goal => goal.id !== id)
      })
    })
  }

  handleStart (id) {
    Goals.start(id).then((request) => {
      let goals = this.state.goals.map((goal) => {
        return goal.id !== id ? goal : request.data
      })
      this.setState({
        goals: goals
      })
    })
  }

  render () {
    const yourGoals = this.state.goals.filter((goal) => goal.user_has_started || !goal.is_public)

    return <div className='your-goals'>
      <h1 className="title">Your Learning Goals</h1>
      <GoalsList goals={yourGoals} handleDelete={this.handleDelete}
        handleStart={this.handleStart} showAddButton/>
    </div>
  }
}

const wrapper = document.getElementById('goals_list')

wrapper ? ReactDOM.render(<GoalsListPage/>, wrapper) : null
