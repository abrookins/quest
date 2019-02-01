import axios from 'axios'

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

const GoalUrl = '/api/goal'

const getAll = () => axios.get(`${GoalUrl}/`).catch((error) => {
  console.log(error)
  window.alert('Could not retrieve goals due to an error.')
})

const get = (id) => axios.get(`${GoalUrl}/${id}/`).catch((error) => {
  console.log(error)
  window.alert('Could not retrieve goal due to an error.')
})

const create = (name) => {
  let data = { name: name, is_public: false }
  return axios.post(`${GoalUrl}/`, data).catch((error) => {
    console.log(error)
    window.alert('An error prevented creating the goal.')
  })
}

const update = (id, name) => axios.put(`${GoalUrl}/${id}/`, {
  name: name,
  id: id
}).catch((error) => {
  console.log(error)
  window.alert('An error prevented updating the goal.')
})

const start = (id) => axios.post(`${GoalUrl}/${id}/start/`).catch((error) => {
  console.log(error)
  window.alert('An error prevented starting the goal.')
})

const destroy = (id) => axios.delete(`${GoalUrl}/${id}/`).catch((error) => {
  console.log(error)
  window.alert('An error prevented deleting the goal.')
})

export default {
  getAll: getAll,
  get: get,
  create: create,
  update: update,
  start: start,
  delete: destroy
}
