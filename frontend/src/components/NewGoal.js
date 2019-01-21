import React from 'react'
import PropTypes from 'prop-types'

class NewGoal extends React.Component {
  constructor (props) {
    super(props)
    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleCancel = this.handleCancel.bind(this)
    this.state = {
      name: ''
    }
  }

  handleChange (event) {
    this.setState({ name: event.target.value })
  }

  handleCancel (event) {
    window.location.replace('/')
  }

  handleSubmit (event) {
    event.preventDefault()
    this.props.model.create(this.state).then((response) => {
      window.location.replace(`/goal/${response.data.id}`)
    })
  }

  render () {
    return (
      <div>
        <h2 className='title'>New Goal</h2>
        <form onSubmit={this.handleSubmit}>
          <div className="field">
            <label className="label">Name</label>
            <div className="control">
              <input className="input" type="text" placeholder="Goal name" value={this.state.name} onChange={this.handleChange} />
            </div>
          </div>

          <div className="field is-grouped">
            <div className="control">
              <button className="button is-primary" onSubmit={this.handleSubmit}>Create</button>
            </div>
            <div className="control">
              <a className="button is-text" onClick={this.handleCancel}>Cancel</a>
            </div>
          </div>
        </form>
      </div>
    )
  }
}

NewGoal.propTypes = {
  model: PropTypes.object.isRequired
}

export default NewGoal
