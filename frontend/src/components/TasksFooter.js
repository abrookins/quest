import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import Utils from "./Utils";

const ALL = 'all';
const ACTIVE = 'active';
const COMPLETED = 'completed';

class TasksFooter extends React.Component {
  render() {
    const activeTodoWord = Utils.pluralize(this.props.count, 'item')
    let clearButton = null

    if (this.props.completedCount > 0) {
      clearButton = (
        <button
          className="clear-completed button is-small"
          onClick={this.props.onClearCompleted}>
          Clear completed
        </button>
      );
    }

    const mode = this.props.mode
    return (
      <footer className="footer">
					<span className="task-count">
						<strong>{this.props.count}</strong> {activeTodoWord} left
					</span>
        <ul className="filters">
          <li>
            <a
              href="#/"
              className={classNames({selected: mode === ALL})}>
              All
            </a>
          </li>
          {' '}
          <li>
            <a
              href="#/active"
              className={classNames({selected: mode === ACTIVE})}>
              Active
            </a>
          </li>
          {' '}
          <li>
            <a
              href="#/completed"
              className={classNames({selected: mode === COMPLETED})}>
              Completed
            </a>
          </li>
        </ul>
        {clearButton}
      </footer>
    );
  }
}

TasksFooter.propTypes = {
  count: PropTypes.number.isRequired,
  completedCount: PropTypes.number.isRequired,
  onClearCompleted: PropTypes.func.isRequired,
  mode: PropTypes.string.isRequired,
};

export default TasksFooter;
