import React, { Component } from 'react';
import { Col, Row, Button, Form, FormGroup, Label, Input } from 'reactstrap';
import { Redirect } from 'react-router-dom';
import axios from 'axios';
import { getCookie } from '../getCookie/getCookie';

import './login.scss';

const API_URL = 'http://localhost:8001/api/login/';

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = { username: '', password: '', redirect: false };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange = e => {
        this.setState({ [e.target.name]: e.target.value });
    };

    getCookie(name) {
        return getCookie(name);
    }

    handleSubmit = e => {
        e.preventDefault();
        let form_data = new FormData();
        let csrftoken = this.getCookie('csrftoken');

        form_data.append('username', this.state.username);
        form_data.append('password', this.state.password);

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
            },
            data: form_data
        }).then(response => {
            if (response.key !== '') {
                localStorage.setItem('token', response.data['key']);
                this.setState({ redirect: true });
            }
        });
    };

    defaultIfEmpty = value => {
        return value === '' ? '' : value;
    };

    render() {
        const redirect = this.state.redirect;
        if (redirect === true) {
            return <Redirect to="/user-area" />;
        }

        let csrftoken = this.getCookie('csrftoken');

        return (
            <div className="ci-register__wrapper">
                <Form onSubmit={this.handleSubmit}>
                    <Row form>
                        <Col md={6}>
                            <FormGroup>
                                <input
                                    type="hidden"
                                    name="csrfmiddlewaretoken"
                                    value={csrftoken}
                                />
                                <Label for="username">User name</Label>
                                <Input
                                    type="text"
                                    name="username"
                                    id="username"
                                    onChange={this.handleChange}
                                    value={this.defaultIfEmpty(
                                        this.state.username
                                    )}
                                />
                            </FormGroup>
                        </Col>
                        <Col md={6}>
                            <FormGroup>
                                <Label for="password">Password</Label>
                                <Input
                                    type="password"
                                    name="password"
                                    id="password"
                                    onChange={this.handleChange}
                                    value={this.defaultIfEmpty(
                                        this.state.password
                                    )}
                                />
                            </FormGroup>
                        </Col>
                    </Row>
                    <Button htmltype="submit">Login</Button>
                </Form>
            </div>
        );
    }
}
export default Login;
