import React, { Component } from 'react';

import { Col, Row, Button, Form, FormGroup, Label, Input } from 'reactstrap';
import { Redirect } from 'react-router-dom';
import { getCookie } from '../getCookie/getCookie';
import axios from 'axios';

//edit profile
const API_URL_GET_USER_DATA = 'http://localhost:8001/api/user/';
const API_URL_SAVE_NEW_DATA = 'http://localhost:8001/api/user/';

class EditProfile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            email: '',
            type: 'athlete',
            club: '',
            birth_date: '',
            start_climbing: '',
            profile_photo: null,
            phone: '',
            city: '',
            redirect: false
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleImageChange = this.handleImageChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    getCookie(name) {
        return getCookie(name);
    }

    getUserData = () => {
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
            console.log(results.data);

            Object.keys(results.data).forEach(e => {
                if (results.data[e] === null) {
                    results.data[e] = '';
                }
            });
            this.setState(results.data);
            console.log('state', this.state);
        });
    };

    componentDidMount() {
        this.getUserData();
    }

    handleChange = e => {
        this.setState({ [e.target.name]: e.target.value });
    };

    handleImageChange = e => {
        this.setState({
            profile_photo: e.target.files[0]
        });

        console.log(e.target.files);
    };

    handleSubmit = e => {
        e.preventDefault();
        let form_data = new FormData();
        let csrftoken = this.getCookie('csrftoken');

        form_data.append(
            'profile_photo',
            this.state.profile_photo,
            this.state.profile_photo.name
        );
        form_data.append('username', this.state.username);
        form_data.append('email', this.state.email);
        form_data.append('type', this.state.type);
        form_data.append('club', this.state.club);
        form_data.append('birth_date', this.state.birth_date);
        form_data.append('start_climbing', this.state.start_climbing);
        form_data.append('profile_photo', this.state.profile_photo);
        form_data.append('phone', this.state.phone);
        form_data.append('city', this.state.username);

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios.defaults.withCredentials = true;

        console.log(form_data);

        axios({
            method: 'patch',
            url: API_URL_SAVE_NEW_DATA,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrftoken
            },
            data: form_data
        })
            .then(response => {
                console.log(response);
                // this.setState({ redirect: true });
            })
            .catch(response => {
                //handle error
                console.log(response);
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
        return (
            <div className="ci-register__wrapper">
                <Form onSubmit={this.handleSubmit}>
                    <Row form>
                        <Col md={6}>
                            <FormGroup>
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
                                <Label for="email">Email:</Label>
                                <Input
                                    type="email"
                                    name="email"
                                    id="email"
                                    onChange={this.handleChange}
                                    value={this.defaultIfEmpty(
                                        this.state.email
                                    )}
                                />
                            </FormGroup>
                        </Col>
                    </Row>
                    <Row>
                        <Col md={6}>
                            <FormGroup>
                                <Label for="type">User Type</Label>
                                <Input
                                    type="select"
                                    name="type"
                                    id="type"
                                    onChange={this.handleChange}
                                    value={this.state.type}
                                >
                                    <option>athlete</option>
                                    <option>trainer</option>
                                </Input>
                            </FormGroup>
                        </Col>
                        <Col md={6}>
                            <FormGroup>
                                <Label for="club">Club</Label>
                                <Input
                                    type="text"
                                    name="club"
                                    id="club"
                                    onChange={this.handleChange}
                                    value={this.defaultIfEmpty(this.state.club)}
                                />
                            </FormGroup>
                        </Col>
                    </Row>
                    <Row>
                        <Col md={6}>
                            <FormGroup>
                                <Label for="birth_date">Birth Date</Label>
                                <Input
                                    type="date"
                                    name="birth_date"
                                    id="birth_date"
                                    onChange={this.handleChange}
                                    value={this.defaultIfEmpty(
                                        this.state.birth_date
                                    )}
                                />
                            </FormGroup>
                        </Col>
                        <Col md={6}>
                            <FormGroup>
                                <Label for="start_climbing">
                                    Start of climbing - year
                                </Label>
                                <Input
                                    type="date"
                                    name="start_climbing"
                                    id="start_climbing"
                                    onChange={this.handleChange}
                                    value={this.defaultIfEmpty(
                                        this.state.start_climbing
                                    )}
                                />
                            </FormGroup>
                        </Col>
                    </Row>
                    <Row form>
                        <Col md={12}>
                            <FormGroup>
                                <Label for="photoFile">Profile photo</Label>
                                <Input
                                    type="file"
                                    name="profile_photo"
                                    id="profile_photo"
                                    accept="image/png, image/jpeg"
                                    onChange={this.handleImageChange}
                                />
                            </FormGroup>
                        </Col>
                    </Row>
                    <Row form>
                        <Col md={6}>
                            <FormGroup>
                                <Label for="phone">Phone</Label>
                                <Input
                                    type="text"
                                    name="phone"
                                    id="phone"
                                    onChange={this.handleChange}
                                    value={this.defaultIfEmpty(
                                        this.state.phone
                                    )}
                                />
                            </FormGroup>
                        </Col>
                        <Col md={6}>
                            <FormGroup>
                                <Label for="city">City</Label>
                                <Input
                                    type="text"
                                    name="city"
                                    id="city"
                                    onChange={this.handleChange}
                                    value={this.defaultIfEmpty(this.state.city)}
                                />
                            </FormGroup>
                        </Col>
                    </Row>

                    <Button htmltype="submit">Save</Button>
                </Form>
            </div>
        );
    }
}

export default EditProfile;
