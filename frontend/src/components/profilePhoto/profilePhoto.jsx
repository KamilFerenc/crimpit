import React, { Component } from 'react';
import { getCookie } from '../getCookie/getCookie';
import defaultDrofileImg from '../../images/profile.png';
import axios from 'axios';

const API_URL_GET_USER_DATA = 'http://localhost:8001/api/user/';

class ProfilePhoto extends Component {
    constructor(props) {
        super(props);
        this.state = { profile_photo: defaultDrofileImg };
    }

    getCookie(name) {
        return getCookie(name);
    }

    getUserPhoto = () => {
        let csrftoken = this.getCookie('csrftoken');

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios.defaults.withCredentials = true;

        axios({
            method: 'get',
            url: API_URL_GET_USER_DATA,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrftoken
            }
        }).then(results => {
            if (results.data.profile_photo !== null) {
                this.setState((state, props) => ({
                    profile_photo: results.data.profile_photo
                }));
            } else if (results.data.profile_photo === null) {
                results.data.profile_photo = '';
                this.setState((state, props) => ({
                    profile_photo: defaultDrofileImg
                }));
            }
        });
    };

    componentDidMount() {
        this.getUserPhoto();
    }

    render() {
        return (
            <div>
                <div className="ci-aside-nav__item ci-aside-nav__item--picture-container">
                    {' '}
                    <img src={this.state.profile_photo} alt="" />
                </div>
            </div>
        );
    }
}

export default ProfilePhoto;
