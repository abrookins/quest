import React from 'react'
import ReactDOM from 'react-dom'
import DataProvider from './DataProvider'
import GoalsList from './GoalsList'
import '../css/application.scss'

const Homepage = () => (
  <div>
    <div className='your-goals'>
      <DataProvider endpoint='/api/goal/?has_started=true'
        render={data => <GoalsList data={data} header="Your Learning Goals"
          moreUrl="/goals" />} />
    </div>

    <div className='public-goals'>
      <DataProvider endpoint='/api/goal/?is_public=true&has_started=false'
        render={data => <GoalsList data={data} header="Recommended Goals" />} />
    </div>
  </div>
)

const wrapper = document.getElementById('homepage')

wrapper ? ReactDOM.render(<Homepage />, wrapper) : null
