import React from 'react'
import { Chart, PieSeries, Title, Tooltip, Legend } from '@devexpress/dx-react-chart-material-ui';
import { Animation, EventTracker, HoverState } from '@devexpress/dx-react-chart';

const Root = props => (
  <Legend.Root {...props} sx={{ display: 'flex', margin: 'auto', flexDirection: 'row' }} />
);

const Label = props => (
  <Legend.Label {...props} sx={{ whiteSpace: 'nowrap' }} />
);

function PieChart(props) {
  return (
    <Chart
      data={props.data}
    >
      <PieSeries
        valueField="value"
        argumentField="text"
      />
      {props.data.length !== 0 ?
        (<Title
          text={props.title}
        />) : ''}
      <Animation />
      <EventTracker />
      <HoverState />
      <Tooltip />
      <Legend position="bottom" rootComponent={Root} labelComponent={Label}/>
    </Chart>
  )
}

export default PieChart