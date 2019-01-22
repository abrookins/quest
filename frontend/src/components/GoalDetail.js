import React from 'react'
import PropTypes from 'prop-types'
import { Router } from 'director/build/director'
import GoalTitle from './GoalTitle'
import TasksFooter from './TasksFooter'
import Task from './Task'

const ALL = 'all'
const ACTIVE = 'active'
const COMPLETED = 'completed'
const ENTER_KEY = 13

class GoalDetail extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      mode: ALL,
      editingTask: null,
      editingGoal: false,
      newTask: ''
    }

    this.handleChange = this.handleChange.bind(this)
    this.handleNewTaskKeyDown = this.handleNewTaskKeyDown.bind(this)
    this.toggleAll = this.toggleAll.bind(this)
    this.toggle = this.toggle.bind(this)
    this.destroy = this.destroy.bind(this)
    this.destroy = this.destroy.bind(this)
    this.edit = this.edit.bind(this)
    this.save = this.save.bind(this)
    this.cancel = this.cancel.bind(this)
    this.clearCompleted = this.clearCompleted.bind(this)

    this.editGoal = this.editGoal.bind(this)
    this.saveGoal = this.saveGoal.bind(this)
    this.cancelGoal = this.cancelGoal.bind(this)
  }

  componentDidMount () {
    const setState = this.setState
    let router = Router({
      '/': setState.bind(this, { mode: ALL }),
      '/active': setState.bind(this, { mode: ACTIVE }),
      '/completed': setState.bind(this, { mode: COMPLETED })
    })
    router.init('/')
  }

  handleChange (event) {
    this.setState({ newTask: event.target.value })
  }

  handleNewTaskKeyDown (event) {
    if (event.keyCode !== ENTER_KEY) {
      return
    }

    event.preventDefault()

    const val = this.state.newTask.trim()

    if (val) {
      this.props.model.tasks.add(val)
      this.setState({ newTask: '' })
    }
  }

  toggleAll (event) {
    const checked = event.target.checked
    this.props.model.tasks.toggleAll(checked)
  }

  toggle (taskToToggle) {
    this.props.model.tasks.toggle(taskToToggle)
  }

  destroy (task) {
    this.props.model.tasks.destroy(task)
  }

  edit (task) {
    this.setState({ editingTask: task.id })
  }

  save (taskToSave, text) {
    this.props.model.tasks.save(taskToSave, text)
    this.setState({ editingTask: null })
  }

  cancel () {
    this.setState({ editingTask: null })
  }

  clearCompleted () {
    this.props.model.tasks.clearCompleted()
  }

  editGoal () {
    this.setState({ editingGoal: true })
  }

  saveGoal (newName) {
    this.props.model.save(newName)
    this.setState({ editingGoal: false })
  }

  cancelGoal () {
    this.setState({ editingGoal: false })
  }

  render () {
    let footer
    let main
    const tasks = this.props.model.tasks.all()

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
          onToggle={this.toggle.bind(this, task)}
          onDestroy={this.destroy.bind(this, task)}
          onEdit={this.edit.bind(this, task)}
          editing={this.state.editingTask === task.id}
          onSave={this.save.bind(this, task)}
          onCancel={this.cancel}
        />
      )
    }, this)

    const activeTaskCount = tasks.reduce(function (accum, task) {
      return task.completed ? accum : accum + 1
    }, 0)

    const completedCount = tasks.length - activeTaskCount

    if (activeTaskCount || completedCount) {
      footer =
        <TasksFooter
          count={activeTaskCount}
          completedCount={completedCount}
          mode={this.state.mode}
          onClearCompleted={this.clearCompleted}
        />
    }

    if (tasks.length) {
      main = (
        <section className="main">
          <input
            id="toggle-all"
            className="toggle-all"
            type="checkbox"
            onChange={this.toggleAll}
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

    return (
      <div>
        <header className="header">
          <GoalTitle name={this.props.model.name} editing={this.state.editingGoal}
            onEdit={this.editGoal} onSave={this.saveGoal} onCancel={this.cancelGoal} />
          <input
            className="new-task"
            placeholder="Add a new task for this goal"
            value={this.state.newTask}
            onKeyDown={this.handleNewTaskKeyDown}
            onChange={this.handleChange}
            autoFocus={true}
          />
        </header>
        {main}
        {footer}
      </div>
    )
  }
}

GoalDetail.propTypes = {
  model: PropTypes.object.isRequired
}

export default GoalDetail
