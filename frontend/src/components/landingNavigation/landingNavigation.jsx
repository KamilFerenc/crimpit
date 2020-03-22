import React, { Component } from 'react';
import './landingNavigation.scss';

class LandingNavigation extends Component {
    state = {};
    render() {
        return (
            <nav className="navbar navbar-light bg-light ci-landing-navigation">
                <form className="form-inline ci-landing-navigation__form">
                    <button
                        className="btn btn-outline-primary ci-landing-navigation__login-button"
                        type="button"
                    >
                        Sign Up
                    </button>
                    <button
                        className="btn btn-outline-secondary m-2 ci-landing-navigation__signup-button"
                        type="button"
                    >
                        Log In
                    </button>
                </form>
            </nav>
        );
    }
}

export default LandingNavigation;
