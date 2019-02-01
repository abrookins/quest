import React, { Component } from 'react'
import PropTypes from 'prop-types'
import axios from 'axios'

class DataProvider extends Component {
  constructor (props) {
    super(props)
    this.state = {
      placeholder: 'Loading...'
    }
  }

  componentDidMount () {
    axios.get(this.props.endpoint)
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: 'Something went wrong' })
        }
        return response.data
      })
      .then((data) => {
        this.props.onLoad(data)
      })
  }

  render () {
    const { model, loaded, placeholder } = this.state
    return loaded ? this.props.render(model) : <p>{placeholder}</p>
  }
}

DataProvider.propTypes = {
  onLoad: PropTypes.func.isRequired,
  endpoint: PropTypes.string.isRequired,
  render: PropTypes.func.isRequired,
  model: PropTypes.object
}

export default DataProvider
