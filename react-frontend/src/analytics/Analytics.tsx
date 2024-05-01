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
import React, { useEffect } from 'react'
import { Bar } from "react-chartjs-2";
import { Line } from "react-chartjs-2";
import { getCrimeFreq, getCrimeTotals } from "../api-interface";
import "./Analytics.css"

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
        labels: {
          color: '#ffffff',
        },
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

  export const line_options = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: '#ffffff',
        },
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
      scales: {
        yAxes: [{
          ticks: {
              fontColor: '#fff'
          }
        }],
        xAxes: [{
          ticks: {
              fontColor: '#fff'
          }
        }]
      }
    },
  };


const Analytics = (props: GlobalStateProps) => {   

    useEffect(() => {
      getCrimeFreq(props)
      getCrimeTotals(props)
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <div id="analytics-div" className={props.globalState.active === "analytics"? "sectionactive":""}>
            <br/>
            <Bar id="first-chart" options={bar_options} data={props.globalState.analytics.totals} />
            <br/>
            <Line id="second-chart" options={line_options} data={props.globalState.analytics.freq} />
        </div>
    );
}

export default Analytics;