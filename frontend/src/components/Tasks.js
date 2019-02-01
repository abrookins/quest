import axios from 'axios'

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

const TaskUrl = '/api/task'

const update = (task) => axios.put(`${TaskUrl}/${task.id}/`, task)

const destroy = (task) => axios.delete(`${TaskUrl}/${task.id}/`)

const add = (goalId, task) => axios.post(`${TaskUrl}/`, { goal: goalId, name: task })

export default {
  update: update,
  destroy: destroy,
  add: add
}
