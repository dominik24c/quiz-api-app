import { render, screen } from '@testing-library/react';
import Footer from './Footer';

describe('Footer component', () => {
    test('renders copyright text', () => {
        render(<Footer />);
        const footerText = screen.getByText(/2021 quiz-app.com/);

        expect(footerText).toBeInTheDocument();

    });
});