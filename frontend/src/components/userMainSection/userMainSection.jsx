import React, { Component } from 'react';
import EditProfile from '../editProfile/editProfile';
import { Route, NavLink } from 'react-router-dom';

const mainSectionItems = [
    {
        name: 'test-yourself',
        path: '/test-yourself',
        nameLong: 'Test yourself',
        description: 'Description'
    },
    {
        name: 'browse-tests',
        path: '/browse-tests',
        nameLong: 'Browse tests',
        description: 'Description'
    },
    {
        name: 'create-test',
        path: '/create-test',
        nameLong: 'Create set of tests',
        description: 'Description'
    }
];

const cards = mainSectionItems.map(item => {
    return (
        <div className="col-4" key={item.name}>
            <div className="card ci-main-section__card">
                <img
                    className="card-img-top ci-main-section__card-img"
                    src=".../100px180/"
                    alt=""
                />
                <div className="card-body">
                    <h5 className="card-title">{item.nameLong}</h5>
                    <p className="card-text">{item.description}</p>
                    {/* <a href="#" className="btn btn-primary">
                </a> */}
                    <NavLink
                        to={item.name}
                        key={item.name}
                        activeClassName=""
                        className="btn btn-outline-primary ci-main-section__card-button"
                    >
                        {item.name}
                    </NavLink>
                </div>
            </div>
        </div>
    );
});

class UserMainSection extends Component {
    // constructor(props) {
    //     super(props);
    // }
    state = {};

    render() {
        return (
            <div className="ci-user-area__main-section col-9">
                User Main Section
                <div className="ci-main-section">
                    <div className="container">
                        <div className="row">{cards}</div>
                    </div>
                </div>
                <Route path="/edit-profile" component={EditProfile} />
            </div>
        );
    }
}

export default UserMainSection;
