import React from 'react'
import PropTypes from 'prop-types'
import key from 'weak-key'
import GoalSummary from './GoalSummary'
import GoalModel from './GoalModel'
import Utils from './Utils'

class GoalsList extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      goals: props.data
    }
    this.handleDelete = this.handleDelete.bind(this)
    this.handleStart = this.handleStart.bind(this)
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

  handleStart (id) {
    new GoalModel(id).start().then(() => {
      let goals = this.goals.map(function (goal) {
        return goal.id !== id
          ? goal
          : Utils.extend({}, goal, { has_started: true })
      })
      this.setState({
        goals: goals
      })
    })
  }

  render () {
    const addButton = this.props.showAddButton ? <p>
      <a href="/goal/new" className="button is-primary">Add goal</a>
    </p> : ''
    const moreLink = this.props.moreUrl ? <p>
      <a href={this.props.moreUrl} className="is-size-5">See All</a>
    </p> : ''

    return !this.state.goals.length ? (
      <div>
        <h2 className="subtitle">No learning goals yet!</h2>
        <p>
          <a href="/goal/new" className="button is-primary">Create a new learning goal.</a>
        </p>
      </div>
    ) : (
      <div>
        <h1 className="title">{this.props.header}</h1>
        {moreLink}
        <div className="learning-goals">
          {this.state.goals.map(
            goal => <GoalSummary goal={goal} startFn={this.handleStart}
              deleteFn={this.handleDelete} key={key(goal)} />
          )}
        </div>
        {addButton}
      </div>
    )
  }
}

GoalsList.propTypes = {
  data: PropTypes.array.isRequired,
  header: PropTypes.string.isRequired,
  showAddButton: PropTypes.bool,
  moreUrl: PropTypes.string
}

export default GoalsList
