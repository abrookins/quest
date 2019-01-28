import axios from 'axios'
import TaskModel from './TaskModel'

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

const GoalUrl = '/api/goal'

class GoalModel {
  constructor (id = null, name = '') {
    this.id = id
    this.name = name
    this.tasks = new TaskModel()
    this.onChanges = []

    // Allow components to subscribe to GoalModel to receive
    // changes to both GoalModel and TaskModel state.
    this.tasks.subscribe(() => this.inform())
  }

  inform (onChange) {
    this.onChanges.forEach(function (cb) {
      cb()
    })
  }

  subscribe (onChange) {
    this.onChanges.push(onChange)
  }

  load (data, inform = true) {
    this.name = data.name
    this.id = data.id
    this.tasks.load(this.id, data.tasks)

    if (inform) {
      this.inform()
    }
  }

  save (newName = '') {
    this.name = newName
    this.update()
  }

  get (goalId, inform = true) {
    let promise = axios.get(`${GoalUrl}/${goalId}/`).catch((error) => {
      console.log(error)
      window.alert('Could not retrieve goal due to an error.')
    })
    promise.then((response) => {
      this.load(response.data, false)
    })
    if (inform) {
      promise.then((response) => {
        this.inform()
      })
    }
    return promise
  }

  create (data, inform = true) {
    let promise = axios.post(`${GoalUrl}/`, data).catch((error) => {
      console.log(error)
      window.alert('An error prevented creating the goal.')
    })
    if (inform) {
      promise.then((response) => {
        this.inform()
      })
    }
    return promise
  }

  update (inform = true) {
    let promise = axios.put(`${GoalUrl}/${this.id}/`, {
      name: this.name,
      id: this.id
    }).catch((error) => {
      console.log(error)
      window.alert('An error prevented updating the goal.')
    })
    if (inform) {
      promise.then((response) => {
        this.inform()
      })
    }
    return promise
  }

  start (inform = true) {
    let promise = axios.post(`${GoalUrl}/${this.id}/start/`).catch((error) => {
      console.log(error)
      window.alert('An error prevented starting the goal.')
    })
    if (inform) {
      promise.then((response) => {
        this.inform()
      })
    }
    return promise
  }

  delete (inform = true) {
    let promise = axios.delete(`${GoalUrl}/${this.id}/`).catch((error) => {
      console.log(error)
      window.alert('An error prevented deleting the goal.')
    })
    if (inform) {
      promise.then((response) => {
        this.inform()
      })
    }
    return promise
  }
}

export default GoalModel
