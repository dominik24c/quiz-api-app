import { render, screen } from '@testing-library/react';
import Navbar from './Navbar';

describe('Navbar component', () => {
    test('renders navbars links', () => {
        render(<Navbar />);
        const listElement = screen.getByRole('list');
        const listItems = screen.getAllByRole('listitem');

        expect(listElement).toBeInTheDocument();
        expect(listItems.length).toEqual(3);

    });
});

