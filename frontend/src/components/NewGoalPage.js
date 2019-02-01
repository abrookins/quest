import React from 'react'
import ReactDOM from 'react-dom'
import Goals from './Goals'
import '../css/application.scss'

const wrapper = document.getElementById('goal')

class NewGoalPage extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      name: ''
    }
    this.handleChange = this.handleChange.bind(this)
    this.handleCancel = this.handleCancel.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleChange (event) {
    this.setState({ name: event.target.value })
  }

  handleCancel (event) {
    window.location.replace('/')
  }

  handleSubmit (event) {
    event.preventDefault()
    Goals.create(this.state.name).then((response) => {
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
              <input className="input" type="text" placeholder="Goal name" value={this.state.name}
                onChange={this.handleChange} />
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

wrapper ? ReactDOM.render(<NewGoalPage />, wrapper) : null
