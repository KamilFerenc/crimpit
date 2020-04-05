import React, { Component } from 'react';
import { Route, NavLink } from 'react-router-dom';

import './topBar.scss';

const landingPageTopBarItems = [
    { name: 'login', path: '/login' },
    { name: 'register', path: '/register' }
];

const loginTopBarItems = [{ name: 'back', destination: '/' }];

const userAreaTopBarItems = [{ name: 'logout', path: '/logout' }];
const userAreaEditProfileTopBarItems = [
    { name: 'back', destination: '/user-area' },
    { name: 'logout', path: '/logout' }
];

class TopBar extends Component {
    // constructor(props) {
    //     super(props);
    // }

    goBack = () => {
        this.props.history.goBack();
    };

    renderItems = (location, itemsList) => {
        const items = itemsList.map(item => {
            return item.name !== 'back' ? (
                <NavLink
                    to={item.name}
                    key={item.name}
                    activeClassName=""
                    className="btn btn-outline-primary ci-landing-navigation__button"
                >
                    {item.name}
                </NavLink>
            ) : (
                <NavLink
                    to={item.destination}
                    key={item.name}
                    activeClassName=""
                    className="btn btn-outline-primary ci-landing-navigation__button"
                >
                    {item.name}
                </NavLink>
            );
        });
        return (
            <Route exact path={location}>
                {items}
            </Route>
        );
    };

    render() {
        return (
            <>
                <nav className="navbar navbar-light bg-light ci-landing-navigation">
                    <form className="form-inline ci-landing-navigation__form">
                        {this.renderItems('/', landingPageTopBarItems)}
                        {this.renderItems('/login', loginTopBarItems)}
                        {this.renderItems('/register', loginTopBarItems)}
                        {this.renderItems('/user-area', userAreaTopBarItems)}
                        {this.renderItems(
                            '/edit-profile',
                            userAreaEditProfileTopBarItems
                        )}
                    </form>
                </nav>
            </>
        );
    }
}

export default TopBar;
