import React, { Component } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

const API_URL = 'http://localhost:8001/api/logout/';

class Logout extends Component {
    constructor(props) {
        super(props);
        this.state = { popup: '', redirect: false };
    }

    logoutMessage = 'You have been logged out';

    getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }
        return cookieValue;
    }

    componentDidMount() {
        let csrftoken = this.getCookie('csrftoken');
        const redirect = this.state.redirect;

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios.defaults.withCredentials = true;

        axios({
            method: 'post',
            url: API_URL,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrftoken
            }
        }).then(response => {
            console.log(response);
            localStorage.removeItem('token');
            this.setState({ popup: this.logoutMessage });
            setTimeout(() => {
                this.setState({ redirect: true });
            }, 2000);
        });
    }

    render() {
        const redirect = this.state.redirect;
        if (redirect === true) {
            return <Redirect to="/" />;
        }

        return (
            <div>
                Logout
                <p>{this.state.popup}</p>
            </div>
        );
    }
}

export default Logout;
