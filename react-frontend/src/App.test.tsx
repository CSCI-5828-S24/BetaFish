import React, { useState } from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';
import Search from './search/Search';
import { GlobalState } from './types';

test('renders Database Dump Section', () => {
  const globalState:GlobalState = {
    active: "search",
    filters: {
      lat: 39.74956044238265,
      long: -104.95078325271608,
      startDate: new Date().toJSON().slice(0, 10),
      endDate: new Date().toJSON().slice(0, 10)
    },
    map: {
        lat: 39.74956044238265,
        long: -104.95078325271608
    },
    crimeList: {
      page_no: 1,
      page_size: 20,
      data: []
    },
    crimeTotals: {
      data: []
    },
    analytics: {
      freq: {
        labels: [],
        datasets: [
          {
            label: 'Crime Frequency',
            data:  [],
            borderColor: '#ff936c',
            backgroundColor: '#ff936c'
          }
        ]
      },
      totals: {
        labels: [],
        datasets: [
          {
            label: 'Crime Totals',
            data: [],
            borderColor: '#ff936c',
            backgroundColor: '#ff936c',
          }
        ],
      },
    }
  };
  const setGlobalState = jest.fn();
  render(<Search globalState={globalState} setGlobalState={setGlobalState} />);
  const linkElement = screen.getByText(/Latitude/i);
  expect(linkElement).toBeInTheDocument();
});
