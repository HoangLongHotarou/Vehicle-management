import { React, Fragment } from 'react'
import {
    Chart, ArgumentAxis, ValueAxis, Title, Legend, Tooltip,
} from '@devexpress/dx-react-chart-material-ui';
import { Animation, EventTracker, HoverState } from '@devexpress/dx-react-chart';
import { useState } from 'react';

const Root = props => (
    <Legend.Root {...props} sx={{ display: 'flex', margin: 'auto', flexDirection: 'row' }} />
);

const Label = props => (
    <Legend.Label {...props} sx={{ whiteSpace: 'nowrap' }} />
);

const TooltipContent = (props) => {
    const { targetItem, text, ...restProps } = props;
    return (
        <div>
            <div>
                <Tooltip.Content
                    {...restProps}
                    text={targetItem.value}
                />
            </div>
        </div>
    );
};

function StackedBarChart(props) {

    const [targetToolTip, setTargetToolTip] = useState(null);

    const handleChangeToolTip = target => {
        target ? setTargetToolTip({...target, value: getValue(target)}) : setTargetToolTip(null);
    }

    const getValue = target => {
        if (target) {
            const { order, point } = target;
            let key = order === 0 ? 'total_in' : 'total_out';
            return props.data[point][key];
        }       
    }

    return (
        <>
            {props.data.length !== 0 ? (
                <Chart
                    data={props.data}
                >
                    {props.openAxis ? (<ArgumentAxis />) : ''}
                    {props.openAxis ? (<ValueAxis />) : ''}
                    {props.children}

                    <Legend position="bottom" rootComponent={Root} labelComponent={Label} />
                    <Title text={props.data.length !== 0 ? props.title : ''} />
                    <Animation />
                    <EventTracker />
                    <HoverState />
                    <Tooltip
                        targetItem={targetToolTip}
                        onTargetItemChange={handleChangeToolTip}       
                        contentComponent={TooltipContent}                 
                    />
                </Chart>
            ) : ''}
        </>
    )
}

export default StackedBarChart