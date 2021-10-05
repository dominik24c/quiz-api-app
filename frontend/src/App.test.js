import { render, screen } from '@testing-library/react';
import App from './App';


describe('App Component',()=>{
  test('renders Quiz app as text', () => {
    const header = document.createElement('header');
    header.setAttribute('id','navbar');
    const footer = document.createElement('footer');
    footer.setAttribute('id','footer');
    global.document.body.appendChild(header);
    global.document.body.appendChild(footer);

    render(<App />);
    const linkElement = screen.getByText('Quiz app');
    expect(linkElement).toBeInTheDocument();
  });
})

