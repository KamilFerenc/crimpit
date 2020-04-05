import React, { Component } from 'react';

import AsideNav from '../asideNav/asideNav';
import UserMainSection from '../userMainSection/userMainSection';
import './userArea.scss';

class UserArea extends Component {
    state = {};
    render() {
        return (
            <React.Fragment>
                <div className="ci-user-area__wrapper .container-fluid">
                    <div className="row ci-user-area__inner">
                        <AsideNav />
                        <UserMainSection />
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default UserArea;
