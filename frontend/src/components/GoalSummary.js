import React from 'react'
import PropTypes from 'prop-types'

// TODO: Editable with GoalModel

const GoalSummary = (props) =>
  <div className="learning-goal row-card card">
    <div className="card-header">
      <p className="card-header-title">
        <a href={`/goal/${props.goal.id}`}>{props.goal.name}</a>
      </p>
      <p className="card-header-icon">
        <i className="fa fa-trash-o goal-button" onClick={() => props.deleteFn(props.goal.id)}/>
      </p>
    </div>
    <div className="card-content">
      <article className="content">
        <p>{props.goal.description ? props.goal.description : 'This is going to be awesome.'}</p>
      </article>
    </div>
    <div className=''>
      <progress className='progress is-primary' value={props.goal.percentage_complete}
        max='100'>
        {props.goal.percentage_complete === 100 ? (
          <span className='sr-only'>{props.goal.percentage_complete} Done!</span>
        ) : (
          <span
            className='sr-only'>{props.goal.percentage_complete} % Complete (success)</span>
        )}
      </progress>
    </div>
  </div>

GoalSummary.propTypes = {
  goal: PropTypes.object.isRequired,
  deleteFn: PropTypes.func.isRequired
}

export default GoalSummary
