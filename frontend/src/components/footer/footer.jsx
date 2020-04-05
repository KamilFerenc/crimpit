import React, { Component } from 'react';
import './footer.scss';

class Footer extends Component {
    render() {
        return (
            <footer className="footer mt-auto py-3 bg-light">
                <div className="container">
                    <span className="text-muted">Copiright: The Fernenz</span>
                </div>
            </footer>
        );
    }
}

export default Footer;
