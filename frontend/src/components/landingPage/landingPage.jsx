import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import './landingPage.scss';
import crimpImage from '../../images/crimp.png';
import measureImage from '../../images/measure.png';
import progressImage from '../../images/progress.png';

class LandingPage extends Component {
    state = {};
    render() {
        return (
            <main className="ci-landing-page__wrapper">
                <div className="container ci-landing-page__grid">
                    <div className="row ci-landing-page__logo-wrapper">
                        <div className=" ci-landing-page__logo">
                            <h4>Crimp it!</h4>
                        </div>
                    </div>
                    <div className="row ci-landing-page__features">
                        <div className="col ci-landing-page__feature">
                            <h3 className="ci-landing-page__feature-title">
                                Test
                            </h3>
                            <img
                                src={crimpImage}
                                className="ci-landing-page__feature-image"
                                alt=""
                            ></img>
                        </div>
                        <div className="col ci-landing-page__feature">
                            <h3 className="ci-landing-page__feature-title">
                                Measure
                            </h3>
                            <img
                                src={measureImage}
                                className="ci-landing-page__feature-image"
                                alt=""
                            ></img>
                        </div>
                        <div className="col ci-landing-page__feature">
                            <h3 className="ci-landing-page__feature-title">
                                Progress
                            </h3>
                            <img
                                src={progressImage}
                                className="ci-landing-page__feature-image"
                                alt=""
                            ></img>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col ci-landing-page__features-signup">
                            <NavLink
                                to={'register'}
                                activeClassName=""
                                className="btn btn-outline-primary ci-landing-navigation__button"
                            >
                                Register
                            </NavLink>
                        </div>
                    </div>
                </div>
            </main>
        );
    }
}

export default LandingPage;
