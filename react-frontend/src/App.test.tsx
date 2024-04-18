import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Database Dump Section', () => {
  render(<App />);
  const linkElement = screen.getByText(/Database Dump/i);
  expect(linkElement).toBeInTheDocument();
});
