import React from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
import { Router } from 'director/build/director'
import Goals from './Goals'
import GoalTitle from './GoalTitle'
import TasksFooter from './TasksFooter'
import Task from './Task'
import Tasks from './Tasks'
import Utils from './Utils'
import '../css/application.scss'
import '../css/tasks.scss'

const goalId = document.getElementById('goal-id').dataset.id

const ALL = 'all'
const ACTIVE = 'active'
const COMPLETED = 'completed'
const ENTER_KEY = 13

class GoalDetailPage extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      goal: null,
      loaded: false,
      placeholder: 'Loading...',
      mode: ALL,
      editingTask: null,
      editingGoal: false,
      newTask: '',
      descriptionText: ''
    }

    this.handleTaskChange = this.handleTaskChange.bind(this)
    this.handleNewTaskKeyDown = this.handleNewTaskKeyDown.bind(this)
    this.toggleAllTasks = this.toggleAllTasks.bind(this)
    this.toggleTask = this.toggleTask.bind(this)
    this.destroyTask = this.destroyTask.bind(this)
    this.editTask = this.editTask.bind(this)
    this.saveTask = this.saveTask.bind(this)
    this.cancelEditTask = this.cancelEditTask.bind(this)
    this.clearCompleted = this.clearCompleted.bind(this)

    this.editGoal = this.editGoal.bind(this)
    this.saveGoal = this.saveGoal.bind(this)
    this.cancelEditGoal = this.cancelEditGoal.bind(this)
    this.handleDescriptionSubmit = this.handleDescriptionSubmit.bind(this)
    this.handleDescriptionChange = this.handleDescriptionChange.bind(this)
  }

  componentDidMount () {
    const setState = this.setState
    let router = Router({
      '/': setState.bind(this, { mode: ALL }),
      '/active': setState.bind(this, { mode: ACTIVE }),
      '/completed': setState.bind(this, { mode: COMPLETED })
    })
    router.init('/')

    Goals.get(this.props.goalId)
      .catch(response => {
        console.log('Error retrieving goal.', response)
        this.setState({ placeholder: 'Something went wrong' })
      })
      .then((response) => {
        const tasks = response.data.tasks
        delete response.data.tasks
        let goal = response.data
        this.setState({ goal: goal, tasks: tasks, loaded: true, descriptionText: goal.description })
      })
  }

  handleTaskChange (event) {
    this.setState({ newTask: event.target.value })
  }

  handleNewTaskKeyDown (event) {
    if (event.keyCode !== ENTER_KEY) {
      return
    }

    event.preventDefault()

    const val = this.state.newTask.trim()

    if (val) {
      Tasks.add(this.state.goal.id, val).then((response) => {
        this.setState({ tasks: this.state.tasks.concat(response.data) })
      })
      this.setState({ newTask: '' })
    }
  }

  toggleAllTasks (event) {
    const checked = event.target.checked
    this.setState({
      tasks: this.state.tasks.map(function (task) {
        return Utils.extend({}, task, { completed: checked })
      })
    })
  }

  toggleTask (taskToToggle) {
    let newTasks = this.state.tasks.map((task) => {
      return task !== taskToToggle
        ? task
        : Utils.extend({}, task, { completed: !task.completed })
    })
    this.setState({
      tasks: newTasks
    }, () => {
      let task = this.state.tasks.find((task) => task.id === taskToToggle.id)
      Tasks.update(task)
    })
  }

  destroyTask (task) {
    Tasks.destroy(task).then(() => {
      this.setState({
        tasks: this.state.tasks.filter(function (candidate) {
          return candidate !== task
        })
      })
    })
  }

  editTask (task) {
    this.setState({ editingTask: task.id })
  }

  saveTask (taskToSave, text) {
    this.setState({
      tasks: this.state.tasks.map(function (task) {
        return task !== taskToSave
          ? task
          : Utils.extend({}, task, { name: text })
      })
    }, () => {
      let task = this.state.tasks.filter((task) => task.id === taskToSave.id)[0]
      Tasks.update(task).then((response) => {
        this.setState({ editingTask: false })
      })
    })
  }

  cancelEditTask () {
    this.setState({ editingTask: null })
  }

  clearCompleted () {
    let completedTasks = this.state.tasks.filter((task) => task.completed)
    completedTasks.map((task) => Tasks.destroy(task))
    this.setState({ tasks: this.state.tasks.filter((task) => !task.completed) })
  }

  editGoal () {
    this.setState({ editingGoal: true })
  }

  handleDescriptionSubmit (event) {
    this.goal.description = this.state.descriptionText
    this.saveGoal()
  }

  handleDescriptionChange (event) {
    if (this.state.editingGoal) {
      this.setState({ descriptionText: event.target.value })
    }
  }

  saveGoal (newName) {
    Goals.update(this.state.goal.id, newName).then((response) => {
      this.setState({ goal: response.data })
      this.setState({ editingGoal: false })
    })
  }

  cancelEditGoal () {
    this.setState({ editingGoal: false })
  }

  render () {
    let newTaskInput
    let main
    let footer

    if (!this.state.loaded) {
      return <div></div>
    }

    let tasks = this.state.tasks

    const shownTasks = tasks.filter(function (task) {
      switch (this.state.mode) {
        case ACTIVE:
          return !task.completed
        case COMPLETED:
          return task.completed
        default:
          return true
      }
    }, this)

    const taskItems = shownTasks.map((task) => {
      return (
        <Task
          key={task.id}
          task={task}
          goal={this.state.goal}
          onToggle={this.toggleTask.bind(this, task)}
          onDestroy={this.destroyTask.bind(this, task)}
          onEdit={this.editTask.bind(this, task)}
          editing={this.state.editingTask === task.id}
          onSave={this.saveTask.bind(this, task)}
          onCancel={this.cancelEditTask}
        />
      )
    }, this)

    const activeTaskCount = tasks.reduce(function (accum, task) {
      return task.completed ? accum : accum + 1
    }, 0)

    const completedCount = tasks.length - activeTaskCount

    if (!this.state.goal.is_public) {
      newTaskInput = <input
        className="new-task"
        placeholder="Add a new task for this learning goal"
        value={this.state.newTask}
        onKeyDown={this.handleNewTaskKeyDown}
        onChange={this.handleTaskChange}
        autoFocus={true}
      />
    }

    if (tasks.length) {
      main = (
        <section className="main">
          <input
            id="toggle-all"
            className="toggle-all"
            type="checkbox"
            onChange={this.toggleAllTasks}
            checked={activeTaskCount === 0}
          />
          <label
            htmlFor="toggle-all"
          />
          <ul className="task-list">
            {taskItems}
          </ul>
        </section>
      )
    }

    if (activeTaskCount || completedCount) {
      footer =
        <TasksFooter
          count={activeTaskCount}
          completedCount={completedCount}
          mode={this.state.mode}
          onClearCompleted={this.clearCompleted}
        />
    }

    return (
      <div>
        <header className="header">
          <GoalTitle name={this.state.goal.name} editing={this.state.editingGoal}
            onEdit={this.editGoal} onSave={this.saveGoal} onCancel={this.cancelEditGoal}/>
          {newTaskInput}
        </header>
        {main}
        {footer}
      </div>
    )
  }
}

GoalDetailPage.propTypes = {
  goalId: PropTypes.string.isRequired
}

const wrapper = document.getElementById('goal')
wrapper ? ReactDOM.render(<GoalDetailPage goalId={goalId}/>, wrapper) : null
