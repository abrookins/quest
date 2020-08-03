import React from 'react'
import PropTypes from 'prop-types'

const GoalSummary = (props) => {
  const showProgress = props.goal.user_has_started || !props.goal.is_public
  const progress = showProgress ? <div className='progress-container'>
    <progress className='progress is-primary' value={props.goal.percentage_complete}
      max='100'>
      {props.goal.percentage_complete === 100 ? (
        <span className='sr-only'>{props.goal.percentage_complete} Done!</span>
      ) : (
        <span
          className='sr-only'>{props.goal.percentage_complete} % Complete (success)</span>
      )}
    </progress>
  </div> : <button className="is-info is-small button is-fullwidth"
    onClick={props.handleStart}>Start</button>

	const tasks = props.goal.tasks.map((task) => {
				return (
					<li>{task.name}</li>
				)
			}, this)

  return <div className="learning-goal row-card card">
    <div className="card-header">
      <p className="card-header-title">
        <a href={`/goal/${props.goal.id}`}>{props.goal.name}</a>
      </p>
      <p className="card-header-icon">
        <i className="fa fa-trash-o goal-button" onClick={props.handleDelete} />
      </p>
    </div>
    <div className="card-content">
      <article className="content">
				<ul>
				{tasks}
				</ul>
      </article>
    </div>
    {progress}
  </div>
}

GoalSummary.propTypes = {
  goal: PropTypes.object.isRequired,
  handleDelete: PropTypes.func.isRequired,
  handleStart: PropTypes.func.isRequired
}

export default GoalSummary
