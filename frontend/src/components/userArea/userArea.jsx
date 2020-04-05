import React, { Component } from 'react';

import AsideNav from '../asideNav/asideNav';
import UserMainSection from '../userMainSection/userMainSection';
import './userArea.scss';
import EditProfile from '../editProfile/editProfile';

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

class UserArea extends Component {
    state = {};
    render() {
        return (
            <React.Fragment>
                <div className="ci-user-area__wrapper .container-fluid">
                    <div className="row ci-user-area__inner">
                        <AsideNav />
                        <Switch>
                            <Route
                                path="/user-area"
                                exact
                                component={UserMainSection}
                                key="user-area"
                            />
                            <Route
                                path="/edit-profile"
                                exact
                                component={EditProfile}
                                key="edit-profile"
                            />
                        </Switch>
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default UserArea;
