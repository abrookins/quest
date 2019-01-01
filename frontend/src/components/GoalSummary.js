import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";

const GoalSummary = (learning_goal) =>
  <div className="learning-goal row-card card" key={key(learning_goal)}>
    <div className="card-header">
      <p className="card-header-title">
        <a href="">{learning_goal.name}</a>
      </p>
      <p className="card-header-icon">
        <a href="" data-method="delete" data-confirm='Delete this goal?'>
          <i className="fa fa-trash-o goal-button"/>
        </a>
        <a href="">
          <i className="fa fa-pencil goal-button"/>
        </a>
      </p>
    </div>
    <div className="card-content">
      <article className="content">
        {learning_goal.description &&
        <p>{learning_goal.description}</p>}
      </article>
    </div>
    <div className="">
      <progress className="progress is-primary" value={learning_goal.percentage_complete}
                max="100">
        {learning_goal.percentage_complete === 100 ? (
          <span className="sr-only">{learning_goal.percentage_complete} Done!</span>
        ) : (
          <span className="sr-only">{learning_goal.percentage_complete} % Complete (success)</span>
        )}
      </progress>
    </div>
  </div>

GoalSummary.propTypes = {
  learning_goal: PropTypes.object.isRequired
};

export default GoalSummary;
