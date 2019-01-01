import React from "react";
import PropTypes from "prop-types";
import GoalSummary from "./GoalSummary";


const GoalsList = ({data}) =>
  !data.length ? (
    <div>
      <h2 className="subtitle">No learning goals yet!</h2>
      <p>
        <a href="" className="button is-primary">Create a new learning goal.</a>
      </p>
    </div>
  ) : (
    <div className="learning-goals">
      {data.map(goal => GoalSummary(goal))}
    </div>
  );

GoalsList.propTypes = {
  data: PropTypes.array.isRequired
};

export default GoalsList;
