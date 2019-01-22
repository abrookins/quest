import Utils from './Utils'
import axios from 'axios'

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

const TaskUrl = '/api/task'

class TaskModel {
  constructor () {
    this.goalId = null
    this.tasks = []
    this.onChanges = []
  }

  all () {
    return this.tasks
  }

  load (goalId, tasks) {
    this.goalId = goalId
    this.tasks = tasks
  }

  update (task, inform = true) {
    let promise = axios.put(`${TaskUrl}/${task.id}/`, task)
    if (inform) {
      promise.then((response) => {
        this.inform()
      })
    }
    return promise
  }

  updateAll () {
    let promises = this.tasks.map((task) => {
      return this.update(task)
    })
    Promise.all(promises).then(() => this.inform())
  }

  delete (task, inform = true) {
    let promise = axios.delete(`${TaskUrl}/${task.id}/`)
    if (inform) {
      promise.then((response) => {
        this.inform()
      })
    }
    return promise
  }

  add (task, inform = true) {
    let data = {
      goal: parseInt(this.goalId),
      name: task
    }
    let promise = axios.post(`${TaskUrl}/`, data).then((response) => {
      this.tasks = this.tasks.concat(response.data)
    })
    if (inform) {
      promise.then((response) => {
        this.inform()
      })
    }
    return promise
  }

  inform (onChange) {
    this.onChanges.forEach(function (cb) {
      cb()
    })
  }

  subscribe (onChange) {
    this.onChanges.push(onChange)
  }

  toggleAll (checked) {
    this.tasks = this.tasks.map(function (task) {
      return Utils.extend({}, task, { completed: checked })
    })

    this.updateAll()
  }

  toggle (taskToToggle) {
    this.tasks = this.tasks.map(function (task) {
      return task !== taskToToggle
        ? task
        : Utils.extend({}, task, { completed: !task.completed })
    })
    let task = this.tasks.find((task) => task.id === taskToToggle.id)

    this.update(task)
  }

  destroy (task) {
    this.tasks = this.tasks.filter(function (candidate) {
      return candidate !== task
    })
    this.delete(task)
  }

  save (taskToSave, text) {
    this.tasks = this.tasks.map(function (task) {
      return task !== taskToSave ? task : Utils.extend({}, task, { name: text })
    })
    let task = this.tasks.filter((task) => task.id === taskToSave.id)[0]

    this.update(task)
  }

  clearCompleted () {
    let completedTasks = this.tasks.filter((task) => task.completed)
    completedTasks.map((task) => this.delete(task))
    this.tasks = this.tasks.filter((task) => !task.completed)
  }
}

export default TaskModel
