import React from 'react'
import PropTypes from 'prop-types'
import key from 'weak-key'
import axios from 'axios'
import GoalSummary from './GoalSummary'

const GoalsUrl = '/api/goal'

class GoalsList extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      goals: props.data
    }
    this.handleDelete = this.handleDelete.bind(this)
  }

  handleDelete (id) {
    if (!window.confirm('Delete learning goal?')) {
      return
    }

    axios.delete(`${GoalsUrl}/${id}/`).then(() => {
      this.setState({
        goals: this.state.goals.filter((goal) => goal.id !== id)
      })
    })
  }

  render () {
    return !this.state.goals.length ? (
      <div>
        <h2 className="subtitle">No learning goals yet!</h2>
        <p>
          <a href="" className="button is-primary">Create a new learning goal.</a>
        </p>
      </div>
    ) : (
      <div>
        <h1 className="title">Learning Goals</h1>
        <div className="learning-goals">
          {this.state.goals.map(
            goal => <GoalSummary goal={goal} deleteFn={this.handleDelete} key={key(goal)}/>
          )}
        </div>
      </div>
    )
  }
}

GoalsList.propTypes = {
  data: PropTypes.array.isRequired
}

export default GoalsList
