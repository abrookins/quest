import React, { Component } from 'react'
import PropTypes from 'prop-types'
import axios from 'axios'

class DataProvider extends Component {
  constructor (props) {
    super(props)
    this.state = {
      model: props.model,
      loaded: false,
      placeholder: 'Loading...'
    }
  }

  componentDidMount () {
    let { model } = this.state
    axios.get(this.props.endpoint)
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: 'Something went wrong' })
        }
        return response.data
      })
      .then((data) => {
        if (this.state.model) {
          model.load(data)
          this.setState({ model: model, loaded: true })
        } else {
          this.setState({ model: data, loaded: true })
        }
      })
  }

  render () {
    const { model, loaded, placeholder } = this.state
    return loaded ? this.props.render(model) : <p>{placeholder}</p>
  }
}

DataProvider.propTypes = {
  endpoint: PropTypes.string.isRequired,
  render: PropTypes.func.isRequired,
  model: PropTypes.object.isRequired
}

export default DataProvider
