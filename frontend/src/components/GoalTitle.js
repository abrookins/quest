import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const ESCAPE_KEY = 27
const ENTER_KEY = 13

class GoalTitle extends React.Component {
  constructor (props) {
    super(props)
    this.state = { editText: this.props.name }

    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleEdit = this.handleEdit.bind(this)
    this.handleKeyDown = this.handleKeyDown.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  handleSubmit (event) {
    const val = this.state.editText.trim()
    if (val) {
      this.props.onSave(val)
      this.setState({ editText: val })
    }
  }

  handleEdit () {
    this.props.onEdit()
    this.setState({ editText: this.props.name })
  }

  handleKeyDown (event) {
    if (event.which === ESCAPE_KEY) {
      this.setState({ editText: this.props.name })
      this.props.onCancel(event)
    } else if (event.which === ENTER_KEY) {
      this.handleSubmit(event)
    }
  }

  handleChange (event) {
    if (this.props.editing) {
      this.setState({ editText: event.target.value })
    }
  }

  render () {
    return (
      <h1 className="title">
        <div className={classNames({
          editing: this.props.editing,
          level: true,
          'goal-title': true
        })}>
          <div className="level-left view">
            {this.props.name}
          </div>
          <input
            ref='editGoalField'
            className='edit'
            value={this.state.editText}
            onBlur={this.handleSubmit}
            onChange={this.handleChange}
            onKeyDown={this.handleKeyDown}
          />
          <div className="level-right">
            <button className="edit button is-large" onClick={this.handleSubmit}>Save</button>
            <button className="view button" onClick={this.handleEdit}>Edit</button>
          </div>
        </div>
      </h1>
    )
  }
}

GoalTitle.propTypes = {
  name: PropTypes.string.isRequired,
  editing: PropTypes.bool.isRequired,
  onEdit: PropTypes.func.isRequired,
  onSave: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired
}

export default GoalTitle
