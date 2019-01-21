import React from 'react'
import PropTypes from 'prop-types'
import key from 'weak-key'
import GoalSummary from './GoalSummary'
import GoalModel from './GoalModel'

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

    new GoalModel(id).delete().then(() => {
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
          <a href="/goal/new" className="button is-primary">Create a new learning goal.</a>
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
        <p>
          <a href="/goal/new" className="button is-primary">Add goal</a>
        </p>
      </div>
    )
  }
}

GoalsList.propTypes = {
  data: PropTypes.array.isRequired,
  model: PropTypes.object.isRequired
}

export default GoalsList
