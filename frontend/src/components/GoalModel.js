import axios from 'axios'

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

const GoalUrl = '/api/goal'

const GoalModel = function (id = null, name = '') {
  this.id = id
  this.name = name
  this.onChanges = []
}

GoalModel.prototype.inform = function (onChange) {
  this.onChanges.forEach(function (cb) {
    cb()
  })
}

GoalModel.prototype.subscribe = function (onChange) {
  this.onChanges.push(onChange)
}

GoalModel.prototype.get = function (goalId, inform = true) {
  let promise = axios.get(`${GoalUrl}/${goalId}/`)
  promise.then((response) => {
    this.name = response.data.name
    this.id = response.data.id
  })
  if (inform) {
    promise.then((response) => {
      this.inform()
    })
  }
  return promise
}

GoalModel.prototype.create = function (data, inform = true) {
  let promise = axios.post(`${GoalUrl}/`, data)
  if (inform) {
    promise.then((response) => {
      this.inform()
    })
  }
  return promise
}

GoalModel.prototype.update = function (inform = true) {
  let promise = axios.put(`${GoalUrl}/${this.id}/`, {
    name: this.name,
    id: this.id
  })
  if (inform) {
    promise.then((response) => {
      this.inform()
    })
  }
  return promise
}

GoalModel.prototype.delete = function (inform = true) {
  let promise = axios.delete(`${GoalUrl}/${this.id}/`)
  if (inform) {
    promise.then((response) => {
      this.inform()
    })
  }
  return promise
}

export default GoalModel
