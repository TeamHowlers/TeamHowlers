import React from 'react';
import { render } from '@testing-library/react';
import WeatherForecast from './WeatherForecast';

test('renders learn react link', () => {
    const { getByText } = render(<WeatherForecast />);
    const linkElement = getByText(/5-Day Weather Forecast/i);
    expect(linkElement).toBeInTheDocument();
});