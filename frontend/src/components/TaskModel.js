
import Utils from "./Utils";

const TaskUrl = "/api/task";

const TaskModel = function (goalId) {
  this.key = key;
  this.tasks = Utils.store(key);
  this.onChanges = [];
};

TaskModel.prototype.subscribe = function (onChange) {
  this.onChanges.push(onChange);
};

TaskModel.prototype.inform = function () {
  Utils.store(this.key, this.tasks);
  this.onChanges.forEach(function (cb) {
    cb();
  });
};

TaskModel.prototype.addTask = function (title) {
  this.tasks = this.tasks.concat({
    id: Utils.uuid(),
    title: title,
    completed: false
  });

  this.inform();
};

TaskModel.prototype.toggleAll = function (checked) {
  this.tasks = this.tasks.map(function (task) {
    return Utils.extend({}, task, {completed: checked});
  });

  this.inform();
};

TaskModel.prototype.toggle = function (taskToToggle) {
  this.tasks = this.tasks.map(function (task) {
    return task !== taskToToggle ?
      task :
      Utils.extend({}, task, {completed: !task.completed});
  });

  this.inform();
};

TaskModel.prototype.destroy = function (task) {
  this.tasks = this.tasks.filter(function (candidate) {
    return candidate !== task;
  });

  this.inform();
};

TaskModel.prototype.save = function (taskToSave, text) {
  this.tasks = this.tasks.map(function (task) {
    return task !== taskToSave ? task : Utils.extend({}, task, {title: text});
  });

  this.inform();
};

TaskModel.prototype.clearCompleted = function () {
  this.tasks = this.tasks.filter(function (task) {
    return !task.completed;
  });

  this.inform();
};

export default TaskModel;
