import React from 'react'
import PropTypes from 'prop-types'
import key from 'weak-key'
import GoalSummary from './GoalSummary'

class GoalsList extends React.Component {
  render () {
    const addButton = this.props.showAddButton ? <p>
      <a href="/goal/new" className="button is-primary">Add goal</a>
    </p> : ''
    const moreLink = this.props.moreUrl ? <p>
      <a href={this.props.moreUrl} className="is-size-6">See All</a>
    </p> : ''

    return !this.props.goals.length ? (
      <div>
        <p>
          <a href="/goal/new" className="button is-primary">Create a new learning goal.</a>
        </p>
      </div>
    ) : (
      <div>
        {moreLink}
        <div className="learning-goals">
          {this.props.goals.map(
            goal => <GoalSummary goal={goal} handleStart={this.props.handleStart.bind(this, goal.id)}
              handleDelete={this.props.handleDelete.bind(this, goal.id)} key={key(goal)} />
          )}
        </div>
        {addButton}
      </div>
    )
  }
}

GoalsList.propTypes = {
  goals: PropTypes.array.isRequired,
  showAddButton: PropTypes.bool,
  handleDelete: PropTypes.func.isRequired,
  handleStart: PropTypes.func.isRequired,
  moreUrl: PropTypes.string
}

export default GoalsList
