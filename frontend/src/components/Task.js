import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

const ESCAPE_KEY = 27;
const ENTER_KEY = 13;


class Task extends React.Component {
  constructor(props) {
    super(props);
    this.state = {editText: this.props.task.title};

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleEdit = this.handleEdit.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleSubmit(event) {
    const val = this.state.editText.trim()
    if (val) {
      this.props.onSave(val);
      this.setState({editText: val});
    } else {
      this.props.onDestroy();

    }
  }

  handleEdit() {
    this.props.onEdit();
    this.setState({editText: this.props.task.title});
  }

  handleKeyDown(event) {
    if (event.which === ESCAPE_KEY) {
      this.setState({editText: this.props.task.title});
      this.props.onCancel(event);
    } else if (event.which === ENTER_KEY) {
      this.handleSubmit(event);
    }
  }

  handleChange(event) {
    if (this.props.editing) {
      this.setState({editText: event.target.value});
    }
  }

  render() {
    return (
      <li className={classNames({
        completed: this.props.task.completed,
        editing: this.props.editing
      })}>
        <div className="view">
          <input
            className="toggle"
            type="checkbox"
            checked={this.props.task.completed}
            onChange={this.props.onToggle}
          />
          <label onDoubleClick={this.handleEdit}>
            {this.props.task.title}
          </label>
          <button className="destroy" onClick={this.props.onDestroy}/>
        </div>
        <input
          ref="editField"
          className="edit"
          value={this.state.editText}
          onBlur={this.handleSubmit}
          onChange={this.handleChange}
          onKeyDown={this.handleKeyDown}
        />
      </li>
    );
  }
}

Task.propTypes = {
  task: PropTypes.object.isRequired,
  onSave: PropTypes.func.isRequired,
  onDestroy: PropTypes.func.isRequired,
  onEdit: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
  onToggle: PropTypes.func.isRequired,
  editing: PropTypes.bool.isRequired,
}

export default Task;
