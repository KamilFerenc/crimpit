import React, { Component } from 'react';
import beastmaker from '../../images/beastmaker.jpg';
import campus from '../../images/campus.jpg';
import AddSurveyBeast from './addSurveyBeast';

class AddSurvey extends Component {
    state = {};
    render() {
        return (
            <div class="ci-container__wrapper">
                <div class="ci-container__inner">
                    <div class="ci-container--add-survey ci-add-survey">
                        <div class="ci-container--add-survey ci-add-survey">
                            <h3>Add survey</h3>
                            <div class="ci-add-survey__items">
                                <div class="ci-add-survey__item ci-add-survey__item--beast">
                                    <a href="#" class="ci-add-survey__link">
                                        <img
                                            src={beastmaker}
                                            class="ci-add-survey__image ci-add-survey__image--beasr"
                                        ></img>
                                    </a>
                                </div>
                                <div class="ci-add-survey__item ci-add-survey__item--campus">
                                    <a href="#" class="ci-add-survey__link">
                                        <img
                                            src={campus}
                                            class="ci-add-survey__image ci-add-survey__image--campus"
                                        ></img>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default AddSurvey;
