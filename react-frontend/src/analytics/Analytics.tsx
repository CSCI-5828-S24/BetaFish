import { GlobalStateProps } from "../types";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    PointElement,
    LineElement,
  } from 'chart.js';
import React from 'react'
import { Bar } from "react-chartjs-2";
import { Line } from "react-chartjs-2";
import { getCrimeCounts } from "../api-interface";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );


  export const bar_options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Bar Chart of Crime Totals in the Denver Area',
        color:'#ffffff',
        font: {
            size: 24,
            weight: 500,
        }
      },
    },
  };
  
  const bar_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
  
  export const bar_data = {
    labels: bar_labels,
    datasets: [
      {
        label: 'Crime Totals',
        data: [1,2,3,4,5,6,7],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      }
    ],
  };

  export const line_options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Frequency of Crime in Denver',
        color:'#ffffff',
        font: {
            size: 24,
            weight: 500,
        }
      },
    },
  };

  const line_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

  export const line_data = {
    labels: line_labels,
    datasets: [
      {
        label: 'Crime Frequency',
        data:  [2,3,1,7,6,9,7],
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)'
      }
    ],
  };

const Analytics = (props: GlobalStateProps) => {   

    return (
        <div id="analytics-div" className={props.globalState.active === "analytics"? "sectionactive":""}>
            <p>Something</p>
            <Bar options={bar_options} data={bar_data} />
            <p>----- BREAK -----</p>
            <Line options={line_options} data={line_data} />
        </div>
    );
}

export default Analytics;