import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Multiply Section', () => {
  render(<App />);
  const linkElement = screen.getByText(/Multiply/i);
  expect(linkElement).toBeInTheDocument();
});
