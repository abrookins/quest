import React from 'react'
import ReactDOM from 'react-dom'
import GoalsList from './GoalsList'
import Goals from './Goals'
import Utils from './Utils'
import '../css/application.scss'

class Homepage extends React.Component {
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
    const recommendedGoals = this.state.goals.filter((goal) => goal.is_public && !goal.user_has_started)
    let recommended = ''

    if (recommendedGoals.length) {
      recommended = <div className="learning-goals">
        <h2 className="subtitle">Recommended Goals</h2>
        <GoalsList goals={recommendedGoals} handleDelete={this.handleDelete}
          handleStart={this.handleStart}/>
      </div>
    }

    return <div className='your-goals'>
      <div className="learning-goals">
        <h2 className="subtitle">Your Learning Goals</h2>
        <GoalsList moreUrl="/goals" goals={yourGoals} handleDelete={this.handleDelete}
          handleStart={this.handleStart}/>
      </div>

      {recommended}
    </div>
  }
}

const wrapper = document.getElementById('homepage')

wrapper ? ReactDOM.render(<Homepage/>, wrapper) : null
