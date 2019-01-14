import Utils from './Utils'
import axios from 'axios'

const TaskUrl = '/api/task'

const TaskModel = function (goal) {
  this.goal = null
  this.tasks = []
  this.onChanges = []
}

TaskModel.prototype.load = function (data) {
  this.goal = data
  this.tasks = this.goal.tasks
  this.inform()
}

TaskModel.prototype.update = function (task, inform = true) {
  let promise = axios.put(`${TaskUrl}/${task.id}/`, task)
  if (inform) {
    promise.then((response) => {
      this.inform()
    })
  }
  return promise
}

TaskModel.prototype.updateAll = function () {
  let promises = this.tasks.map((task) => {
    return this.update(task)
  })
  Promise.all(promises).then(() => this.inform())
}

TaskModel.prototype.delete = function (task, inform = true) {
  let promise = axios.delete(`${TaskUrl}/${task.id}/`)
  if (inform) {
    promise.then((response) => {
      this.inform()
    })
  }
  return promise
}

TaskModel.prototype.add = function (task, inform = true) {
  let data = {
    goal: parseInt(this.goal.id),
    name: task,
    completed: false
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

TaskModel.prototype.inform = function (onChange) {
  this.onChanges.forEach(function (cb) {
    cb()
  })
}

TaskModel.prototype.subscribe = function (onChange) {
  this.onChanges.push(onChange)
}

TaskModel.prototype.toggleAll = function (checked) {
  this.tasks = this.tasks.map(function (task) {
    return Utils.extend({}, task, { completed: checked })
  })

  this.updateAll()
}

TaskModel.prototype.toggle = function (taskToToggle) {
  this.tasks = this.tasks.map(function (task) {
    return task !== taskToToggle
      ? task
      : Utils.extend({}, task, { completed: !task.completed })
  })
  let task = this.tasks.find((task) => task.id === taskToToggle.id)

  this.update(task)
}

TaskModel.prototype.destroy = function (task) {
  this.tasks = this.tasks.filter(function (candidate) {
    return candidate !== task
  })
  this.delete(task)
}

TaskModel.prototype.save = function (taskToSave, text) {
  this.tasks = this.tasks.map(function (task) {
    return task !== taskToSave ? task : Utils.extend({}, task, { name: text })
  })
  let task = this.tasks.map((task) => task.id === taskToSave.id)

  this.update(task)
}

// TODO: Should this delete?
TaskModel.prototype.clearCompleted = function () {
  this.tasks = this.tasks.filter(function (task) {
    return !task.completed
  })

  this.update()
}

export default TaskModel
