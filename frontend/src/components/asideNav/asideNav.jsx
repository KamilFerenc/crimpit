import React, { Component } from 'react';

import profileImg from '../../images/profile.png';
import { NavLink } from 'react-router-dom';

import './asideNav.scss';

class asideNav extends Component {
    state = {};
    render() {
        return (
            <div className="ci-user-area__aside-nav col-3">
                <div className="ci-aside-nav">
                    Aside Nav
                    <div className="ci-aside-nav__item ci-aside-nav__item--picture-container">
                        {' '}
                        <img src={profileImg} alt="" />
                    </div>
                    <div className="ci-aside-nav__item ci-aside-nav__item--edit-profile">
                        <NavLink
                            to="edit-profile"
                            key="edit-profile"
                            activeClassName=""
                            className=""
                        >
                            Edit profile
                        </NavLink>
                    </div>
                    <div className="ci-aside-nav__item ci-aside-nav__item--request-trainer">
                        <NavLink
                            to="/request-trainer"
                            key="request-trainer"
                            activeClassName=""
                            className=""
                        >
                            Request trainer
                        </NavLink>
                    </div>
                </div>
            </div>
        );
    }
}

export default asideNav;
